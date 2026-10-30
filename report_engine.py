"""PPTX -> DOCX berformat laporan (contoh: docs/test3.docx) lewat *rencana layout* per slide.

Alur:
  1. extract   semua shape -> elemen ber-id e1, e2, ... (layout_engine.collect: koordinat absolut, group
               diratakan, elemen di luar slide dibuang).
  2. plan      layout_engine.analyse() (aturan geometri) -> rencana: daftar blok yang hanya merujuk id
               elemen (heading / text / table / figure / note) + daftar drop. Tiap slide diberi tipe
               (cover, divider, closing, text, charts, columns, dense) dan tanda bila hasil aturan meragukan.
               Slide dense yang oleh aturan dipecah jadi banyak potongan pendek (infografis) ditulis sebagai
               judul + pesan kunci + satu gambar (tipe infographic; perlu render PowerPoint, tanpa LLM).
  3. route     planner "auto": slide dense atau bertanda dikirim ke LLM (llm_planner) bersama render slide;
               LLM mengembalikan rencana dengan skema yang sama. LLM tidak pernah menulis teks, jadi angka
               tidak bisa berubah. Rencana LLM divalidasi (id ada, tidak dobel, teks penting tidak hilang);
               gagal -> rencana aturan dipakai. Rencana LLM disimpan di cache per isi slide.
  4. write     rencana -> DOCX (report_writer), dan opsional HTML untuk CKEditor dengan format yang sama.
               Format selalu sama, berapapun sumber rencananya.

Rencana semua slide ditulis ke <work>/plans.json (untuk dicek dan untuk evaluate.py), dan per slide render
+ HTML hasil ke <work>/review.json (halaman /review, sama seperti layout_engine).

CLI:
    python report_engine.py docs/test3.pptx -o work/test3_report.docx
    python report_engine.py docs/test3.pptx -o work/test3_report.docx --html work/test3_report.html
    python report_engine.py docs/test2.pptx -o work/test2_report.docx --planner rules   # tanpa LLM
    python report_engine.py docs/test2.pptx -o work/test2_cached.docx --planner cached # rencana LLM tersimpan saja
    python report_engine.py docs/test3.pptx -o work/test3_llm.docx --planner llm        # semua slide ke LLM
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import time
from collections import Counter
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass, field
from pathlib import Path
from typing import Callable, Optional

from lxml import etree
from PIL import Image
from pptx import Presentation

import bedrock_llm
import layout_engine as le
from report_writer import DEFAULT_TEMPLATE, DOC_TITLE, HtmlReportWriter, ReportWriter, Tee

HERE = Path(__file__).resolve().parent
DEFAULT_CACHE = HERE / "work" / "plan_cache"
DEFAULT_MODEL = bedrock_llm.DEFAULT_MODEL
PLANNER_VERSION = "4"         # naikkan kalau extract/prompt berubah supaya cache lama tidak dipakai

# label template yang selalu dibuang (dibandingkan dalam huruf kapital)
BOILERPLATE = {"HASIL PEMBAHASAN DEWAN GUBERNUR"}
BOILERPLATE_MIN_SLIDES = 3    # label sub-judul >= 3 kata yang sama persis di >= sekian slide = label template
BOILERPLATE_MIN_WORDS = 3
CLOSING_RE = re.compile(r"^\s*(terima\s*kasih|thank\s*you)\W*$", re.I)
DENSE_MIN_TEXTS = 25          # lebih banyak teks / shape dari ini (atau ada diagram/tabel-gambar) = dense
DENSE_MIN_SHAPES = 25
DIVIDER_MAX_TEXTS = 4
DIVIDER_MAX_CHARS = 160
LOST_TEXT_CHARS = 40          # teks sepanjang ini yang dibuang aturan = tanda
FRAGMENT_CHARS = 40
FRAGMENT_MIN = 8              # sebanyak ini paragraf pendek di luar label = kemungkinan sisa diagram
COLOUR_TABLE_CELLS = 3        # tabel dengan >= sekian sel kosong berwarna (Gantt) = makna di warna
MISSING_TEXT_CHARS = 30       # rencana LLM: teks sepanjang ini yang tidak dipakai dan tidak di-drop = ditolak
ROW_TOL = 0.02                # caption yang selisih tingginya sekecil ini = satu baris (urut kiri -> kanan)
ICON_NEAR = 0.02              # ikon sejauh ini dari judul kolom dianggap menempel
ICON_MAX_PX = 256             # ikon asli (bisa ratusan KB) diperkecil ke ukuran ini
WIDE_MIN_TEXTS = 5            # gambar berisi >= sekian teks / sel tabel (diagram, Gantt) ditulis selebar halaman
WIDE_MIN_W = 0.5
INFOGRAPHIC_MIN_PIECES = 14   # slide dense yang oleh aturan dipecah jadi sebanyak ini potongan (paragraf pendek,
INFOGRAPHIC_SHORT_SHARE = 0.6 # tabel lepas dihitung 2) dan sebagian besar teksnya pendek = infografis -> satu gambar
NO_LLM_KINDS = ("cover", "divider", "closing", "infographic")
PLANNERS = ("rules", "cached", "auto", "llm")

ProgressFn = Callable[[float, str], None]

# tanda slide -> (penjelasan untuk pengguna, saran prompt AI); dipakai komentar review DOCX dan halaman /dwp
FLAG_INFO = {
    "dense": ("Slide padat (banyak teks dan objek); urutan atau pengelompokan isi bisa keliru.",
              "Kelompokkan isi per panel/kolom dari kiri ke kanan: judul panel jadi heading, teksnya di bawahnya. "
              "Grafik atau diagram beserta label kecilnya jadi satu gambar dengan caption-nya."),
    "no_title": ("Judul slide tidak terdeteksi.",
                 "Jadikan teks judul di bagian atas slide sebagai heading level 1."),
    "uncaptioned": ("Ada beberapa gambar/grafik tanpa keterangan.",
                    "Pasangkan setiap grafik atau gambar dengan label/bar judul tepat di atasnya sebagai caption."),
    "dropped_text": ("Ada teks panjang yang tidak ikut ke dokumen.",
                     "Pastikan semua kalimat di slide tetap muncul sebagai teks; jangan buang teks yang panjang."),
    "fragments": ("Banyak potongan teks pendek, kemungkinan label diagram yang tercecer.",
                  "Potongan teks pendek ini adalah label diagram: jadikan diagram beserta labelnya satu gambar."),
    "duplicate_heading": ("Ada heading yang muncul dua kali.",
                          "Tulis setiap heading sekali saja; buang heading yang dobel."),
    "colour_table": ("Ada tabel yang maknanya di warna sel (mis. Gantt / timeline).",
                     "Tabel ini bermakna lewat warna sel (Gantt/timeline): jadikan satu gambar selebar halaman, "
                     "bukan tabel teks."),
    # tanda dari LLM pada mode perbaikan otomatis (tanpa saran prompt)
    "llm_failed": ("LLM gagal menyusun ulang slide ini saat konversi; hasil aturan dipakai.", ""),
    "llm_fixed": ("Jawaban pertama LLM ditolak validasi; hasil perbaikannya dipakai.", ""),
}
REVIEW_QUOTES = 3             # komentar review: paling banyak sekian teks yang dibuang dikutip
REVIEW_QUOTE_CHARS = 100


def _noop(_f: float, _m: str) -> None:
    pass


@dataclass
class SlidePlan:
    n: int
    els: dict                       # id -> layout_engine.Box (hanya elemen di dalam slide)
    info: dict                      # hasil layout_engine.analyse
    kind: str = "text"
    rules_plan: dict = field(default_factory=dict)
    plan: dict = field(default_factory=dict)    # {"blocks": [...], "drop": [...]}
    source: str = "rules"           # rules | llm | cache
    flags: list = field(default_factory=list)
    errors: list = field(default_factory=list)  # alasan rencana LLM ditolak / gagal
    key: str = ""                   # kunci cache (hash isi slide)


# --------------------------------------------------------------------------- teks & geometri
def para_text(p) -> str:
    return re.sub(r"\s+", " ", "".join(r[0] for r in le._strip_runs(p.runs))).strip()


def box_text(b) -> str:
    return " ".join(t for t in (para_text(p) for p in b.paras) if t)


def is_label_para(p, text: str) -> bool:
    """Paragraf label di dalam kotak teks ("KESIMPULAN", "ARAHAN"): pendek, kapital, bukan bullet."""
    letters = [c for c in text if c.isalpha()]
    return (not p.bullet and len(text) <= 60 and len(letters) >= 3
            and sum(c.isupper() for c in letters) / len(letters) > 0.8)


def _region_box(reg) -> le.Box:
    return le.Box("picture", *reg)


def union(boxes) -> tuple:
    x, y = max(min(b.x for b in boxes), 0.0), max(min(b.y for b in boxes), 0.0)
    r, btm = min(max(b.r for b in boxes), 1.0), min(max(b.b for b in boxes), 1.0)
    return x, y, max(r - x, 0.0), max(btm - y, 0.0)


def inside(b, reg: le.Box) -> bool:
    return le._inside(b, reg, 0.01) or (b.w * b.h > 0 and le._inter(b, reg) > 0.5 * b.w * b.h)


def fig_region(block: dict, els: dict) -> tuple:
    if block.get("box"):
        return tuple(block["box"])
    return union([els[k] for k in block["ids"] if k in els])


# --------------------------------------------------------------------------- 1. extract
def extract(slide, W: int, H: int) -> dict:
    boxes = [b for b in le.collect(slide.shapes, W, H) if le._on_slide(b)]
    return {f"e{i}": b for i, b in enumerate(boxes, 1)}


# --------------------------------------------------------------------------- 2. rencana dari aturan
def rules_plan(els: dict, info: dict) -> dict:
    ids = {id(b): k for k, b in els.items()}
    blocks, used = [], set()

    def text_block(b, kind="text", level=None):
        k = ids.get(id(b))
        if k is None or k in used:
            return
        blk = {"type": kind, "id": k}
        if level:
            blk["level"] = level
        blocks.append(blk)
        used.add(k)

    if info["title"] is not None:
        text_block(info["title"], "heading", 1)
    for s in info["subheads"]:
        text_block(s, "heading", 2)
    for head, col in info["columns"]:
        if head is not None:
            text_block(head, "heading", 2)
        text_block(col)
    for b in info["bodies"]:
        text_block(b)
    for head, items in info.get("panels", []):
        if head is not None:
            text_block(head, "heading", 2)
        for t in items:
            # sub-judul di dalam panel: label kapital, atau bilah berwarna pendek satu baris
            if le._is_label(t) or (t.filled and len(t.text) <= 40 and len(t.paras) == 1):
                text_block(t, "heading", 3)
            else:
                text_block(t)

    captions = {ids[id(c)] for _, c in info["figures"] if c is not None and id(c) in ids}
    for t in info["tables"]:
        if id(t) in ids:
            blocks.append({"type": "table", "id": ids[id(t)]})
            used.add(ids[id(t)])
        else:
            # grid yang disusun aturan dari text box: isi sel sudah jadi, anggotanya dicatat untuk validasi
            members = [k for k, b in els.items() if k not in used and k not in captions and b.kind == "text"
                       and inside(b, t)]
            blocks.append({"type": "table", "rows": t.rows, "ids": members})
            used.update(members)

    figs = []
    for pic, cap in info["figures"]:
        cap_id = ids.get(id(cap)) if cap is not None else None
        members = [k for k, b in els.items() if k not in used and k not in captions and inside(b, pic)]
        used.update(members)
        if cap_id:
            used.add(cap_id)
        figs.append({"type": "figure", "ids": members, "caption": cap_id,
                     "box": [round(v, 5) for v in (pic.x, pic.y, pic.w, pic.h)]})
    blocks += figs
    for nb in info["notes"]:
        text_block(nb, "note")
    return {"blocks": blocks, "drop": [k for k in els if k not in used]}


def sort_figures(figs: list, els: dict) -> list:
    """Urutan gambar = posisi caption (atau gambarnya): atas -> bawah, caption sebaris kiri -> kanan."""
    def anchor(f):
        if f.get("caption") in els:
            b = els[f["caption"]]
            return b.y, b.x
        x, y, _, _ = fig_region(f, els)
        return y, x

    rows, cur = [], []
    for f in sorted(figs, key=anchor):
        if cur and anchor(f)[0] - anchor(cur[0])[0] > ROW_TOL:
            rows.append(cur)
            cur = []
        cur.append(f)
    if cur:
        rows.append(cur)
    return [f for r in rows for f in sorted(r, key=lambda f: anchor(f)[1])]


def normalize(plan: dict, els: dict) -> dict:
    """Konvensi dokumen: isi (heading/teks/tabel) sesuai urutan rencana, lalu gambar menurut posisi
    caption, lalu catatan kaki."""
    blocks = plan["blocks"]
    body = [b for b in blocks if b["type"] not in ("figure", "note")]
    figs = sort_figures([b for b in blocks if b["type"] == "figure"], els)
    notes = [b for b in blocks if b["type"] == "note"]
    return {"blocks": body + figs + notes, "drop": list(plan.get("drop", []))}


# --------------------------------------------------------------------------- tipe slide & tanda
def classify(els: dict, info: dict, first: bool) -> str:
    texts = [b for b in els.values() if b.kind == "text" and box_text(b)]
    pics = [b for b in els.values() if b.kind == "picture" and b.w >= le.ICON_MAX_W]
    tables = [b for b in els.values() if b.kind == "table"]
    shapes = [b for b in els.values() if b.kind == "shape"]
    if len(texts) <= 2 and any(CLOSING_RE.match(box_text(b)) for b in texts):
        return "closing"
    if (not pics and not tables and len(texts) <= DIVIDER_MAX_TEXTS
            and sum(len(box_text(b)) for b in texts) <= DIVIDER_MAX_CHARS):
        return "cover" if first else "divider"
    if (len(texts) > DENSE_MIN_TEXTS or len(shapes) > DENSE_MIN_SHAPES
            or any(p.name in ("diagram", "grid-image") for p, _ in info["figures"])):
        return "dense"
    if info["columns"] or info.get("panels"):
        return "columns"
    if pics or tables:
        return "charts"
    return "text"


def rules_flags(sp: SlidePlan) -> list:
    """Tanda bahwa rencana aturan untuk slide ini meragukan -> planner auto mengirimnya ke LLM."""
    flags = ["dense"] if sp.kind == "dense" else []
    if sp.kind in NO_LLM_KINDS:
        return flags
    blocks = sp.rules_plan["blocks"]
    if not any(b["type"] == "heading" and b.get("level") == 1 for b in blocks):
        flags.append("no_title")
    figs = [b for b in blocks if b["type"] == "figure" and not b.get("icon")]
    if len(figs) >= 2 and any(not f.get("caption") for f in figs):
        flags.append("uncaptioned")
    if any(sp.els[k].kind == "text" and len(box_text(sp.els[k])) >= LOST_TEXT_CHARS for k in sp.rules_plan["drop"]):
        flags.append("dropped_text")
    short = sum(1 for b in blocks if b["type"] == "text" for p in sp.els[b["id"]].paras
                if 0 < len(para_text(p)) < FRAGMENT_CHARS and not is_label_para(p, para_text(p)))
    if short >= FRAGMENT_MIN:
        flags.append("fragments")
    heads = [box_text(sp.els[b["id"]]).upper() for b in blocks if b["type"] == "heading"]
    if len(heads) != len(set(heads)):
        flags.append("duplicate_heading")
    if any(sp.els[b["id"]].fill_cells >= COLOUR_TABLE_CELLS for b in blocks if b["type"] == "table" and "id" in b):
        flags.append("colour_table")
    return flags


def is_infographic(sp: SlidePlan) -> bool:
    """Slide dense yang oleh aturan dipecah jadi banyak potongan teks pendek / tabel kecil (infografis, matriks,
    alur proses): lebih terbaca sebagai satu gambar daripada puluhan label lepas."""
    if sp.kind != "dense":
        return False
    blocks = sp.rules_plan["blocks"]
    paras = [t for b in blocks if b["type"] in ("text", "heading") and b.get("level") != 1
             for t in (para_text(p) for p in sp.els[b["id"]].paras) if t]
    short = sum(1 for t in paras if len(t) < FRAGMENT_CHARS)
    tables = sum(1 for b in blocks if b["type"] == "table")
    return short + 2 * tables >= INFOGRAPHIC_MIN_PIECES and short >= INFOGRAPHIC_SHORT_SHARE * len(paras)


def header_texts(els: dict, title) -> list:
    """Pesan kunci tepat di bawah judul: teks lebar berurutan sebelum elemen lain (grafik, panel)."""
    out, bottom = [], title.b
    for b in sorted(els.values(), key=lambda b: (b.y, b.x)):
        if (b is title or b.w * b.h >= 0.8                           # judul, latar belakang slide
                or (b.y < title.b and b.b <= title.b + 0.02)            # pita judul: nomor slide, logo, tag
                or (b.kind == "shape" and min(b.w, b.h) < 0.01)):      # garis pemisah
            continue
        if b.kind != "text" or not box_text(b) or b.w < 0.4 or b.filled or b.y - bottom > 0.05:
            break
        out.append(b)
        bottom = max(bottom, b.b)
    return out


def infographic_plan(sp: SlidePlan) -> dict:
    """Judul + pesan kunci di bawahnya tetap teks; sisa slide satu gambar selebar halaman (crop render)."""
    els, title = sp.els, sp.info["title"]
    key = {id(b): k for k, b in els.items()}
    heads = header_texts(els, title) if title is not None else []
    top = max([title.b if title is not None else 0.0] + [b.b for b in heads])
    keep = {id(b) for b in heads} | ({id(title)} if title is not None else set())
    body = [k for k, b in els.items() if id(b) not in keep and b.b > top + 0.005]
    blocks = [{"type": "heading", "id": key[id(title)], "level": 1}] if title is not None else []
    blocks += [{"type": "text", "id": key[id(b)]} for b in heads]
    if body:
        x, y, w, h = union([els[k] for k in body])
        y2 = max(y, top)
        blocks.append({"type": "figure", "ids": body, "box": [round(v, 5) for v in (x, y2, w, y + h - y2)]})
    return {"blocks": blocks, "drop": [k for k, b in els.items() if id(b) not in keep and k not in body]}


def boilerplate_labels(slides: list) -> set:
    """Sub-judul yang sama persis muncul di banyak slide = label template ("HASIL PEMBAHASAN ...")."""
    seen = Counter()
    for sp in slides:
        seen.update({box_text(sp.els[b["id"]]).upper() for b in sp.rules_plan["blocks"]
                     if b["type"] == "heading" and b.get("level", 1) >= 2})
    common = {t for t, c in seen.items() if c >= BOILERPLATE_MIN_SLIDES and len(t.split()) >= BOILERPLATE_MIN_WORDS}
    return common | BOILERPLATE


def plan_ids(plan: dict) -> set:
    used = set()
    for b in plan["blocks"]:
        used.update(k for k in [b.get("id"), b.get("caption")] + b.get("ids", []) if k)
        for row in b.get("cells", []):
            for cell in row:
                used.update(cell)
    return used


def attach_icons(plan: dict, els: dict) -> dict:
    """Konvensi contoh test3.docx: ikon kecil yang menempel di judul bagian (MONETER, MAKROPRUDENSIAL, ...)
    ikut sebagai gambar dengan keterangan judul itu. Dijalankan untuk semua rencana (aturan maupun LLM)
    supaya hasilnya tidak bergantung pada planner."""
    used, figs = plan_ids(plan), []
    for b in plan["blocks"]:
        if b["type"] != "heading" or b.get("level") != 2:
            continue
        h = els[b["id"]]
        near = le.Box("", h.x - ICON_NEAR, h.y - ICON_NEAR, h.w + 2 * ICON_NEAR, h.h + 2 * ICON_NEAR)
        icon = next((k for k, e in els.items() if e.kind == "picture" and e.w < le.ICON_MAX_W
                     and k not in used and le._inter(e, near) > 0), None)
        if icon:
            figs.append({"type": "figure", "ids": [icon], "caption": b["id"], "icon": True})
            used.add(icon)
    if not figs:
        return plan
    icons = {f["ids"][0] for f in figs}
    return normalize({"blocks": plan["blocks"] + figs, "drop": [k for k in plan["drop"] if k not in icons]}, els)


def drop_boilerplate(plan: dict, els: dict, labels: set) -> dict:
    keep, drop = [], list(plan["drop"])
    for b in plan["blocks"]:
        if b["type"] in ("heading", "text") and box_text(els[b["id"]]).upper() in labels \
                and not (b["type"] == "heading" and b.get("level") == 1):
            drop.append(b["id"])
        else:
            keep.append(b)
    return {"blocks": keep, "drop": drop}


# --------------------------------------------------------------------------- validasi rencana
def validate_plan(plan, els: dict) -> list:
    """Kesalahan rencana LLM (kosong = sah). Pesan berbahasa Inggris karena dikirim balik ke LLM."""
    if not isinstance(plan, dict) or not isinstance(plan.get("blocks"), list):
        return ['the answer must be an object with a "blocks" list']
    errs, content, members, captions, regions = [], [], [], [], []

    def check(k, kinds, where) -> bool:
        if not isinstance(k, str) or k not in els:
            errs.append(f"{where}: unknown id {k!r}")
            return False
        if kinds and els[k].kind not in kinds:
            errs.append(f"{where}: {k} is a {els[k].kind}, expected {'/'.join(kinds)}")
            return False
        return True

    for i, b in enumerate(plan["blocks"]):
        t = b.get("type") if isinstance(b, dict) else None
        where = f"block {i} ({t})"
        if t == "heading":
            if b.get("level") not in (1, 2, 3):
                errs.append(f"{where}: level must be 1, 2 or 3")
            if check(b.get("id"), ("text",), where):
                content.append(b["id"])
        elif t in ("text", "note"):
            if check(b.get("id"), ("text",), where):
                content.append(b["id"])
        elif t == "table":
            if "id" in b:
                if check(b["id"], ("table",), where):
                    content.append(b["id"])
                    if els[b["id"]].fill_cells >= COLOUR_TABLE_CELLS:
                        errs.append(f"{where}: {b['id']} carries its meaning in coloured cells (Gantt/status "
                                    "colours); it must be a figure so the colours stay visible")
            elif isinstance(b.get("cells"), list) and b["cells"] and all(
                    isinstance(r, list) and all(isinstance(c, list) for c in r) for r in b["cells"]):
                for row in b["cells"]:
                    for cell in row:
                        content += [k for k in cell if check(k, ("text",), where)]
            else:
                errs.append(f'{where}: needs "id" (native table) or "cells" (list of rows of lists of ids)')
        elif t == "figure":
            fids = b.get("ids")
            if not isinstance(fids, list) or not fids:
                errs.append(f'{where}: "ids" must list the elements that make up the image')
            else:
                ok = [k for k in fids if check(k, None, where)]
                members += ok
                if ok:
                    regions.append((i, _region_box(fig_region({"ids": ok}, els))))
            cap = b.get("caption")
            if cap is not None and check(cap, ("text",), where):
                captions.append(cap)
        else:
            errs.append(f"block {i}: unknown type {t!r}")

    dup = {k for k in content if content.count(k) > 1} | {k for k in members if members.count(k) > 1}
    dup |= set(content) & set(members)
    dup |= {c for c in captions if captions.count(c) > 1 or c in content or c in members}
    if dup:
        errs.append("ids used more than once: " + ", ".join(sorted(dup)))
    drop = {k for k in plan.get("drop", []) if isinstance(k, str)}
    used = set(content) | set(members) | set(captions) | drop
    missing = [k for k, b in els.items() if b.kind == "text" and k not in used
               and len(box_text(b)) >= MISSING_TEXT_CHARS and not any(inside(b, r) for _, r in regions)]
    if missing:
        errs.append("text elements neither used nor dropped: " + ", ".join(missing))
    # heading tanpa isi (gambar dipindah ke akhir slide) = seharusnya caption gambar
    body = [b for b in plan["blocks"] if isinstance(b, dict) and b.get("type") not in ("figure", "note")]
    empty = [b.get("id") for i, b in enumerate(body) if b.get("type") == "heading" and b.get("level") in (2, 3)
             and (i + 1 == len(body) or (body[i + 1].get("type") == "heading"
                                         and (body[i + 1].get("level") or 9) <= b["level"]))]
    if empty:
        errs.append(f"headings with no text or table under them: {', '.join(map(str, empty))}; a label that titles "
                    "a chart/picture must be that figure's caption, otherwise make it text or drop it")
    # crop gambar yang menutupi teks yang juga ditulis sebagai teks -> teks itu muncul dua kali
    for i, r in regions:
        covered = sorted({k for k in content if els[k].kind == "text" and inside(els[k], r)})
        if covered:
            errs.append(f"block {i} (figure): its crop (bounding box of its ids) covers {', '.join(covered)}, "
                        "which is written as text; remove large background, panel or frame elements from its ids")
    return errs


# --------------------------------------------------------------------------- 3. LLM + cache
def cache_key(slide, provider: str, model: str) -> str:
    h = hashlib.sha256("|".join((PLANNER_VERSION, provider, model)).encode())
    h.update(etree.tostring(slide._element))
    for rel in sorted(slide.part.rels.values(), key=lambda r: r.rId):
        if not rel.is_external and ("image" in rel.reltype or "chart" in rel.reltype):
            h.update(rel.target_part.blob)
    return h.hexdigest()[:32]


def element_rows(els: dict) -> list:
    """Elemen dalam bentuk ringkas untuk prompt LLM."""
    rows = []
    for k, b in els.items():
        row = {"id": k, "kind": b.kind, "x": b.x, "y": b.y, "w": b.w, "h": b.h}
        if b.kind == "text":
            row["paras"] = [("• " if p.bullet else "") + para_text(p) for p in b.paras if para_text(p)]
            row["title"] = b.is_title
            row["filled"] = b.filled
        elif b.kind == "table":
            row["rows"] = b.rows[:3]
            row["size"] = f"{len(b.rows)}x{max((len(r) for r in b.rows), default=0)}"
        elif b.kind == "picture":
            row["small"] = b.w < le.ICON_MAX_W
        rows.append(row)
    return rows


def load_cached_plan(sp: SlidePlan, cache_dir: Optional[Path]) -> bool:
    """Rencana LLM yang sudah tersimpan untuk slide ini (sah menurut validasi sekarang) -> dipakai."""
    cache_file = cache_dir / f"{sp.key}.json" if cache_dir else None
    if not (cache_file and cache_file.exists()):
        return False
    try:
        plan = json.loads(cache_file.read_text(encoding="utf-8"))["plan"]
    except (ValueError, KeyError):
        return False
    if validate_plan(plan, sp.els):
        return False
    sp.plan, sp.source = normalize(plan, sp.els), "cache"
    return True


def plan_with_llm(sp: SlidePlan, render_png: Optional[Path], provider: str, model: str,
                  cache_dir: Optional[Path], instruction: str = "") -> None:
    if load_cached_plan(sp, cache_dir):
        return
    import llm_planner   # import lambat: SDK provider hanya dimuat kalau LLM dipakai

    cache_file = cache_dir / f"{sp.key}.json" if cache_dir else None
    image = None
    if render_png and render_png.exists():
        image = llm_planner.slide_image(render_png)
    draft = {"blocks": [{k: v for k, v in b.items() if k != "box"} for b in sp.rules_plan["blocks"]
                        if not (b["type"] == "table" and "rows" in b)],
             "drop": sp.rules_plan["drop"]}
    try:
        plan, errors = llm_planner.plan_slide(element_rows(sp.els), draft, image, provider, model,
                                              validate=lambda p: validate_plan(p, sp.els), instruction=instruction)
    except Exception as e:      # jaringan / kuota / SDK: slide tetap memakai rencana aturan
        plan, errors = None, [f"{type(e).__name__}: {e}"]
    sp.errors = errors
    if plan is None:
        sp.flags.append("llm_failed")
        return
    if errors:
        sp.flags.append("llm_fixed")      # jawaban pertama ditolak validasi, perbaikannya sah
    sp.plan, sp.source = normalize(plan, sp.els), "llm"
    if cache_file:
        cache_file.parent.mkdir(parents=True, exist_ok=True)
        cache_file.write_text(json.dumps({"plan": plan, "provider": provider, "model": model,
                                          "created": time.strftime("%Y-%m-%d %H:%M:%S")},
                                         ensure_ascii=False), encoding="utf-8")


# --------------------------------------------------------------------------- 4. tulis DOCX
def _icon_image(b: dict, els: dict, path: Path) -> Optional[Path]:
    """Ikon diambil dari gambar aslinya (crop render ikut memotong kotak di sebelahnya), diperkecil."""
    imgs = [img for k in b["ids"] for img in els[k].images]
    if not imgs:
        return None
    blob, ext, _ = max(imgs, key=lambda i: i[2])
    raw = path.with_suffix("." + ext)
    path.parent.mkdir(parents=True, exist_ok=True)
    raw.write_bytes(blob)
    try:
        with Image.open(raw) as im:
            im = im.convert("RGBA")
            im.thumbnail((ICON_MAX_PX, ICON_MAX_PX))
            im.save(path)
        if raw != path:
            raw.unlink()
        return path
    except Exception:
        return raw if ext.lower() in ("png", "jpg", "jpeg", "gif") else None


def figure_layout(b: dict, els: dict) -> str:
    x, y, w, h = fig_region(b, els)
    if b.get("icon") or (w < le.ICON_MAX_W * 1.5 and h < 0.12):
        return "icon"
    # gambar yang isinya banyak teks (diagram, tabel Gantt) perlu selebar halaman supaya terbaca
    n_text = sum(1 for k in b["ids"] if els[k].kind == "text") + \
        sum(1 for k in b["ids"] if els[k].kind == "table" for r in els[k].rows for c in r if c.strip())
    return "wide" if n_text >= WIDE_MIN_TEXTS and w >= WIDE_MIN_W else "chart"


def table_rows(b: dict, els: dict) -> list:
    if "id" in b:
        return [[re.sub(r"[ \t]+", " ", c).strip() for c in r] for r in els[b["id"]].rows]
    if "cells" in b:
        return [[le._cell_text([els[k] for k in cell]) for cell in row] for row in b["cells"]]
    return b.get("rows", [])


def slide_title(sp: SlidePlan) -> str:
    h1 = next((b["id"] for b in sp.plan["blocks"] if b["type"] == "heading" and b.get("level") == 1), None)
    if h1:
        return box_text(sp.els[h1])
    texts = sorted((b for b in sp.els.values() if b.kind == "text" and box_text(b)), key=lambda b: (b.y, b.x))
    return box_text(texts[0]) if texts else ""


def para_runs(p) -> list:
    """Run paragraf apa adanya (tebal/miring per kata), spasi dirapikan."""
    runs = [(re.sub(r"\s+", " ", t), b, i) for t, b, i in le._strip_runs(p.runs)]
    return [r for r in runs if r[0]]


def write_slide(w: ReportWriter, sp: SlidePlan, crop, media_dir: Path):
    els, figures, n_icon = sp.els, [], 0
    for b in sp.plan["blocks"]:
        t = b["type"]
        if t != "figure" and figures:
            w.figures(figures)        # semua gambar slide ini dalam satu tabel
            figures = []
        w.end_list()
        if t == "heading":
            text = box_text(els[b["id"]])
            if text:
                w.heading(text, b.get("level", 2))
        elif t == "text":
            box = els[b["id"]]
            paras = [(p, para_text(p)) for p in box.paras if para_text(p)]
            for p, text in paras:
                label = len(paras) > 1 and is_label_para(p, text)
                w.rich(para_runs(p), "label" if label else "para", bullet=p.bullet, numbered=p.numbered,
                       level=p.level, num_fmt=p.num_fmt)
        elif t == "note":
            for p in els[b["id"]].paras:
                if para_text(p):
                    w.note(para_text(p))
        elif t == "table":
            rows = table_rows(b, els)
            if rows:
                w.table(rows)
        elif t == "figure":
            layout = figure_layout(b, els)
            if layout == "icon":
                n_icon += 1
                img = _icon_image(b, els, media_dir / f"s{sp.n:02d}_icon{n_icon}.png")
            else:
                reg = fig_region(b, els)
                img = crop(le.Box("picture", *reg, images=[i for k in b["ids"] for i in els[k].images]))
            if img is None:
                # tanpa render PowerPoint dan tanpa gambar asli (mis. chart native): tabel asli kalau ada
                tbl = next((k for k in b["ids"] if els[k].kind == "table"), None)
                if tbl is not None:
                    w.figures(figures)
                    figures = []
                    w.table(table_rows({"id": tbl}, els))
                continue
            # if not figures:
            #     w.figures_label()
            figures.append((img, box_text(els[b["caption"]]) if b.get("caption") else "", layout))
    w.figures(figures)


def review_notes(sp: SlidePlan) -> list:
    """Isi komentar review Word untuk slide ini (baris per baris): apa yang diperbaiki AI dan apa yang perlu
    dicek. Kosong = slide aman."""
    checks = [FLAG_INFO.get(f, (f,))[0] for f in sp.flags if f != "llm_fixed"]
    if "dropped_text" in sp.flags:
        lost = [box_text(sp.els[k]) for k in sp.plan["drop"]
                if sp.els[k].kind == "text" and len(box_text(sp.els[k])) >= LOST_TEXT_CHARS]
        checks += [f"Tidak ikut: “{t[:REVIEW_QUOTE_CHARS]}{'...' if len(t) > REVIEW_QUOTE_CHARS else ''}”"
                   for t in lost[:REVIEW_QUOTES]]
    if sp.kind == "infographic":
        checks.append("Slide infografis ditulis sebagai satu gambar; judul dan pesan kunci tetap teks. "
                      "Pastikan gambarnya terbaca.")
    if sp.source in ("llm", "cache"):
        lines = [f"Slide {sp.n}: diperbaiki AI. Susunan slide ini dibuat ulang oleh AI; teks dan angka tetap "
                 "dari slide asli. Cek urutan dan pengelompokan isinya."]
        if checks:
            lines.append("Alasan dikirim ke AI:")
    elif checks:
        lines = [f"Slide {sp.n}: perlu dicek."]
    else:
        return []
    return lines + ["- " + c for c in checks]


def write_report(slides: list, docx_path: Path, template: Path, render_dir: Optional[Path], media_dir: Path,
                 html_path: Optional[Path] = None, comments: bool = False) -> dict:
    """DOCX, dan HTML CKEditor kalau html_path diisi (gambar base64). Hasil: {nomor slide: fragmen HTML}
    untuk halaman review, dengan gambar dirujuk relatif ("media/<nama>").
    comments: versi review, DOCX diberi komentar Word per slide (review_notes)."""
    docx, page = ReportWriter(template), HtmlReportWriter() if html_path else None
    w = Tee(docx, page)
    content = [sp for sp in slides if sp.kind not in ("cover", "closing")]
    cover = next((sp for sp in slides if sp.kind == "cover"), None)
    deck_title = slide_title(cover or (content[0] if content else slides[0])) if slides else ""
    # w.header(deck_title)
    w.title(deck_title)
    fragments = {}
    for sp in content:
        render_png = render_dir / f"slide{sp.n}.png" if render_dir else None
        review = HtmlReportWriter(img_src=lambda p: f"media/{p.name}")
        start = docx.mark()
        write_slide(Tee(docx, page, review), sp, le.make_cropper(render_png, media_dir, sp.n), media_dir)
        if comments:
            docx.comment(start, review_notes(sp))
        fragments[sp.n] = review.fragment()
    docx.save(docx_path)
    if page:
        page.save(html_path, deck_title)
    return fragments


# --------------------------------------------------------------------------- orkestrasi
def plans_json(slides: list) -> list:
    return [{"n": sp.n, "title": slide_title(sp), "kind": sp.kind, "source": sp.source, "flags": sp.flags,
             "errors": sp.errors, "blocks": sp.plan["blocks"], "drop": sp.plan["drop"],
             "elements": {k: f"{b.kind}: {box_text(b)[:80]}" if b.kind == "text" else b.kind
                          for k, b in sp.els.items()}}
            for sp in slides]


def convert_report(
    pptx_path,
    docx_path,
    html_path=None,
    planner: str = "auto",
    provider: str = "bedrock",
    model: str = DEFAULT_MODEL,
    render: bool = True,
    work_dir=None,
    template=DEFAULT_TEMPLATE,
    include_hidden: bool = False,
    cache_dir=DEFAULT_CACHE,
    workers: int = 4,
    progress: ProgressFn = _noop,
    only: Optional[set] = None,
    instruction: str = "",
    slides_dir=None,
    comments: bool = False,
) -> dict:
    """planner: rules (tanpa LLM) | cached (rencana LLM tersimpan bila ada, sisanya aturan; tanpa panggilan LLM)
    | auto (LLM hanya untuk slide dense/bertanda) | llm (semua slide isi).
    html_path: kalau diisi, juga menulis HTML mandiri untuk CKEditor dengan format yang sama.
    only: nomor slide yang dikonversi (untuk mencoba ulang slide tertentu); None = semua.
    instruction: perintah reviewer untuk LLM (bersama only; slide terpilih selalu dikirim ke LLM).
    slides_dir: folder render slide yang sudah ada (slideN.png dari deck yang sama), dipakai tanpa render ulang.
    comments: versi review: komentar Word dari "Digital Workplace" pada slide yang perlu dicek / diperbaiki AI."""
    if planner not in PLANNERS:
        raise ValueError(f"planner tidak dikenal: {planner}")
    pptx_path, docx_path = Path(pptx_path), Path(docx_path)
    work = Path(work_dir) if work_dir else docx_path.parent / (docx_path.stem + "_build")
    render_dir, media_dir = work / "slides", work / "media"
    work.mkdir(parents=True, exist_ok=True)
    t0 = time.time()

    progress(0.02, "Merender slide dengan PowerPoint")
    if slides_dir and (Path(slides_dir) / "slide1.png").exists():
        render_dir, rendered = Path(slides_dir), True
    else:
        rendered = le.render_slides(pptx_path, render_dir) if render else False
    t_render = time.time()

    progress(0.3, "Menyusun rencana layout dengan aturan")
    prs = Presentation(str(pptx_path))
    W, H = prs.slide_width, prs.slide_height
    slides, skipped, visible = [], [], 0
    for n, slide in enumerate(prs.slides, 1):
        if le.is_hidden(slide) and not include_hidden:
            skipped.append(n)
            continue
        visible += 1
        if only and n not in only:
            continue
        els = extract(slide, W, H)
        info = le.analyse(slide, W, H, boxes=list(els.values()))
        sp = SlidePlan(n, els, info)
        sp.kind = classify(els, info, first=visible == 1)
        sp.rules_plan = normalize(rules_plan(els, info), els)
        sp.plan = sp.rules_plan
        sp.flags = rules_flags(sp)
        if rendered and is_infographic(sp):
            # satu gambar dari render (tanpa render PowerPoint tidak ada yang bisa di-crop)
            sp.kind, sp.rules_plan, sp.flags = "infographic", infographic_plan(sp), []
            sp.plan = sp.rules_plan
        if planner != "rules":
            sp.key = cache_key(slide, provider, model + ("|" + instruction.strip() if instruction.strip() else ""))
        slides.append(sp)

    n_flagged = sum(1 for sp in slides if sp.flags)
    if instruction.strip() and planner != "rules":
        targets = list(slides)
    elif planner == "llm":
        targets = [sp for sp in slides if sp.kind not in NO_LLM_KINDS]
    elif planner == "auto":
        targets = [sp for sp in slides if sp.flags]
    else:
        targets = []
    t_plan = time.time()
    if planner == "cached":
        cache = Path(cache_dir) if cache_dir else None
        for sp in slides:
            if sp.kind not in NO_LLM_KINDS:
                load_cached_plan(sp, cache)
    if targets:
        progress(0.35, f"LLM menyusun rencana {len(targets)} slide")
        cache = Path(cache_dir) if cache_dir else None
        with ThreadPoolExecutor(max(1, workers)) as ex:
            futures = {ex.submit(plan_with_llm, sp, render_dir / f"slide{sp.n}.png" if rendered else None,
                                 provider, model, cache, instruction): sp for sp in targets}
            for done, f in enumerate(as_completed(futures), 1):
                f.result()
                progress(0.35 + 0.5 * done / len(targets),
                         f"LLM: slide {futures[f].n} selesai ({done}/{len(targets)})")
    t_llm = time.time()

    labels = boilerplate_labels(slides)
    for sp in slides:
        sp.plan = attach_icons(drop_boilerplate(sp.plan, sp.els, labels), sp.els)

    progress(0.88, "Menulis dokumen Word" + (" dan HTML" if html_path else ""))
    fragments = write_report(slides, docx_path, Path(template), render_dir if rendered else None, media_dir,
                             Path(html_path) if html_path else None, comments)
    plans_path = work / "plans.json"
    plans_path.write_text(json.dumps(plans_json(slides), ensure_ascii=False, indent=1), encoding="utf-8")

    # bahan halaman review (/review): render asli + HTML hasil per slide, sama seperti layout_engine
    written = [sp for sp in slides if sp.n in fragments]
    if rendered:
        le.write_previews(render_dir, [sp.n for sp in written])
    review = {"source": pptx_path.name, "rendered": rendered, "skipped": skipped, "slides": [
        {"n": sp.n, "render": f"slides/preview{sp.n}.jpg" if rendered else None, "html": fragments[sp.n],
         "kind": sp.kind, "source": sp.source, "flags": sp.flags} for sp in written]}
    (work / "review.json").write_text(json.dumps(review, ensure_ascii=False), encoding="utf-8")

    progress(1.0, "Selesai")
    sources = Counter(sp.source for sp in slides)
    return {
        "slides": len(slides), "hidden_skipped": skipped, "rendered": rendered, "planner": planner,
        "kinds": dict(Counter(sp.kind for sp in slides)),
        "flagged": n_flagged, "llm_slides": sources.get("llm", 0), "cache_hits": sources.get("cache", 0),
        "llm_fixed": [sp.n for sp in slides if "llm_fixed" in sp.flags],
        "llm_failed": [sp.n for sp in slides if "llm_failed" in sp.flags],
        "comments": sum(1 for sp in slides if review_notes(sp)) if comments else 0,
        "seconds": {"render": round(t_render - t0, 1), "rules": round(t_plan - t_render, 1),
                    "llm": round(t_llm - t_plan, 1), "write": round(time.time() - t_llm, 1)},
        "docx": str(docx_path), "html": str(html_path) if html_path else None, "plans": str(plans_path),
        "review": str(work / "review.json"),
    }


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="PPTX -> DOCX format laporan (aturan + LLM untuk slide sulit)")
    ap.add_argument("pptx")
    ap.add_argument("-o", "--output", default="Report_Output.docx")
    ap.add_argument("--html", default=None, help="juga tulis HTML mandiri untuk CKEditor ke path ini")
    ap.add_argument("--planner", choices=PLANNERS, default="auto",
                    help="auto: LLM hanya untuk slide dense/bertanda (default); rules: tanpa LLM; "
                         "cached: rencana LLM yang sudah tersimpan, tanpa panggilan LLM; llm: semua slide")
    ap.add_argument("--provider", choices=["bedrock", "ollama"], default="bedrock")
    ap.add_argument("--model", default=DEFAULT_MODEL)
    ap.add_argument("--template", default=str(DEFAULT_TEMPLATE))
    ap.add_argument("--work-dir", default=None)
    ap.add_argument("--workers", type=int, default=4, help="jumlah panggilan LLM paralel")
    ap.add_argument("--no-cache", action="store_true", help="jangan pakai/simpan cache rencana LLM")
    ap.add_argument("--no-render", action="store_true", help="jangan pakai PowerPoint, ambil gambar asli")
    ap.add_argument("--include-hidden", action="store_true", help="ikut konversi slide yang di-hide")
    ap.add_argument("--slides", default=None, help="hanya slide ini, mis. 5,12,30 (untuk mencoba ulang)")
    ap.add_argument("--comments", action="store_true",
                    help="versi review: komentar Word pada slide yang perlu dicek / diperbaiki AI")
    a = ap.parse_args()
    stats = convert_report(a.pptx, a.output, a.html, planner=a.planner, provider=a.provider, model=a.model,
                           render=not a.no_render, work_dir=a.work_dir, template=a.template,
                           include_hidden=a.include_hidden, cache_dir=None if a.no_cache else DEFAULT_CACHE,
                           workers=a.workers, progress=lambda f, m: print(f"[{f:4.0%}] {m}"),
                           only={int(x) for x in a.slides.split(",")} if a.slides else None,
                           comments=a.comments)
    print(json.dumps(stats, ensure_ascii=False, indent=1))
