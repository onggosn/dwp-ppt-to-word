"""PPTX -> DOCX + HTML (CKEditor) tanpa LLM: layout ditentukan dari geometri shape.

Alur:
  1. collect()   baca semua shape (python-pptx) dengan koordinat absolut di slide (transform group ikut).
  2. analyse()   tentukan peran tiap shape dengan aturan: judul, sub-judul, caption, isi, gambar, tabel, catatan.
                 Caption dipasangkan ke gambar tepat di bawah/atasnya; kolom teks berdampingan dibaca per kolom.
  3. render      slide dirender PowerPoint (COM) lalu tiap gambar di-crop dari render, jadi grafik yang
                 di-group, overlay, WMF dan diagram ikut utuh. Tanpa PowerPoint: pakai gambar asli dari PPTX.
  4. tulis       blok yang sama ditulis ke DOCX (python-docx, style dari template docs/example.docx)
                 dan ke HTML mandiri (gambar base64) yang bisa langsung dipakai di CKEditor.
  5. opsional    LLM hanya merapikan teks per paragraf (JSON in/out, divalidasi); layout tidak disentuh LLM.

CLI:
    python layout_engine.py docs/test.pptx -o work/test.docx [--llm gemini --model gemini-3.8-flash]
"""
from __future__ import annotations

import argparse
import base64
import copy
import html
import json
import re
import shutil
import subprocess
import threading
from dataclasses import dataclass, field
from pathlib import Path
from typing import Callable, Optional

from docx import Document
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Emu, Pt
from PIL import Image
from pptx import Presentation
from pptx.enum.shapes import MSO_SHAPE_TYPE, PP_PLACEHOLDER

HERE = Path(__file__).resolve().parent
DEFAULT_TEMPLATE = HERE / "docs" / "example.docx"

# Ambang aturan (fraksi lebar/tinggi slide)
ICON_MAX_W = 0.08         # gambar lebih sempit dari ini = ikon/logo, dibuang
WIDE_MIN_W = 0.5          # gambar selebar ini atau lebih = baris penuh (colspan)
LABEL_MAX_H = 0.08        # label/caption maksimal setinggi ini
LABEL_MAX_H_FILLED = 0.12 # ... kecuali bilah berwarna (caption grafik panjang)
LABEL_MAX_CHARS = 260
NOTE_MIN_Y = 0.9          # teks yang mulai di bawah ini = catatan kaki
STICKER_MAX_W = 0.12      # teks kecil di atas elemen lain ("Tindak Lanjut", "UPDATED") = stiker, dibuang
PANEL_MIN_AREA = 0.06     # shape latar minimal seluas ini untuk dianggap panel teks
TABLE_MAX_COLS = 12      # tabel PPT lebih lebar dari ini dijadikan gambar (tidak muat di halaman Word)
FIG_COL_SPLIT = (0.72, 0.28)   # rasio kolom tabel gambar di example.docx (6509/2507 twips)

ProgressFn = Callable[[float, str], None]
Run = tuple  # (text, bold, italic)


def _noop(_f: float, _m: str) -> None:
    pass


# --------------------------------------------------------------------------- model
@dataclass
class Para:
    runs: list            # [(text, bold, italic)]
    level: int = 0
    bullet: bool = False
    numbered: bool = False    # buAutoNum -> list bernomor (1. 2. 3.), selain itu bullet
    num_fmt: str = "decimal"  # format nomor Word: decimal | lowerLetter | upperLetter | lowerRoman | upperRoman

    @property
    def text(self) -> str:
        return "".join(r[0] for r in self.runs).strip()


@dataclass
class Box:
    kind: str             # text | picture | table
    x: float
    y: float
    w: float
    h: float
    name: str = ""
    paras: list = field(default_factory=list)    # [Para] untuk text
    rows: list = field(default_factory=list)     # [[str]] untuk table
    images: list = field(default_factory=list)   # [(blob, ext, area)] untuk picture (cadangan tanpa render)
    col_widths: list = field(default_factory=list)  # tabel grid: lebar relatif kolom (dari header di slide)
    is_title: bool = False
    is_placeholder_body: bool = False
    filled: bool = False      # kotak teks berwarna (node diagram / bilah), bukan text box polos
    fill_cells: int = 0       # tabel: sel kosong berwarna (bar Gantt, status warna) -> maknanya ada di warna

    @property
    def r(self) -> float:
        return self.x + self.w

    @property
    def b(self) -> float:
        return self.y + self.h

    @property
    def text(self) -> str:
        return " ".join(p.text for p in self.paras).strip()

    @property
    def runs(self) -> list:
        out = []
        for i, p in enumerate(self.paras):
            if i:
                out.append((" ", False, False))
            out += p.runs
        return out


# Blok keluaran (dipakai DOCX dan HTML writer)
@dataclass
class Block:
    type: str             # heading | para | bullet | figures | table | note
    level: int = 0
    runs: list = field(default_factory=list)
    numbered: bool = False
    col_widths: list = field(default_factory=list)   # table: lebar relatif kolom (kosong = rata)
    num_fmt: str = "decimal"                          # bullet bernomor: format nomor Word
    rows: list = field(default_factory=list)     # figures: [{"img": Path, "wide": bool, "caption": runs}], table: [[str]]


# --------------------------------------------------------------------------- 1. collect
_CONTROL_RE = re.compile("[\x00-\x08\x0b\x0c\x0e-\x1f￾￿-​-‍⁠﻿]")


def _clean(text: str, vt: str = " ") -> str:
    """Buang karakter kontrol yang tidak valid di XML Word, karakter Private Use Area
    (simbol font Wingdings/Symbol yang tampil sebagai kotak di luar PowerPoint) dan karakter
    tak terlihat (zero-width), supaya placeholder yang isinya cuma itu dianggap kosong.
    \\v (baris baru di sel tabel / text box PowerPoint) diganti `vt`."""
    return _CONTROL_RE.sub("", text.replace("\x0b", vt))


# Simbol font (disimpan PowerPoint sebagai U+F0xx) -> Unicode biasa, per typeface di <a:sym>
_SYMBOL_MAP = {
    "symbol": {0xAC: "←", 0xAD: "↑", 0xAE: "→", 0xAF: "↓", 0xAB: "↔", 0xB7: "•", 0xB4: "×",
               0xB3: "≥", 0xA3: "≤", 0xB1: "±", 0xB0: "°", 0xD6: "√", 0xBB: "≈", 0xB9: "≠"},
    "wingdings": {0xE0: "→", 0xE1: "←", 0xE2: "↑", 0xE3: "↓", 0xE8: "➔", 0xD8: "➢", 0xF0: "⇨",
                  0xFC: "✓", 0xFB: "✗", 0xFD: "☒", 0xFE: "☑", 0x6C: "●", 0x6E: "■", 0xA7: "▪",
                  0x9F: "•", 0x76: "❖", 0x71: "❑", 0xA8: "◻"},
    "wingdings 3": {0xC6: "➔", 0xC7: "⬅", 0xC8: "⬆", 0xC9: "⬇", 0x75: "►", 0x74: "◄", 0x70: "▲", 0x71: "▼"},
}


def _map_symbols(text: str, typeface: str) -> str:
    table = _SYMBOL_MAP.get((typeface or "").lower(), {})
    return "".join(table.get(ord(c) - 0xF000, c) if 0xF000 <= ord(c) <= 0xF0FF else c for c in text)


def _para_runs(p) -> list:
    """Run teks + bold/italic. <a:br/> jadi spasi (baris patah di PPT bukan paragraf baru)."""
    out = []
    for el in p._p:
        tag = el.tag.split("}")[1]
        if tag == "r":
            t = el.find(qn("a:t"))
            rpr = el.find(qn("a:rPr"))
            sym = rpr.find(qn("a:sym")) if rpr is not None else None
            text = t.text if t is not None and t.text else ""
            if sym is not None:
                text = _map_symbols(text, sym.get("typeface"))
            text = _clean(text)
            b = rpr is not None and rpr.get("b") in ("1", "true")
            i = rpr is not None and rpr.get("i") in ("1", "true")
            if text:
                out.append((text, b, i))
        elif tag == "br":
            out.append((" ", False, False))
        elif tag == "fld":
            t = el.find(qn("a:t"))
            if t is not None and t.text:
                out.append((_clean(t.text), False, False))
    # rapikan spasi ganda di tepi
    return [r for r in out if r[0]]


_AUTONUM_FMT = (("alphaLc", "lowerLetter"), ("alphaUc", "upperLetter"),
                ("romanLc", "lowerRoman"), ("romanUc", "upperRoman"))


def _bullet_kind(p, placeholder_body: bool) -> tuple:
    """(bullet?, bernomor?, format nomor) dari markup paragraf; tanpa markup: placeholder isi /
    indentasi = bullet."""
    ppr = p._p.pPr
    if ppr is not None:
        tags = {c.tag.split("}")[1] for c in ppr}
        if "buNone" in tags:
            return False, False, "decimal"
        if "buAutoNum" in tags:
            kind = ppr.find(qn("a:buAutoNum")).get("type", "")
            fmt = next((f for prefix, f in _AUTONUM_FMT if kind.startswith(prefix)), "decimal")
            return True, True, fmt
        if tags & {"buChar", "buBlip"}:
            return True, False, "decimal"
    return placeholder_body or p.level > 0, False, "decimal"


_MANUAL_NUM_RE = re.compile(r"^\s*(\d{1,2})[.)]\s+")


def _continue_manual_numbers(blocks: list) -> list:
    """Paragraf yang nomornya diketik manual ("2.   Kebijakan ...") padahal item sebelumnya di level
    yang sama memakai nomor otomatis (1.) dijadikan item bernomor lanjutan, asalkan nomornya pas
    berurutan. Word lalu melanjutkan penomorannya sendiri (1 -> 2)."""
    out = []
    for bl in blocks:
        m = _MANUAL_NUM_RE.match("".join(r[0] for r in bl.runs)) if bl.type == "para" else None
        if m:
            same = [b for b in out if b.type == "bullet" and b.numbered and b.level == bl.level
                    and b.num_fmt == "decimal"]
            if same and int(m.group(1)) == len(same) + 1:
                runs, cut = list(bl.runs), m.end()
                while runs and cut >= len(runs[0][0]):     # buang awalan "2.   " dari run-run pertama
                    cut -= len(runs[0][0])
                    runs.pop(0)
                if runs:
                    runs[0] = (runs[0][0][cut:],) + tuple(runs[0][1:])
                out.append(Block("bullet", bl.level, runs, numbered=True, num_fmt="decimal"))
                continue
        out.append(bl)
    return out


def _xfrm(grp):
    x = grp._element.grpSpPr.find(qn("a:xfrm"))
    if x is None:
        return None
    def get(tag, a, b):
        e = x.find(qn(tag))
        return (int(e.get(a)), int(e.get(b))) if e is not None else None

    off, ext = get("a:off", "x", "y"), get("a:ext", "cx", "cy")
    if off is None or ext is None:
        return None
    # tanpa chOff/chExt: anak sudah memakai koordinat yang sama dengan group
    return off, ext, get("a:chOff", "x", "y") or off, get("a:chExt", "cx", "cy") or ext


def _has_fill(s) -> bool:
    """Shape punya isian warna: eksplisit di spPr, atau dari style tema (fillRef idx > 0) tanpa noFill."""
    try:
        sppr = s._element.spPr
    except AttributeError:
        return False
    if sppr.find(qn("a:noFill")) is not None:
        return False
    if any(sppr.find(qn(t)) is not None for t in ("a:solidFill", "a:gradFill", "a:pattFill", "a:blipFill")):
        return True
    ref = s._element.find(".//" + qn("a:fillRef"))
    return ref is not None and ref.get("idx", "0") != "0"


def _empty_filled_cells(table) -> int:
    """Jumlah sel tanpa teks yang diberi warna (bukan putih). Sel gabungan tidak dihitung."""
    n = 0
    for row in table.rows:
        for c in row.cells:
            if c.is_spanned or c.text.strip():
                continue
            tcpr = c._tc.tcPr
            fill = tcpr.find(qn("a:solidFill")) if tcpr is not None else None
            clr = fill[0] if fill is not None and len(fill) else None
            if clr is not None and (clr.get("val") or "").upper() not in ("FFFFFF", "BG1", "LT1"):
                n += 1
    return n


def collect(shapes, W: int, H: int, tf=None) -> list:
    """Semua shape (group diratakan) dalam koordinat fraksi slide."""
    tf = tf or (lambda x, y, w, h: (x, y, w, h))
    out = []
    for s in shapes:
        if s.left is None or s.width is None:
            continue
        x, y, w, h = tf(s.left, s.top, s.width, s.height)
        if s.shape_type == MSO_SHAPE_TYPE.GROUP:
            xf = _xfrm(s)
            if xf is None:
                continue
            off, ext, ch_off, ch_ext = xf
            sx = ext[0] / ch_ext[0] if ch_ext[0] else 1.0
            sy = ext[1] / ch_ext[1] if ch_ext[1] else 1.0

            def child_tf(cx, cy, cw, ch, _p=tf, _o=off, _c=ch_off, _sx=sx, _sy=sy):
                return _p(_o[0] + (cx - _c[0]) * _sx, _o[1] + (cy - _c[1]) * _sy, cw * _sx, ch * _sy)

            out += collect(s.shapes, W, H, child_tf)
            continue

        box = Box("text", x / W, y / H, w / W, h / H, name=s.name or "")
        if s.shape_type == MSO_SHAPE_TYPE.PICTURE or (
                s.shape_type == MSO_SHAPE_TYPE.PLACEHOLDER and hasattr(s, "image")):
            try:
                img = s.image
                box.kind = "picture"
                box.images = [(img.blob, img.ext, box.w * box.h)]
            except Exception:
                continue
        elif getattr(s, "has_table", False) and s.has_table:
            box.kind = "table"
            box.rows = [[_clean(c.text, vt="\n").strip() for c in r.cells] for r in s.table.rows]
            box.col_widths = [int(c.width or 0) for c in s.table.columns]
            box.fill_cells = _empty_filled_cells(s.table)
        elif getattr(s, "has_chart", False) and s.has_chart:
            box.kind = "picture"      # chart native: diambil dari render
        elif s.has_text_frame:
            ph_type = s.placeholder_format.type if s.is_placeholder else None
            box.is_placeholder_body = ph_type in (PP_PLACEHOLDER.BODY, PP_PLACEHOLDER.OBJECT)
            box.is_title = ph_type in (PP_PLACEHOLDER.TITLE, PP_PLACEHOLDER.CENTER_TITLE)
            for p in s.text_frame.paragraphs:
                runs = _para_runs(p)
                if "".join(r[0] for r in runs).strip():
                    box.paras.append(Para(runs, int(p.level), *_bullet_kind(p, box.is_placeholder_body)))
            if not box.paras:
                box.kind = "shape"    # kotak/panah/garis tanpa teks: sinyal untuk deteksi diagram
            box.filled = _has_fill(s)
        else:
            box.kind = "shape"        # connector / garis
        out.append(box)
    return out


# --------------------------------------------------------------------------- 2. analyse
def _on_slide(b: Box) -> bool:
    cx, cy = b.x + b.w / 2, b.y + b.h / 2
    return 0 <= cx <= 1 and 0 <= cy <= 1 and b.w > 0.003 and b.h > 0.003


def _inter(a: Box, b: Box) -> float:
    return max(0.0, min(a.r, b.r) - max(a.x, b.x)) * max(0.0, min(a.b, b.b) - max(a.y, b.y))


def _h_overlap(a: Box, b: Box) -> float:
    return max(0.0, min(a.r, b.r) - max(a.x, b.x)) / max(min(a.w, b.w), 1e-6)


def _inside(inner: Box, outer: Box, tol: float = 0.01) -> bool:
    return (inner.x >= outer.x - tol and inner.r <= outer.r + tol
            and inner.y >= outer.y - tol and inner.b <= outer.b + tol)


def _is_label(b: Box) -> bool:
    """Teks pendek, (hampir) kapital semua, tidak tinggi -> label / caption / sub-judul."""
    t = b.text
    letters = [c for c in t if c.isalpha()]
    # bilah berwarna (caption grafik) boleh lebih tinggi: caption panjang bisa sampai 4 baris
    max_h = LABEL_MAX_H_FILLED if b.filled else LABEL_MAX_H
    return (b.kind == "text" and not b.is_title and bool(t) and len(t) <= LABEL_MAX_CHARS
            and b.h <= max_h and bool(letters)
            and sum(c.isupper() for c in letters) / len(letters) > 0.8)


def merge_pictures(pics: list) -> list:
    """Gambar yang saling menumpuk (grafik + overlay legend/tabel) digabung jadi satu unit."""
    units = [copy.copy(p) for p in pics]
    changed = True
    while changed:
        changed = False
        for i in range(len(units)):
            for j in range(i + 1, len(units)):
                a, b = units[i], units[j]
                small = min(a.w * a.h, b.w * b.h)
                if small and _inter(a, b) / small > 0.2:
                    x, y = min(a.x, b.x), min(a.y, b.y)
                    r, btm = max(a.r, b.r), max(a.b, b.b)
                    # nama khusus (diagram / grid-image) dipertahankan supaya asal unit tetap diketahui
                    name = next((u.name for u in (a, b) if u.name in ("diagram", "grid-image")), a.name)
                    units[i] = Box("picture", x, y, r - x, btm - y, name=name,
                                   images=a.images + b.images, rows=a.rows or b.rows)
                    del units[j]
                    changed = True
                    break
            if changed:
                break
    return units


def _pick_title(boxes: list) -> Optional[Box]:
    # placeholder judul yang kosong tersimpan sebagai "shape" -> bukan judul
    t = next((b for b in boxes if b.is_title and b.kind == "text"), None)
    if t:
        return t
    named = [b for b in boxes if b.kind == "text" and re.match(r"(title|judul)", b.name, re.I)]
    return min(named, key=lambda b: b.y, default=None)


# --- grid: "tabel" yang disusun dari text box (header sejajar + kolom pengelompok baris)
GRID_HEADER_MAX_CHARS = 45
GRID_MIN_COLS = 3
GRID_MIN_ROWS = 2
GRID_HEADER_GAP = 0.022        # sel header grid (hampir) menempel; celah lebih lebar = bukan satu header
GRID_WITH_MARKS_AS_IMAGE = True  # grid dengan titik progres (TW I-IV) diambil sebagai gambar; False = tabel
                                 # Word dengan label "(TW II)" di teks deliverable
GRID_FOOTER_Y = 0.96          # teks yang mulai di bawah ini (legenda) tidak masuk tabel
GRID_ROW_COVERAGE = 0.85       # minimal porsi kotak isi yang masuk ke baris; kurang = mode daftar per kolom
GRID_LIST_GAP = 0.05           # mode daftar: jarak vertikal maksimum antar kotak dalam satu kolom
GRID_COLUMN_FIT = 0.8       # >= 75% kotak isi minimal 80% lebarnya berada di dalam kolomnya


def _cell_text(boxes: list, notes: Optional[dict] = None) -> str:
    """notes: {id(box): [label]} -> ditempel di akhir teks box itu, mis. "RBT New BI-FAST (TW II)"."""
    lines = []
    for b in sorted(boxes, key=lambda b: (round(b.y, 3), b.x)):
        box_lines = []
        for p in b.paras:
            t = "".join(r[0] for r in _strip_runs(p.runs))
            if t:
                box_lines.append(("• " if p.bullet else "") + t)
        if box_lines and notes and notes.get(id(b)):
            box_lines[-1] += " (" + ", ".join(notes[id(b)]) + ")"
        lines += box_lines
    return "\n".join(lines)


def _mark_labels(header, top, rows, texts, marks) -> tuple:
    """Penanda kecil (titik/centang) di bawah sub-header kolom (mis. TW -> I II III IV) diubah jadi
    label teks. Label ditempel ke teks sebaris di kolom sebelah kirinya; kalau tidak ada, ke sel itu sendiri.
    Mengembalikan ({id(box): [label]}, {(row, col): [label]})."""
    subs = {}
    for c, h in enumerate(header):
        subs[c] = [t for t in texts if len(t.text.strip()) <= 4 and h.x - 0.005 <= t.x + t.w / 2 <= h.r + 0.005
                   and t.y >= h.b - 0.005 and t.b <= top + 0.01]
    notes, extra = {}, {}
    for ri, (lo, hi, cells) in enumerate(rows):
        for m in marks:
            cx, cy = m.x + m.w / 2, m.y + m.h / 2
            if not lo <= cy < hi:
                continue
            for c, ss in subs.items():
                sub = next((s for s in ss if s.x - 0.003 <= cx <= s.r + 0.003), None)
                if not sub:
                    continue
                label = f"{header[c].text.strip()} {sub.text.strip()}"
                left = [t for t in cells[c - 1] if abs((t.y + t.h / 2) - cy) < 0.02] if c > 0 else []
                target = min(left, key=lambda t: abs((t.y + t.h / 2) - cy), default=None)
                if target is not None:
                    notes.setdefault(id(target), []).append(label)
                else:
                    extra.setdefault((ri, c), []).append(label)
                break
    return notes, extra


def detect_grids(texts: list, marks: list = ()) -> tuple:
    """Cari baris header (>= 3 teks pendek sejajar, berdampingan) lalu bangun tabel di bawahnya.
    Baris ditentukan oleh kotak di kolom pertama/kedua (mis. "ICT 3.1.1 SP RITEL") yang tingginya
    menutupi barisnya; teks lain masuk ke sel menurut posisi tengahnya.
    Mengembalikan ([Box table], set id teks yang dipakai)."""
    used, grids = set(), []
    # lencana nomor ("3", "4", ...) yang menempel di header tidak ikut membentuk baris header
    heads = sorted([t for t in texts if len(t.text) <= GRID_HEADER_MAX_CHARS and t.h <= 0.07
                    and not t.text.strip().isdigit()], key=lambda t: t.y)
    # kelompokkan per garis horizontal: tepi atas sejajar (header bertingkat seperti "TW" di atas
    # I-IV punya tengah yang berbeda, tapi tepi atasnya sama dengan header lain)
    lines, cur = [], []
    for t in heads:
        if cur and abs(t.y - cur[0].y) > 0.012:
            lines.append(cur)
            cur = []
        cur.append(t)
    if cur:
        lines.append(cur)

    for line in lines:
        line = sorted(line, key=lambda t: t.x)
        runs, run = [], [line[0]]
        for prev, nxt in zip(line, line[1:]):
            if nxt.x - prev.r > GRID_HEADER_GAP or nxt.x < prev.r - 0.01:   # berjarak / tumpang tindih
                runs.append(run)
                run = []
            run.append(nxt)
        runs.append(run)
        for header in runs:
            if len(header) < GRID_MIN_COLS or header[-1].r - header[0].x < 0.25:
                continue
            if not all(any(c.isalpha() for c in h.text) for h in header):
                continue          # deretan angka (isi tabel) bukan header
            if any(id(h) in used for h in header):
                continue
            left, right, top = header[0].x - 0.01, header[-1].r + 0.01, max(h.b for h in header)
            # legenda di tepi bawah slide ("Progressing on target", ...) bukan bagian tabel
            members = [t for t in texts if id(t) not in used and t not in header and len(t.text.strip()) > 2
                       and t.y + t.h / 2 > top and t.y < GRID_FOOTER_Y and left <= t.x + t.w / 2 <= right]

            def col_of(t):
                cx = t.x + t.w / 2
                inside = [i for i, h in enumerate(header) if h.x - 0.005 <= cx <= h.r + 0.005]
                return inside[0] if inside else min(range(len(header)),
                                                    key=lambda i: abs(cx - (header[i].x + header[i].w / 2)))

            by_col = {}
            for t in members:
                by_col.setdefault(col_of(t), []).append(t)
            anchors = None
            for c in range(min(2, len(header))):
                cands = sorted([t for t in by_col.get(c, []) if len(t.text) > 2], key=lambda t: t.y)
                # kotak pengelompok baris tidak saling tumpang tindih secara vertikal
                if len(cands) >= GRID_MIN_ROWS and all(a.b <= b.y + 0.01 for a, b in zip(cands, cands[1:])):
                    anchors = cands
                    break
            rows, row_used, bands = [], set(), []
            if anchors:
                for i, a in enumerate(anchors):
                    end = a.b + 0.008
                    if i + 1 < len(anchors):
                        end = min(end, anchors[i + 1].y)
                    bands.append((a.y - 0.008, end))
                for lo, hi in bands:
                    cells = [[] for _ in header]
                    for t in members:
                        cy = t.y + t.h / 2
                        if lo <= cy < hi:
                            cells[col_of(t)].append(t)
                            row_used.add(id(t))
                    rows.append(cells)
            if not anchors or len(row_used) < GRID_ROW_COVERAGE * len(members) or \
                    sum(1 for r in rows if sum(1 for c in r if c) >= 2) < GRID_MIN_ROWS:
                # daftar per kolom (mis. matriks inisiatif): kotak bertumpuk langsung di bawah tiap header,
                # baris tidak sejajar antar kolom -> satu baris isi berisi semua item per kolom
                cells, row_used = [[] for _ in header], set()
                for c, h in enumerate(header):
                    prev_b = top
                    for t in sorted(by_col.get(c, []), key=lambda t: t.y):
                        if t.y - prev_b > GRID_LIST_GAP or t.x < h.x - 0.02 or t.r > h.r + 0.02:
                            break
                        cells[c].append(t)
                        row_used.add(id(t))
                        prev_b = t.b
                # daftar sungguhan: minimal 3 kolom terisi dan minimal 2 kolom berisi >= 2 item
                # (matriks berwarna 2x2 dengan satu kotak per kolom = diagram, bukan daftar)
                if sum(1 for c in cells if c) < GRID_MIN_COLS or sum(1 for c in cells if len(c) >= 2) < 2:
                    continue
                rows = [cells]
                bands = [(top, max(t.b for c in cells for t in c) + 0.005)]
            # grid asli: tiap kotak isi berada di dalam lebar kolomnya. Diagram yang kebetulan punya
            # deretan label sejajar (atau dua tabel bersebelahan) gagal di sini.
            fits = sorted(max(0.0, min(t.r, header[c].r) - max(t.x, header[c].x)) / max(t.w, 1e-6)
                          for r in rows for c, cell in enumerate(r) for t in cell)
            if not fits or fits[len(fits) // 4] < GRID_COLUMN_FIT:
                continue
            notes, extra = _mark_labels(header, top, [(lo, hi, r) for (lo, hi), r in zip(bands, rows)],
                                        texts, marks)
            if (notes or extra) and GRID_WITH_MARKS_AS_IMAGE:
                # tabel progress dengan titik penanda (mis. TW I-IV) lebih terbaca sebagai gambar utuh;
                # legenda tepat di bawah tabel ("Progressing on target", ...) ikut dalam gambar
                bottom = max(hi for _, hi in bands)
                legend = [t for t in texts if id(t) not in used and t not in header and bottom - 0.01 <= t.y <= bottom + 0.04
                          and left <= t.x + t.w / 2 <= right]
                if legend:
                    bottom = max([bottom] + [t.b for t in legend])
                    row_used |= {id(t) for t in legend}
                grids.append(Box("picture", left, header[0].y, right - left, bottom - header[0].y,
                                 name="grid-image"))
                used |= {id(h) for h in header} | row_used
                continue

            def cell(ri, ci, boxes):
                text = _cell_text(boxes, notes)
                more = ", ".join(extra.get((ri, ci), []))
                return "\n".join(x for x in (text, more) if x)

            table_rows = [[_cell_text([h]) for h in header]] + \
                [[cell(ri, ci, c) for ci, c in enumerate(r)] for ri, r in enumerate(rows)]
            # kolom yang kosong di semua baris isi (mis. kolom ikon/progress) dibuang
            keep = [i for i in range(len(header)) if any(r[i] for r in table_rows[1:])]
            table_rows = [[r[i] for i in keep] for r in table_rows]
            bottom = max(hi for _, hi in bands)
            grids.append(Box("table", left, header[0].y, right - left, bottom - header[0].y,
                             name="grid", rows=table_rows, col_widths=[header[i].w for i in keep]))
            used |= {id(h) for h in header} | row_used
    return grids, used


# --- diagram: kumpulan teks pendek + shape/ikon yang berdekatan -> satu gambar dari render
DIAGRAM_MIN_TEXTS = 3
DIAGRAM_MIN_GFX = 3
DIAGRAM_SHORT_CHARS = 90
DIAGRAM_MARGIN = 0.008
BACKGROUND_MIN_AREA = 0.15     # shape sebesar ini = latar belakang, bukan bagian diagram
DIAGRAM_FLOW_GROW = 0.03       # diagram alur: elemen sejauh ini dari area ikut masuk diagram
DIAGRAM_MIN_FLOW = 5          # >= 2 panah/shape + kotak berwarna berisi teks, total minimal sebanyak ini
DIAGRAM_MAX_CHART_SHARE = 0.4 # area kandidat diagram yang > 40% isinya grafik besar bukan diagram


def detect_diagrams(boxes: list, title: Optional[Box]) -> tuple:
    """Mengembalikan ([Box picture untuk tiap diagram], set id box yang tercakup di dalamnya)."""
    long_texts = [b for b in boxes if b.kind == "text" and len(b.text) > 120]

    def is_background(s):
        return s.w * s.h >= BACKGROUND_MIN_AREA or any(_inside(t, s, 0.005) for t in long_texts)

    gfx = [b for b in boxes if (b.kind == "shape" and not is_background(b))
           or (b.kind == "picture" and b.w < ICON_MAX_W)]
    charts = [b for b in boxes if b.kind == "picture" and b.w >= ICON_MAX_W]
    # caption grafik (label tepat di atas grafik besar dan kurang lebih selebar grafiknya) milik grafiknya,
    # bukan bagian diagram. Bilah yang jauh lebih sempit dari gambar di bawahnya = lapisan diagram.
    shorts = [b for b in boxes if b.kind == "text" and b is not title and len(b.text) <= DIAGRAM_SHORT_CHARS
              and not (_is_label(b) and any(_h_overlap(b, c) >= 0.6 and -0.03 <= c.y - b.b <= 0.06
                                            and abs(b.w - c.w) <= 0.25 * c.w for c in charts))]
    cands = gfx + shorts
    parent = list(range(len(cands)))

    def find(i):
        while parent[i] != i:
            parent[i] = parent[parent[i]]
            i = parent[i]
        return i

    m = DIAGRAM_MARGIN
    for i, a in enumerate(cands):
        for j in range(i + 1, len(cands)):
            b = cands[j]
            if a.x - m < b.r and b.x - m < a.r and a.y - m < b.b and b.y - m < a.b:
                parent[find(i)] = find(j)
    groups = {}
    for i, c in enumerate(cands):
        groups.setdefault(find(i), []).append(c)

    units, used = [], set()
    for members in groups.values():
        n_text = sum(1 for b in members if b.kind == "text")
        # garis tipis hanya menyambung, tidak dihitung sebagai elemen grafis
        n_gfx = sum(1 for b in members if b.kind != "text" and min(b.w, b.h) >= 0.01)
        # diagram alur: node berupa kotak berwarna berisi teks, dihubungkan panah
        n_nodes = sum(1 for b in members if b.kind == "text" and b.filled)
        is_flow = not n_gfx >= DIAGRAM_MIN_GFX
        if n_text < DIAGRAM_MIN_TEXTS or not (
                n_gfx >= DIAGRAM_MIN_GFX or (n_gfx >= 2 and n_gfx + n_nodes >= DIAGRAM_MIN_FLOW)):
            continue
        if is_flow:
            # diagram alur: jarak antar node (dihubungkan panah) bisa lebih lebar dari margin sambung,
            # jadi area diperluas menelan elemen di sekitarnya, termasuk kotak kesimpulan berwarna
            grow = [b for b in boxes if b not in members and b is not title and (
                b in gfx or b in shorts or (b.kind == "text" and b.filled and len(b.text) <= 250))]
            g = DIAGRAM_FLOW_GROW
            changed = True
            while changed:
                changed = False
                x0, y0 = min(b.x for b in members), min(b.y for b in members)
                x1, y1 = max(b.r for b in members), max(b.b for b in members)
                for b in list(grow):
                    if b.x < x1 + g and x0 - g < b.r and b.y < y1 + g and y0 - g < b.b:
                        members.append(b)
                        grow.remove(b)
                        changed = True
        # area dibatasi ke dalam slide dan tidak menutupi judul
        x, y = max(min(b.x for b in members), 0.0), max(min(b.y for b in members), 0.0)
        r, btm = min(max(b.r for b in members), 1.0), min(max(b.b for b in members), 1.0)
        if title is not None and title.b > y and _h_overlap(title, Box("", x, y, r - x, btm - y)) > 0:
            y = title.b
        # subjudul/keynote panjang tepat di bawah judul slide tetap teks: area dimulai di bawahnya
        if title is not None:
            for t in long_texts:
                if abs(t.y - title.b) < 0.03 and t.w > 0.6 and t.y - y < 0.03 and t.b < btm:
                    y = max(y, t.b)
        if r <= x or btm <= y or (r - x) * (btm - y) < 0.01:
            continue
        unit = Box("picture", x, y, r - x, btm - y, name="diagram")
        # area yang sebagian besar berisi grafik besar = deretan grafik + caption, bukan diagram;
        # grafik-grafik itu ditangani sebagai gambar biasa dengan caption masing-masing
        charts = sum(b.w * b.h for b in boxes if b.kind == "picture" and b.w >= ICON_MAX_W and _inside(b, unit, 0.01))
        if charts > DIAGRAM_MAX_CHART_SHARE * unit.w * unit.h:
            continue
        units.append(unit)
        # semua yang berada di dalam area diagram ikut ter-crop; teks panjang tetap ditulis sebagai teks
        used |= {id(b) for b in boxes if b is not title and _inside(b, unit, 0.005)
                 and not (b.kind == "text" and len(b.text) > 120)}
    return units, used


def analyse(slide, W: int, H: int, boxes: Optional[list] = None) -> dict:
    """boxes (opsional): hasil collect() yang sudah difilter _on_slide. Diisi oleh report_engine supaya
    hasil analisa (objek Box yang sama) bisa dipetakan kembali ke id elemennya."""
    if boxes is None:
        boxes = [b for b in collect(slide.shapes, W, H) if _on_slide(b)]
    title = _pick_title(boxes)
    if title:
        title.is_title = True
    # penanda progres di grid = shape kecil (titik). Ikon gambar (centang "Ahead Schedule") sudah
    # punya label teks sendiri, jadi tidak dihitung.
    marks = [b for b in boxes if b.kind == "shape" and b.w < 0.03 and b.h < 0.06]
    grids, used = detect_grids([b for b in boxes if b.kind == "text" and b is not title], marks)
    # shape/ikon di dalam area grid (titik progres, latar baris, garis) = dekorasi tabel
    used |= {id(b) for g in grids for b in boxes
             if (b.kind == "shape" or (b.kind == "picture" and b.w < ICON_MAX_W)) and _inside(b, g, 0.01)}
    boxes = [b for b in boxes if id(b) not in used]
    # huruf/angka dekorasi tunggal ("I", "S", "V", "1" di dalam lingkaran) tidak ditulis
    boxes = [b for b in boxes if not (b.kind == "text" and b is not title and len(b.text.strip()) <= 2)]
    diagrams, used = detect_diagrams(boxes, title)
    boxes = [b for b in boxes if id(b) not in used]
    # grid yang berada di dalam area diagram sudah ikut ter-crop di gambar diagram -> jangan dobel
    grids = [g for g in grids if not any(_inside(g, d, 0.02) for d in diagrams)]

    # tabel PPT yang sangat lebar tidak terbaca di halaman Word -> diambil sebagai gambar dari render
    wide_tables = [b for b in boxes if b.kind == "table" and max((len(r) for r in b.rows), default=0) > TABLE_MAX_COLS]
    pics = merge_pictures([b for b in boxes if b.kind == "picture" and b.w >= ICON_MAX_W] + diagrams +
                          [Box("picture", t.x, t.y, t.w, t.h, name=t.name, rows=t.rows) for t in wide_tables] +
                          [g for g in grids if g.kind == "picture"])
    tables = sorted([b for b in boxes if b.kind == "table" and b not in wide_tables] +
                    [g for g in grids if g.kind == "table"], key=lambda b: (b.y, b.x))
    texts = [b for b in boxes if b.kind == "text" and b is not title]

    # teks yang (sebagian besar) menimpa area gambar sudah ikut ter-crop dari render
    # (gambar tabel progress sudah memakai teks miliknya sendiri; teks lain yang menempel di tepinya tetap teks)
    texts = [t for t in texts if not any(_inside(t, p) or _inter(t, p) > 0.5 * t.w * t.h
                                         for p in pics if p.name != "grid-image")]
    # stiker: teks kecil pendek yang menempel di atas elemen lain (catatan kaki dikecualikan)
    def sticker(t):
        return (t.w < STICKER_MAX_W and len(t.text) < 40 and t.y < NOTE_MIN_Y
                and any(o is not t and _inter(t, o) > 0 for o in boxes
                        if o.kind in ("picture", "table") or (o.kind == "text" and o.w > t.w * 2)))
    texts = [t for t in texts if not sticker(t)]

    # label sempit yang menempel di tepi atas/bawah gambar = header kolom milik gambar itu
    # (mis. BASELINE | POTENTIAL RISK | TAIL RISK): area crop diperluas, label tidak ditulis ulang
    for p in pics:
        attached = [t for t in texts if _is_label(t) and t.w < 0.6 * p.w
                    and t.x >= p.x - 0.01 and t.r <= p.r + 0.01
                    and (-0.01 <= p.y - t.b <= 0.01 or -0.01 <= t.y - p.b <= 0.01)]
        if attached:
            top, bottom = min([p.y] + [t.y for t in attached]), max([p.b] + [t.b for t in attached])
            p.y, p.h = top, bottom - top
            texts = [t for t in texts if t not in attached]

    labels = [t for t in texts if _is_label(t)]

    def is_above(l, p):
        return _h_overlap(l, p) >= 0.6 and -0.03 <= p.y - l.b <= 0.06

    # satu caption yang menaungi beberapa grafik berdampingan -> grafik-grafik itu satu gambar dengan
    # caption tersebut; judul kecil tiap grafik (label di antara caption dan grafik) ikut ter-crop
    caps, used = {}, set()
    for l in labels:
        if id(l) in used:
            continue
        under = [p for p in pics if is_above(l, p) and p.x >= l.x - 0.02 and p.r <= l.r + 0.02]
        if len(under) >= 2 and max(p.y for p in under) - min(p.y for p in under) < 0.05:
            x, y = min(p.x for p in under), min(p.y for p in under)
            r, btm = max(p.r for p in under), max(p.b for p in under)
            inner = [t for t in labels if t is not l and id(t) not in used and t.y >= l.b - 0.005
                     and t.b <= y + 0.01 and t.x >= x - 0.01 and t.r <= r + 0.01]
            if inner:
                y = min([y] + [t.y for t in inner])
                texts = [t for t in texts if t not in inner]
                used |= {id(t) for t in inner}
            unit = Box("picture", x, y, r - x, btm - y, name=under[0].name,
                       images=sum((p.images for p in under), []))
            pics = [p for p in pics if p not in under] + [unit]
            caps[id(unit)] = l
            used.add(id(l))

    # caption: label tepat di atas gambar (konvensi deck) diberikan dulu ke semua gambar; baru setelah itu
    # gambar yang belum punya caption boleh memakai label tepat di bawahnya, asalkan label itu bukan
    # caption atas gambar lain
    for p in sorted(pics, key=lambda p: (p.y, p.x)):
        if id(p) in caps:
            continue
        above = [l for l in labels if id(l) not in used and is_above(l, p)]
        cap = min(above, key=lambda l: abs(p.y - l.b), default=None)
        if cap:
            caps[id(p)] = cap
            used.add(id(cap))
    for p in sorted(pics, key=lambda p: (p.y, p.x)):
        if id(p) in caps:
            continue
        below = [l for l in labels if id(l) not in used and _h_overlap(l, p) >= 0.6
                 and -0.03 <= l.y - p.b <= 0.04 and not any(is_above(l, o) for o in pics if o is not p)]
        cap = min(below, key=lambda l: abs(l.y - p.b), default=None)
        if cap:
            caps[id(p)] = cap
            used.add(id(cap))
    figures = [(p, caps.get(id(p))) for p in sorted(pics, key=lambda p: (p.y, p.x))]

    # panel grafik: teks pendek di dalam lebar caption, di antara caption dan grafik (judul grafik),
    # ikut ter-crop bersama grafiknya
    for p, cap in figures:
        if cap is None or cap.b > p.y + 0.01:
            continue
        inner = [t for t in texts if id(t) not in used and t is not cap and len(t.text) <= 120
                 and t.x >= cap.x - 0.01 and t.r <= cap.r + 0.01
                 and t.y >= cap.b - 0.005 and t.b <= p.y + 0.02]
        if inner:
            top, bottom = min([p.y] + [t.y for t in inner]), max([p.b] + [t.b for t in inner])
            left, right = min([p.x] + [t.x for t in inner]), max([p.r] + [t.r for t in inner])
            p.x, p.y, p.w, p.h = left, top, right - left, bottom - top
            used |= {id(t) for t in inner}

    rest = [t for t in texts if id(t) not in used]
    notes = sorted([t for t in rest if t.y >= NOTE_MIN_Y], key=lambda b: (b.y, b.x))
    rest = [t for t in rest if t.y < NOTE_MIN_Y]
    subheads = [t for t in rest if _is_label(t)]
    bodies = [t for t in rest if not _is_label(t)]

    # kolom: >= 2 body tinggi berdampingan -> dibaca per kolom, label di atasnya = judul kolom
    columns = []
    tall = sorted([b for b in bodies if b.h > 0.4], key=lambda b: b.x)
    if len(tall) >= 2 and all(tall[i].r <= tall[i + 1].x + 0.03 for i in range(len(tall) - 1)):
        for col in tall:
            head = next((s for s in subheads if _h_overlap(s, col) >= 0.6 and s.y < col.y + 0.05), None)
            columns.append((head, col))
        heads = [h for h, _ in columns if h]
        bodies = [b for b in bodies if b not in tall]
        subheads = [s for s in subheads if s not in heads]

    # panel berdampingan (mis. RPLN | PLM dengan sub-bagian yang sama): teks dibaca per panel, kiri ke
    # kanan, supaya isi kedua panel tidak selang-seling. Panel = shape latar yang berisi >= 3 teks.
    panels = []
    frames = [s for s in boxes if s.kind == "shape" and PANEL_MIN_AREA <= s.w * s.h <= 0.5]
    inside_of = {id(f): [t for t in subheads + bodies + notes if _inside(t, f, 0.01)] for f in frames}
    frames = [f for f in frames if len(inside_of[id(f)]) >= 3]
    frames = [f for f in frames if not any(o is not f and _inside(f, o, 0.005) for o in frames)]  # terluar
    row = sorted(frames, key=lambda f: f.x)
    if len(row) >= 2 and all(a.r <= b.x + 0.01 and min(a.b, b.b) - max(a.y, b.y) > 0.5 * min(a.h, b.h)
                             for a, b in zip(row, row[1:])):
        for f in row:
            head = next((s for s in subheads if _h_overlap(s, f) >= 0.6 and f.y - 0.05 <= s.y <= f.y + 0.03
                         and s not in inside_of[id(f)]), None)
            panels.append((head, sorted(inside_of[id(f)], key=lambda t: (round(t.y, 3), t.x))))
        taken = {id(t) for _, ts in panels for t in ts} | {id(h) for h, _ in panels if h}
        subheads = [s for s in subheads if id(s) not in taken]
        bodies = [b for b in bodies if id(b) not in taken]
        notes = [n for n in notes if id(n) not in taken]

    # figure: gambar kecil (2 kolom) dulu per kolom atas->bawah, lalu gambar lebar (colspan)
    figures.sort(key=lambda f: (f[0].w >= WIDE_MIN_W, round(f[0].x, 1), f[0].y))

    return dict(title=title,
                subheads=sorted(subheads, key=lambda b: (b.y, b.x)),
                columns=columns, panels=panels,
                bodies=sorted(bodies, key=lambda b: (round(b.y, 2), b.x)),
                figures=figures, tables=tables, notes=notes)


def _body_blocks(box: Box, h3_labels: bool) -> list:
    out = []
    for p in box.paras:
        t = p.text
        if h3_labels and t.isupper() and len(t) < 40 and not p.bullet:
            out.append(Block("heading", 3, p.runs))   # "KESIMPULAN" / "ARAHAN" di dalam kolom
        elif p.bullet:
            out.append(Block("bullet", p.level, p.runs, numbered=p.numbered, num_fmt=p.num_fmt))
        else:
            out.append(Block("para", p.level, p.runs))   # level PPT disimpan untuk penomoran manual
    return out


def slide_blocks(info: dict, crop: Callable[[Box], Path]) -> list:
    blocks = []
    if info["title"]:
        blocks.append(Block("heading", 1, info["title"].runs))
    for s in info["subheads"]:
        blocks.append(Block("heading", 2, s.runs))
    for head, col in info["columns"]:
        if head:
            blocks.append(Block("heading", 2, head.runs))
        blocks += _body_blocks(col, h3_labels=True)
    for b in info["bodies"]:
        blocks += _body_blocks(b, h3_labels=False)
    for head, items in info.get("panels", []):
        if head:
            blocks.append(Block("heading", 2, head.runs))
        for t in items:
            # sub-judul di dalam panel: label kapital, atau bilah berwarna pendek satu baris ("Terkait Ketentuan")
            if _is_label(t) or (t.filled and len(t.text) <= 40 and len(t.paras) == 1):
                blocks.append(Block("heading", 3, t.runs))
            else:
                blocks += _body_blocks(t, h3_labels=False)
    # gambar dan tabel diurutkan menurut posisi atasnya di slide (mis. legenda di bawah tabel tetap di bawah)
    placed = []
    if info["figures"]:
        rows = []
        for pic, cap in info["figures"]:
            img = crop(pic)
            if img:
                rows.append({"img": img, "wide": pic.w >= WIDE_MIN_W, "caption": cap.runs if cap else []})
            elif pic.rows:
                # tabel lebar tanpa render (PowerPoint tidak tersedia): tetap ditulis sebagai tabel
                placed.append((pic.y, Block("table", rows=pic.rows)))
        if rows:
            placed.append((min(p.y for p, _ in info["figures"]), Block("figures", rows=rows)))
    for t in info["tables"]:
        placed.append((t.y, Block("table", rows=t.rows, col_widths=t.col_widths)))
    blocks += [b for _, b in sorted(placed, key=lambda x: x[0])]
    for n in info["notes"]:
        for p in n.paras:
            blocks.append(Block("note", runs=p.runs))
    return _continue_manual_numbers(blocks)


# --------------------------------------------------------------------------- tanda "perlu dicek"
CHECK_IMAGE_SHARE = 0.4     # >= 40% area slide masuk sebagai diagram/tabel-gambar -> teksnya tidak bisa diedit
CHECK_SHORT_PARAS = 8       # sebanyak ini potongan teks pendek di luar list -> kemungkinan sisa diagram


def slide_flags(info: dict, blocks: list) -> list:
    """Tanda otomatis untuk slide yang hasilnya sebaiknya dicek manual. Tidak mengubah hasil konversi.
    Mengembalikan [{"code", "msg"}]."""
    flags = []
    units = [p for p, _ in info["figures"] if p.name in ("diagram", "grid-image") or p.rows]
    share = sum(min(p.w, 1) * min(p.h, 1) for p in units)
    if share >= CHECK_IMAGE_SHARE:
        flags.append({"code": "image", "msg": "Sebagian besar isi slide dimasukkan sebagai gambar (diagram/tabel), "
                                               "jadi teks di dalamnya tidak bisa diedit di CKEditor."})
    if any(p.name == "grid-image" or p.rows for p in units):
        flags.append({"code": "table_image", "msg": "Tabel dimasukkan sebagai gambar karena terlalu lebar atau "
                                                     "berisi penanda progres. Angka di dalamnya tidak bisa diedit."})
    short = [b for b in blocks if b.type == "para" and len("".join(r[0] for r in b.runs).strip()) < 40]
    if len(short) >= CHECK_SHORT_PARAS:
        flags.append({"code": "fragments", "msg": f"Ada {len(short)} potongan teks pendek di luar daftar; "
                                                   "kemungkinan bagian dari diagram. Cek urutan dan kelengkapannya."})
    figs = [r for b in blocks if b.type == "figures" for r in b.rows]
    if len(figs) >= 2 and any(not r["caption"] for r in figs):
        n = sum(1 for r in figs if not r["caption"])
        flags.append({"code": "caption", "msg": f"{n} dari {len(figs)} gambar tidak punya judul/caption. "
                                                 "Cek apakah judulnya tertukar atau ikut masuk ke gambar."})
    content = [b for b in blocks if not (b.type == "heading" and b.level == 1)]
    if not content:
        flags.append({"code": "empty", "msg": "Slide hanya menghasilkan judul (mungkin slide pembatas). "
                                               "Pastikan memang tidak ada isi yang terlewat."})
    return flags


# --------------------------------------------------------------------------- 3. render + crop
_render_lock = threading.Lock()   # PowerPoint COM: satu render pada satu waktu

_PS_RENDER = r"""
$ErrorActionPreference = 'Stop'
$app = New-Object -ComObject PowerPoint.Application
try {
  $pres = $app.Presentations.Open('{src}', $true, $false, $false)
  try { foreach ($s in $pres.Slides) { $s.Export(('{out}\slide' + $s.SlideIndex + '.png'), 'PNG', {w}, {h}) } }
  finally { $pres.Close() }
} finally { if ($app.Presentations.Count -eq 0) { $app.Quit() } }
"""


def render_slides(pptx: Path, out_dir: Path, width_px: int = 2667) -> bool:
    """Render tiap slide ke out_dir/slideN.png lewat PowerPoint. False kalau PowerPoint tidak tersedia."""
    ps = shutil.which("powershell") or shutil.which("pwsh")
    if not ps:
        return False
    prs = Presentation(str(pptx))
    height_px = round(width_px * prs.slide_height / prs.slide_width)
    out_dir.mkdir(parents=True, exist_ok=True)
    script = (_PS_RENDER.replace("{src}", str(pptx.resolve()).replace("'", "''"))
              .replace("{out}", str(out_dir.resolve()).replace("'", "''"))
              .replace("{w}", str(width_px)).replace("{h}", str(height_px)))
    with _render_lock:
        try:
            subprocess.run([ps, "-NoProfile", "-NonInteractive", "-Command", script],
                           check=True, capture_output=True, timeout=900)
        except (subprocess.SubprocessError, OSError) as e:
            print(f"  [!] Render PowerPoint gagal, pakai gambar asli dari PPTX: {e}")
            return False
    return (out_dir / "slide1.png").exists()


def load_render(render_png: Optional[Path]):
    return Image.open(render_png).convert("RGB") if render_png and Path(render_png).exists() else None


JPEG_QUALITY = 88   # crop render disimpan JPEG: ukuran DOCX/HTML jauh lebih kecil dari PNG
MAX_IMAGE_PX = 1800  # lebar maksimum crop (~285 dpi di lebar teks A4), cukup tajam untuk teks diagram


def save_box_image(b: Box, path: Path, render=None) -> Optional[Path]:
    """Simpan gambar untuk unit b: crop dari render slide (JPEG), atau tanpa render gambar terbesar
    di unit ini (PNG; WMF/EMF butuh Windows untuk dikonversi). Mengembalikan path akhir."""
    path.parent.mkdir(parents=True, exist_ok=True)
    if render is not None:
        RW, RH = render.size
        pad = 0.002
        box = (int(max(b.x - pad, 0) * RW), int(max(b.y - pad, 0) * RH),
               int(min(b.r + pad, 1) * RW), int(min(b.b + pad, 1) * RH))
        out = path.with_suffix(".jpg")
        img = render.crop(box)
        if img.width > MAX_IMAGE_PX:
            img = img.resize((MAX_IMAGE_PX, round(img.height * MAX_IMAGE_PX / img.width)), Image.LANCZOS)
        img.save(out, quality=JPEG_QUALITY, optimize=True)
        return out
    if not b.images:
        return None
    blob, ext, _ = max(b.images, key=lambda i: i[2])
    raw = path.with_suffix("." + ext)
    raw.write_bytes(blob)
    if raw == path:
        return path               # sudah PNG
    try:
        Image.open(raw).convert("RGB").save(path)
        raw.unlink()
        return path
    except Exception:
        return raw if ext.lower() in ("png", "jpg", "jpeg", "gif") else None


def make_cropper(render_png: Optional[Path], media_dir: Path, slide_no: int):
    render = load_render(render_png)
    counter = {"n": 0}

    def crop(b: Box) -> Optional[Path]:
        counter["n"] += 1
        return save_box_image(b, media_dir / f"s{slide_no:02d}_{counter['n']}.png", render)

    return crop


# --------------------------------------------------------------------------- 4a. DOCX
class DocxWriter:
    def __init__(self, template: Path):
        self.doc = Document(str(template))
        body = self.doc.element.body
        self._numbering = self._find_abstract_nums()
        self._list = {}           # list yang sedang berjalan: {(bernomor, level): numId}
        for el in list(body):
            if el.tag != qn("w:sectPr"):
                body.remove(el)
        sec = self.doc.sections[0]
        self.text_w = int(sec.page_width - sec.left_margin - sec.right_margin)

    @staticmethod
    def _runs(par, runs):
        for t, b, i in runs:
            r = par.add_run(t)
            r.bold = True if b else None
            r.italic = True if i else None

    def _find_abstract_nums(self) -> dict:
        """abstractNum bullet & desimal dari template (example.docx punya keduanya)."""
        try:
            numbering = self.doc.part.numbering_part.element
        except Exception:
            return {}
        found = {}
        for an in numbering.findall(qn("w:abstractNum")):
            lvl = an.find(qn("w:lvl"))
            fmt = lvl.find(qn("w:numFmt")) if lvl is not None else None
            kind = fmt.get(qn("w:val")) if fmt is not None else None
            if kind in ("bullet", "decimal"):
                found.setdefault(kind, an.get(qn("w:abstractNumId")))
        return found

    def _abstract_for(self, fmt: str) -> Optional[str]:
        """abstractNum untuk format nomor tertentu. Template cuma punya decimal & bullet, jadi format
        lain (lowerLetter, lowerRoman, ...) dibuat dengan menyalin abstractNum decimal."""
        if fmt in self._numbering:
            return self._numbering[fmt]
        base = self._numbering.get("decimal")
        if base is None:
            return None
        numbering = self.doc.part.numbering_part.element
        src = next(a for a in numbering.findall(qn("w:abstractNum")) if a.get(qn("w:abstractNumId")) == base)
        clone = copy.deepcopy(src)
        new_id = str(max(int(a.get(qn("w:abstractNumId"))) for a in numbering.findall(qn("w:abstractNum"))) + 1)
        clone.set(qn("w:abstractNumId"), new_id)
        for tag in ("w:nsid", "w:tmpl"):
            for e in clone.findall(qn(tag)):
                clone.remove(e)
        for lvl in clone.findall(qn("w:lvl")):
            nf = lvl.find(qn("w:numFmt"))
            if nf is not None:
                nf.set(qn("w:val"), fmt)
        numbering.findall(qn("w:abstractNum"))[-1].addnext(clone)   # abstractNum harus sebelum w:num
        self._numbering[fmt] = new_id
        return new_id

    def _new_num(self, abstract_id: str, level: int) -> str:
        """w:num baru yang mulai dari 1 -> tiap list di dokumen punya penomoran sendiri."""
        numbering = self.doc.part.numbering_part.element
        new_id = str(max((int(n.get(qn("w:numId"))) for n in numbering.findall(qn("w:num"))), default=0) + 1)
        num = OxmlElement("w:num")
        num.set(qn("w:numId"), new_id)
        a = OxmlElement("w:abstractNumId")
        a.set(qn("w:val"), abstract_id)
        num.append(a)
        ov = OxmlElement("w:lvlOverride")
        ov.set(qn("w:ilvl"), str(level))
        start = OxmlElement("w:startOverride")
        start.set(qn("w:val"), "1")
        ov.append(start)
        num.append(ov)
        numbering.append(num)
        return new_id

    def write(self, blocks: list):
        for bl in blocks:
            if bl.type != "bullet":
                self._list = {}   # list terputus -> list berikutnya mulai dari 1 lagi
            getattr(self, "_" + bl.type)(bl)
        self._list = {}
        self.doc.add_paragraph()   # jeda antar slide

    def _heading(self, bl):
        p = self.doc.add_paragraph(style=f"Heading {bl.level}")
        # tebal/tipis heading mengikuti style template, bukan bold dari PPT
        self._runs(p, [(t, False, i) for t, _, i in _strip_runs(bl.runs)])

    def _para(self, bl):
        self._runs(self.doc.add_paragraph(), _strip_runs(bl.runs))

    def _note(self, bl):
        p = self.doc.add_paragraph()
        self._runs(p, _strip_runs(bl.runs))
        for r in p.runs:
            r.font.size = Pt(8)

    def _bullet(self, bl):
        p = self.doc.add_paragraph()
        level = min(bl.level, 8)
        kind = bl.num_fmt if bl.numbered else "bullet"
        abstract = self._abstract_for(kind) if bl.numbered else self._numbering.get("bullet")
        if abstract is None:
            p.style = "List Number" if bl.numbered else "List Bullet"
        else:
            # sub-list di bawah item ini selesai saat kembali ke level ini
            for key in [k for k in self._list if k[1] > level]:
                del self._list[key]
            key = (kind, level)
            if key not in self._list:
                self._list[key] = self._new_num(abstract, level)
            numPr = OxmlElement("w:numPr")
            ilvl = OxmlElement("w:ilvl")
            ilvl.set(qn("w:val"), str(level))
            numId = OxmlElement("w:numId")
            numId.set(qn("w:val"), self._list[key])
            numPr.append(ilvl)
            numPr.append(numId)
            p._p.get_or_add_pPr().append(numPr)
        self._runs(p, _strip_runs(bl.runs))

    def _new_table(self, cols: int, widths: list):
        t = self.doc.add_table(rows=0, cols=cols)
        t.style = "Table Grid"
        t.alignment = WD_TABLE_ALIGNMENT.CENTER
        t.autofit = False
        for col, w in zip(t.columns, widths):
            col.width = Emu(w)
        return t

    def _figures(self, bl):
        wl = int(self.text_w * FIG_COL_SPLIT[0])
        wr = self.text_w - wl
        margin = 2 * 72000    # padding sel kiri+kanan
        t = self._new_table(2, [wl, wr])
        for row in bl.rows:
            cells = t.add_row().cells
            cells[0].width, cells[1].width = Emu(wl), Emu(wr)
            if row["wide"]:
                m = cells[0].merge(cells[1])
                m.paragraphs[0].add_run().add_picture(str(row["img"]), width=Emu(self.text_w - margin))
                if row["caption"]:
                    self._runs(m.add_paragraph(), _strip_runs(row["caption"]))
            else:
                cells[0].paragraphs[0].add_run().add_picture(str(row["img"]), width=Emu(wl - margin))
                self._runs(cells[1].paragraphs[0], _strip_runs(row["caption"]))

    def _table(self, bl):
        ncols = max((len(r) for r in bl.rows), default=0)
        if not ncols:
            return
        widths = _scale_widths(bl.col_widths, ncols, self.text_w)
        t = self._new_table(ncols, widths)
        small = Pt(8) if ncols > 4 else Pt(9)
        for i, r in enumerate(bl.rows):
            cells = t.add_row().cells
            for c, val, w in zip(cells, r, widths):
                c.width = Emu(w)
                run = c.paragraphs[0].add_run(val)
                run.font.size = small
                run.bold = True if i == 0 else None    # baris pertama = header

    def save(self, path: Path):
        self.doc.save(str(path))


def _scale_widths(rel: list, ncols: int, total: int) -> list:
    """Lebar relatif kolom -> lebar absolut yang jumlahnya `total`; rata kalau tidak diketahui."""
    if len(rel) != ncols or sum(rel) <= 0:
        rel = [1] * ncols
    widths = [int(total * w / sum(rel)) for w in rel]
    widths[-1] += total - sum(widths)
    return widths


def _strip_runs(runs: list) -> list:
    """Buang spasi di awal/akhir paragraf dan karakter zero-width dari PPT."""
    runs = [(re.sub(r" {2,}", " ", re.sub(r"[​﻿]", "", t)), b, i) for t, b, i in runs]
    runs = [r for r in runs if r[0]]
    # spasi ganda di sambungan run dan spasi sebelum tanda baca ("11,9% ." -> "11,9%.")
    for k in range(len(runs)):
        t = re.sub(r" +([,.;:)%])", r"\1", runs[k][0])
        if k + 1 < len(runs) and t.endswith(" ") and re.match(r"[ ,.;:)%]", runs[k + 1][0]):
            t = t.rstrip()
        runs[k] = (t,) + tuple(runs[k][1:])
    runs = [r for r in runs if r[0]]
    if runs:
        runs[0] = (runs[0][0].lstrip(),) + tuple(runs[0][1:])
        runs[-1] = (runs[-1][0].rstrip(),) + tuple(runs[-1][1:])
    return [r for r in runs if r[0]]


# --------------------------------------------------------------------------- 4b. HTML (CKEditor)
def _runs_html(runs: list) -> str:
    out = []
    for t, b, i in _strip_runs(runs):
        s = html.escape(t)
        if i:
            s = f"<i>{s}</i>"
        if b:
            s = f"<strong>{s}</strong>"
        out.append(s)
    return "".join(out)


def _img_src(path: Path, embed: bool, rel_to: Optional[Path]) -> str:
    if embed:
        ext = path.suffix.lower().lstrip(".")
        mime = "image/" + {"jpg": "jpeg"}.get(ext, ext)
        return f"data:{mime};base64," + base64.b64encode(path.read_bytes()).decode()
    return path.relative_to(rel_to).as_posix() if rel_to else path.as_posix()


_HTML_OL_TYPE = {"lowerLetter": "a", "upperLetter": "A", "lowerRoman": "i", "upperRoman": "I"}


def blocks_to_html(slides: list, embed_images: bool = True, rel_to: Optional[Path] = None,
                   img_url: Optional[Callable[[Path], str]] = None) -> str:
    """slides: [[Block]] -> fragmen HTML yang bersih untuk CKEditor (tanpa class/CSS khusus).
    img_url: kalau diisi, menentukan src gambar (mis. URL server) dan menggantikan embed/rel_to."""
    out = []
    for blocks in slides:
        list_stack = []           # tag pembuka list per level: "ul" / "ol" / 'ol type="a"' ...

        def close(level=-1):
            while len(list_stack) > level + 1:
                out.append(f"</li></{list_stack.pop().split()[0]}>")

        for bl in blocks:
            if bl.type == "bullet":
                lvl = min(bl.level, 5)
                tag = "ul" if not bl.numbered else (
                    f'ol type="{_HTML_OL_TYPE[bl.num_fmt]}"' if bl.num_fmt in _HTML_OL_TYPE else "ol")
                if len(list_stack) > lvl + 1:
                    close(lvl)
                if len(list_stack) == lvl + 1 and list_stack[lvl] != tag:
                    close(lvl - 1)        # jenis list berganti di level yang sama -> list baru
                if len(list_stack) == lvl + 1:
                    out.append("</li>")
                while len(list_stack) < lvl + 1:
                    t = tag if len(list_stack) == lvl else "ul"
                    out.append(f"<{t}>")
                    list_stack.append(t)
                out.append(f"<li>{_runs_html(bl.runs)}")
                continue
            close()
            if bl.type == "heading":
                out.append(f"<h{bl.level}>{_runs_html(bl.runs)}</h{bl.level}>")
            elif bl.type == "para":
                out.append(f"<p>{_runs_html(bl.runs)}</p>")
            elif bl.type == "note":
                out.append(f"<p><small>{_runs_html(bl.runs)}</small></p>")
            elif bl.type == "figures":
                rows = []
                for r in bl.rows:
                    src = img_url(r["img"]) if img_url else _img_src(r["img"], embed_images, rel_to)
                    img = f'<img src="{html.escape(src)}" style="max-width:100%;height:auto">'
                    cap = _runs_html(r["caption"])
                    if r["wide"]:
                        rows.append(f'<tr><td colspan="2">{img}' + (f"<p>{cap}</p>" if cap else "") + "</td></tr>")
                    else:
                        rows.append(f'<tr><td style="width:{FIG_COL_SPLIT[0]:.0%}">{img}</td>'
                                    f'<td style="width:{FIG_COL_SPLIT[1]:.0%}">{cap}</td></tr>')
                out.append('<table border="1" style="border-collapse:collapse;width:100%"><tbody>'
                           + "".join(rows) + "</tbody></table>")
            elif bl.type == "table":
                ncols = max((len(r) for r in bl.rows), default=0)
                pct = [w / 100 for w in _scale_widths(bl.col_widths, ncols, 10000)]

                def cell(c, i, k):
                    s = html.escape(c).replace("\n", "<br>")
                    s = f"<strong>{s}</strong>" if i == 0 and s else s
                    return f'<td style="width:{pct[k]:.0f}%">{s}</td>' if i == 0 and k < len(pct) else f"<td>{s}</td>"
                rows = "".join("<tr>" + "".join(cell(c, i, k) for k, c in enumerate(r)) + "</tr>"
                               for i, r in enumerate(bl.rows))
                out.append(f'<table border="1" style="border-collapse:collapse;width:100%"><tbody>{rows}</tbody></table>')
        close()
    return "\n".join(out)


def html_document(fragment: str, title: str) -> str:
    return (f'<!DOCTYPE html>\n<html lang="id"><head><meta charset="UTF-8"><title>{html.escape(title)}</title>'
            '<style>body{font-family:Arial,sans-serif;max-width:900px;margin:20px auto;line-height:1.5}'
            'td{vertical-align:top;padding:6px}h1,h2,h3{color:#0F4761}</style></head>\n<body>\n'
            f"{fragment}\n</body></html>\n")


# --------------------------------------------------------------------------- 5. LLM (opsional)
LLM_PROMPT = """You tidy short texts extracted from presentation slides (Indonesian business/economics).
For each item: fix obvious typos and broken spacing, and merge words split by line breaks.
Strict rules:
- Keep the ORIGINAL LANGUAGE and meaning. Do not translate, summarize, shorten or add content.
- Keep every number, unit, abbreviation and term exactly (e.g. "yg", "dg", "tw", "yoy", "bps").
- Return ONLY a JSON object mapping each id to its tidied text, with the same ids. No markdown.

ITEMS:
{items}
"""


def tidy_text_with_llm(slides: list, provider: str, model: str, progress: ProgressFn = _noop) -> dict:
    """Rapikan teks paragraf/bullet/caption per slide. Hanya paragraf berformat seragam yang dikirim
    (supaya bold/italic per kata tidak hilang). Hasil yang menyimpang jauh dari aslinya ditolak."""
    from converter import _call_llm   # import lambat: converter memuat Docling/torch

    stats = {"llm_items": 0, "llm_changed": 0, "llm_rejected": 0, "llm_errors": 0}
    for si, blocks in enumerate(slides, 1):
        progress(si / max(len(slides), 1), f"LLM merapikan teks slide {si} dari {len(slides)}")
        targets = []      # (holder, key) -> runs
        for bl in blocks:
            if bl.type in ("para", "bullet", "note", "heading"):
                targets.append((bl, None))
            elif bl.type == "figures":
                targets += [(r, "caption") for r in bl.rows if r["caption"]]
        items = {}
        for k, (holder, key) in enumerate(targets):
            runs = holder.runs if key is None else holder[key]
            fmt = {(b, i) for t, b, i in runs if t.strip()}
            text = "".join(t for t, _, _ in runs).strip()
            if len(fmt) == 1 and len(text) > 3:
                items[str(k)] = text
        if not items:
            continue
        stats["llm_items"] += len(items)
        try:
            raw = _call_llm(LLM_PROMPT.format(items=json.dumps(items, ensure_ascii=False, indent=0)),
                            provider, model) or ""
            raw = re.sub(r"^```(?:json)?\s*|\s*```$", "", raw.strip())
            result = json.loads(raw)
        except Exception as e:
            print(f"  [!] LLM slide {si} dilewati: {e}")
            stats["llm_errors"] += 1
            continue
        for k, new in result.items():
            if k not in items or not isinstance(new, str):
                continue
            old = items[k]
            ratio = len(new.strip()) / max(len(old), 1)
            same_numbers = re.findall(r"\d+(?:[.,]\d+)?", old) == re.findall(r"\d+(?:[.,]\d+)?", new)
            if not (0.85 <= ratio <= 1.15 and same_numbers):
                stats["llm_rejected"] += 1
                continue
            if new.strip() != old:
                holder, key = targets[int(k)]
                runs = holder.runs if key is None else holder[key]
                b, i = next((b, i) for t, b, i in runs if t.strip())
                if key is None:
                    holder.runs = [(new.strip(), b, i)]
                else:
                    holder[key] = [(new.strip(), b, i)]
                stats["llm_changed"] += 1
    return stats


# --------------------------------------------------------------------------- orkestrasi
def convert_pptx(
    pptx_path,
    docx_path,
    html_path=None,
    template=DEFAULT_TEMPLATE,
    use_llm: bool = False,
    provider: str = "gemini",
    model: str = "gemini-3.8-flash",
    render: bool = True,
    work_dir=None,
    progress: ProgressFn = _noop,
    include_hidden: bool = False,
) -> dict:
    """include_hidden: ikut konversi slide yang di-hide di PowerPoint (default dilewati).
    Selain DOCX/HTML, menulis work_dir/review.json (per slide: render + HTML hasil) untuk halaman review."""
    pptx_path, docx_path = Path(pptx_path), Path(docx_path)
    work = Path(work_dir) if work_dir else docx_path.parent / (docx_path.stem + "_build")
    render_dir, media_dir = work / "slides", work / "media"
    work.mkdir(parents=True, exist_ok=True)

    progress(0.02, "Merender slide dengan PowerPoint")
    rendered = render_slides(pptx_path, render_dir) if render else False

    progress(0.35, "Menganalisa layout slide")
    prs = Presentation(str(pptx_path))
    W, H = prs.slide_width, prs.slide_height
    slides, numbers, skipped, n_fig = [], [], [], 0
    for n, slide in enumerate(prs.slides, 1):
        if is_hidden(slide) and not include_hidden:
            skipped.append(n)
            continue
        info = analyse(slide, W, H)
        crop = make_cropper(render_dir / f"slide{n}.png" if rendered else None, media_dir, n)
        blocks = slide_blocks(info, crop)
        n_fig += sum(len(b.rows) for b in blocks if b.type == "figures")
        slides.append(blocks)
        numbers.append(n)

    stats = {"slides": len(slides), "images": n_fig, "rendered": rendered, "hidden_skipped": skipped}
    if use_llm:
        stats.update(tidy_text_with_llm(slides, provider, model,
                                        lambda f, m: progress(0.45 + 0.35 * f, m)))

    progress(0.85, "Menulis dokumen Word")
    w = DocxWriter(Path(template))
    for blocks in slides:
        w.write(blocks)
    w.save(docx_path)
    stats["docx"] = str(docx_path)

    if html_path:
        progress(0.95, "Menulis HTML untuk CKEditor")
        Path(html_path).write_text(html_document(blocks_to_html(slides), pptx_path.stem), encoding="utf-8")
        stats["html"] = str(html_path)

    # bahan halaman review: per slide render asli (pratinjau JPEG kecil) + HTML hasil
    if rendered:
        for n in numbers:
            src = render_dir / f"slide{n}.png"
            if src.exists():
                im = Image.open(src).convert("RGB")
                im.thumbnail((1400, 1400))
                im.save(render_dir / f"preview{n}.jpg", quality=80)
    review = {"source": pptx_path.name, "rendered": rendered, "skipped": skipped, "slides": [
        {"n": n, "render": f"slides/preview{n}.jpg" if rendered else None,
         "html": blocks_to_html([blocks], img_url=lambda p: f"media/{Path(p).name}")}
        for n, blocks in zip(numbers, slides)]}
    (work / "review.json").write_text(json.dumps(review, ensure_ascii=False), encoding="utf-8")
    stats["review"] = str(work / "review.json")

    progress(1.0, "Selesai")
    return stats


def is_hidden(slide) -> bool:
    """Slide yang di-hide di PowerPoint (Hide Slide) punya atribut show="0"."""
    return slide._element.get("show") in ("0", "false")


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="PPTX -> DOCX/HTML berbasis geometri (tanpa LLM)")
    ap.add_argument("pptx")
    ap.add_argument("-o", "--output", default="Report_Output.docx")
    ap.add_argument("--html", default=None, help="tulis juga HTML untuk CKEditor")
    ap.add_argument("--template", default=str(DEFAULT_TEMPLATE))
    ap.add_argument("--no-render", action="store_true", help="jangan pakai PowerPoint, ambil gambar asli")
    ap.add_argument("--llm", choices=["gemini", "ollama"], default=None, help="opsional: rapikan teks dengan LLM")
    ap.add_argument("--model", default="gemini-3.8-flash")
    ap.add_argument("--include-hidden", action="store_true", help="ikut konversi slide yang di-hide")
    a = ap.parse_args()
    print(convert_pptx(a.pptx, a.output, a.html, a.template, use_llm=bool(a.llm),
                       provider=a.llm or "gemini", model=a.model, render=not a.no_render,
                       progress=lambda f, m: print(f"[{f:4.0%}] {m}"), include_hidden=a.include_hidden))
