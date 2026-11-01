"""Membaca slide PPTX: elemen (teks, gambar, tabel) dengan koordinatnya, dan render slide ke PNG
(PowerPoint, atau LibreOffice kalau tidak ada). Dipakai book_engine."""
from __future__ import annotations

import re
import shutil
import subprocess
import threading
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

from docx.oxml.ns import qn
from PIL import Image
from pptx import Presentation
from pptx.enum.shapes import MSO_SHAPE_TYPE, PP_PLACEHOLDER


# Ambang aturan (fraksi lebar/tinggi slide)
ICON_MAX_W = 0.08         # gambar lebih sempit dari ini = ikon/logo, dibuang


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
            box.kind = "picture"
            try:
                img = s.image
                box.images = [(img.blob, img.ext, box.w * box.h)]
            except Exception:
                pass                  # gambar tertaut (tanpa data di PPTX): diambil dari render, seperti chart
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


def _inside(inner: Box, outer: Box, tol: float = 0.01) -> bool:
    return (inner.x >= outer.x - tol and inner.r <= outer.r + tol
            and inner.y >= outer.y - tol and inner.b <= outer.b + tol)


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
    """Render tiap slide ke out_dir/slideN.png lewat PowerPoint, atau LibreOffice kalau PowerPoint tidak ada
    (macOS/Linux). False kalau keduanya tidak tersedia: pemanggil pakai gambar asli dari PPTX."""
    prs = Presentation(str(pptx))
    height_px = round(width_px * prs.slide_height / prs.slide_width)
    out_dir.mkdir(parents=True, exist_ok=True)
    with _render_lock:
        if _render_powerpoint(pptx, out_dir, width_px, height_px):
            return True
        return _render_libreoffice(pptx, out_dir, width_px, len(prs.slides))


def _render_powerpoint(pptx: Path, out_dir: Path, width_px: int, height_px: int) -> bool:
    ps = shutil.which("powershell") or shutil.which("pwsh")
    if not ps:
        return False
    script = (_PS_RENDER.replace("{src}", str(pptx.resolve()).replace("'", "''"))
              .replace("{out}", str(out_dir.resolve()).replace("'", "''"))
              .replace("{w}", str(width_px)).replace("{h}", str(height_px)))
    try:
        subprocess.run([ps, "-NoProfile", "-NonInteractive", "-Command", script],
                       check=True, capture_output=True, timeout=900)
    except (subprocess.SubprocessError, OSError) as e:
        print(f"  [!] Render PowerPoint gagal, coba LibreOffice: {e}")
        return False
    return (out_dir / "slide1.png").exists()


def find_soffice() -> Optional[str]:
    found = shutil.which("soffice") or shutil.which("libreoffice")
    if found:
        return found
    for p in (r"C:\Program Files\LibreOffice\program\soffice.exe",
              r"C:\Program Files (x86)\LibreOffice\program\soffice.exe",
              "/Applications/LibreOffice.app/Contents/MacOS/soffice"):
        if Path(p).exists():
            return p
    return None


# slide yang di-hide ikut diekspor supaya halaman PDF ke-n = slide ke-n (sama dengan Export PowerPoint)
_LO_PDF_FILTER = 'pdf:impress_pdf_Export:{"ExportHiddenSlides":{"type":"boolean","value":"true"}}'


def _render_libreoffice(pptx: Path, out_dir: Path, width_px: int, n_slides: int) -> bool:
    """PPTX -> PDF (LibreOffice headless) -> PNG per halaman (PyMuPDF), nama file sama dengan render PowerPoint."""
    soffice = find_soffice()
    if not soffice:
        return False
    try:
        import fitz   # PyMuPDF
    except ImportError:
        print("  [!] PyMuPDF belum terpasang (pip install pymupdf), pakai gambar asli dari PPTX")
        return False
    import tempfile
    with tempfile.TemporaryDirectory(prefix="lo_render_") as tmp:
        tmp = Path(tmp)
        # profil sendiri: tidak bentrok dengan LibreOffice yang sedang dibuka pengguna
        profile = (tmp / "profile").resolve().as_uri()
        try:
            subprocess.run([soffice, f"-env:UserInstallation={profile}", "--headless", "--norestore",
                            "--convert-to", _LO_PDF_FILTER, "--outdir", str(tmp), str(pptx.resolve())],
                           check=True, capture_output=True, timeout=900)
        except (subprocess.SubprocessError, OSError) as e:
            print(f"  [!] Render LibreOffice gagal, pakai gambar asli dari PPTX: {e}")
            return False
        pdf = tmp / (pptx.stem + ".pdf")
        if not pdf.exists():
            print("  [!] LibreOffice tidak menghasilkan PDF, pakai gambar asli dari PPTX")
            return False
        with fitz.open(pdf) as doc:
            if len(doc) != n_slides:
                print(f"  [!] PDF LibreOffice {len(doc)} halaman, PPTX {n_slides} slide: render tidak dipakai")
                return False
            for i, page in enumerate(doc, 1):
                zoom = width_px / page.rect.width
                page.get_pixmap(matrix=fitz.Matrix(zoom, zoom), alpha=False).save(str(out_dir / f"slide{i}.png"))
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


def is_hidden(slide) -> bool:
    """Slide yang di-hide di PowerPoint (Hide Slide) punya atribut show="0"."""
    return slide._element.get("show") in ("0", "false")


# --------------------------------------------------------------------------- teks & geometri
def para_text(p) -> str:
    return re.sub(r"\s+", " ", "".join(r[0] for r in _strip_runs(p.runs))).strip()


def box_text(b) -> str:
    return " ".join(t for t in (para_text(p) for p in b.paras) if t)


def union(boxes) -> tuple:
    x, y = max(min(b.x for b in boxes), 0.0), max(min(b.y for b in boxes), 0.0)
    r, btm = min(max(b.r for b in boxes), 1.0), min(max(b.b for b in boxes), 1.0)
    return x, y, max(r - x, 0.0), max(btm - y, 0.0)


def inside(b, reg: Box) -> bool:
    return _inside(b, reg, 0.01) or (b.w * b.h > 0 and _inter(b, reg) > 0.5 * b.w * b.h)


# --------------------------------------------------------------------------- 1. extract
def extract(slide, W: int, H: int) -> dict:
    boxes = [b for b in collect(slide.shapes, W, H) if _on_slide(b)]
    return {f"e{i}": b for i, b in enumerate(boxes, 1)}
