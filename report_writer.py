"""DOCX dengan format laporan seperti docs/test3.docx. Hanya urusan format; isi dan urutan datang dari
rencana slide (report_engine).

Format:
  - judul dokumen "Hasil Konversi Presentasi" + subjudul (judul deck); header kanan = judul deck,
    footer = nomor halaman (keduanya dari template)
  - Heading 1 = judul slide, Heading 2 = judul kolom/bagian; isi ditulis apa adanya dari PPT:
    bullet / nomor dan levelnya jadi list Word, tebal / miring per kata tetap
  - gambar: satu tabel per slide, satu baris per gambar: gambar | keterangan (ikon: kolom 900 twips;
    grafik: 60/40); gambar lebar (diagram padat, tabel Gantt) selebar tabel dengan keterangan di bawahnya

HtmlReportWriter menulis format yang sama sebagai HTML bersih untuk CKEditor (h1/h2, p, ul/ol, table);
Tee meneruskan panggilan yang sama ke beberapa writer, jadi DOCX dan HTML selalu berisi hal yang sama.

Template dibuat ulang dari contoh hasil yang benar kalau formatnya berubah:
    python report_writer.py --make-template docs/test3.docx
"""
from __future__ import annotations

import argparse
import base64
import html
from pathlib import Path
from typing import Callable

from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.opc.constants import RELATIONSHIP_TYPE as RT
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Emu, Pt, RGBColor, Twips
from PIL import Image

HERE = Path(__file__).resolve().parent
DEFAULT_TEMPLATE = HERE / "docs" / "report_template.docx"

DOC_TITLE = "Hasil Konversi Presentasi"
FIGURES_LABEL = "Gambar dan Keterangan"
FONT, FONT_EAST_ASIA = "Frutiger 45 Light", "SimSun"

TEXT_W = 9020                       # lebar tabel (twips) = lebar teks A4 dengan margin 1"
FIG_COLS = (5417, 3603)             # tabel grafik: gambar | keterangan
ICON_COLS = (900, 8120)             # tabel ikon
FIG_IMG_W = 3200400                 # EMU (3,5")
ICON_IMG_W = 457200                 # EMU (0,5")
WIDE_IMG_W = (TEXT_W - 200) * 635   # EMU: selebar tabel dikurangi margin sel
MAX_IMG_H = 8 * 914400              # gambar setinggi ini atau lebih diperkecil supaya muat satu halaman
BORDER_COLOR = "BFBFBF"
CAPTION_FILL = "F2F6FA"

# jenis paragraf -> format (ukuran pt, tebal, warna, spasi twips, perataan, styleId Word)
PARA = {
    "title": dict(size=16, bold=True, color="000000", after=120, align="left"),
    "subtitle": dict(size=12, color="595959", after=400, align="left"),
    "h1": dict(style="Heading1", size=11, bold=True, color="000000", before=360, after=200),
    "h2": dict(style="Heading2", size=11, bold=True, color="000000", before=240, after=120),
    "label": dict(size=11, bold=False, before=160, after=80),
    "figlabel": dict(size=11, bold=False, before=240, after=120),
    "para": dict(size=11, after=120, line=1.2),
    "note": dict(size=9, color="595959", after=80),
    "spacer": dict(after=80),
}


def _el(tag: str, **attrs) -> OxmlElement:
    e = OxmlElement(tag)
    for k, v in attrs.items():
        e.set(qn("w:" + k), str(v))
    return e


def _style_run(run, size=None, bold=False, color=None, italic=False):
    run.font.name = FONT
    fonts = run._r.get_or_add_rPr().get_or_add_rFonts()
    fonts.set(qn("w:eastAsia"), FONT_EAST_ASIA)
    fonts.set(qn("w:cs"), FONT)
    run.bold = True if bold else None
    run.italic = True if italic else None
    if color:
        run.font.color.rgb = RGBColor.from_string(color)
    if size:
        run.font.size = Pt(size)


def _format_para(p, kind: str):
    f = PARA[kind]
    if f.get("style"):
        # lewat styleId: nama style di template buatan docx-js ("Heading 1") tidak dikenali python-docx
        p._p.get_or_add_pPr().style = f["style"]
    pf = p.paragraph_format
    if "before" in f:
        pf.space_before = Twips(f["before"])
    if "after" in f:
        pf.space_after = Twips(f["after"])
    if "line" in f:
        pf.line_spacing = f["line"]
    if f.get("align") == "center":
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER


def _cell_props(cell, width: int, fill=None, margins=(100, 100, 100, 100)):
    """tcPr ditulis ulang dengan urutan elemen sesuai skema (tcW, gridSpan, shd, tcMar, vAlign)."""
    tc = cell._tc
    old = tc.tcPr
    span = old.find(qn("w:gridSpan")) if old is not None else None
    if old is not None:
        tc.remove(old)
    pr = OxmlElement("w:tcPr")
    pr.append(_el("w:tcW", type="dxa", w=width))
    if span is not None:      # sel hasil merge
        pr.append(span)
    if fill:
        pr.append(_el("w:shd", val="clear", fill=fill))
    mar = OxmlElement("w:tcMar")
    for side, v in zip(("top", "left", "bottom", "right"), margins):
        mar.append(_el("w:" + side, type="dxa", w=v))
    pr.append(mar)
    pr.append(_el("w:vAlign", val="center"))
    tc.insert(0, pr)


def _table_props(table, widths: list):
    tbl = table._tbl
    pr = tbl.tblPr
    for child in list(pr):
        pr.remove(child)
    pr.append(_el("w:tblW", type="dxa", w=sum(widths)))
    borders = OxmlElement("w:tblBorders")
    for side in ("top", "left", "bottom", "right", "insideH", "insideV"):
        borders.append(_el("w:" + side, val="single", color=BORDER_COLOR, sz=4))
    pr.append(borders)
    pr.append(_el("w:tblLayout", type="fixed"))
    for col, w in zip(tbl.tblGrid.findall(qn("w:gridCol")), widths):
        col.set(qn("w:w"), str(w))


def _picture_size(img: Path, width: int) -> tuple:
    with Image.open(img) as im:
        iw, ih = im.size
    height = round(width * ih / max(iw, 1))
    if height > MAX_IMG_H:
        width, height = round(width * MAX_IMG_H / height), MAX_IMG_H
    return width, height


BULLET_CHARS = ("•", "◦", "▪")
LIST_INDENT = 360                    # twips per level
_NUM_FMT_TEXT = {"decimal": "%{n}.", "lowerLetter": "%{n}.", "upperLetter": "%{n}.",
                 "lowerRoman": "%{n}.", "upperRoman": "%{n}."}


def _abstract_num(abstract_id: int, fmt: str) -> OxmlElement:
    """Definisi list 9 level: fmt "bullet" atau format nomor Word (decimal, lowerLetter, ...)."""
    an = _el("w:abstractNum", abstractNumId=abstract_id)
    an.append(_el("w:multiLevelType", val="hybridMultilevel"))
    for lvl in range(9):
        lv = _el("w:lvl", ilvl=lvl)
        lv.append(_el("w:start", val=1))
        lv.append(_el("w:numFmt", val=fmt))
        text = BULLET_CHARS[lvl % 3] if fmt == "bullet" else _NUM_FMT_TEXT[fmt].format(n=lvl + 1)
        lv.append(_el("w:lvlText", val=text))
        lv.append(_el("w:lvlJc", val="left"))
        ppr = OxmlElement("w:pPr")
        ppr.append(_el("w:ind", left=LIST_INDENT * (lvl + 1), hanging=LIST_INDENT))
        lv.append(ppr)
        an.append(lv)
    return an


class ReportWriter:
    def __init__(self, template: Path = DEFAULT_TEMPLATE):
        self.doc = Document(str(template))
        body = self.doc.element.body
        for el in list(body):
            if el.tag != qn("w:sectPr"):
                body.remove(el)
        self._abstract = {}       # format list -> abstractNumId
        self._lists = {}          # list yang sedang berjalan: {(format, level): numId}

    # ------------------------------------------------------------------ list (bullet / nomor)
    def _numbering(self):
        return self.doc.part.numbering_part.element

    def _abstract_for(self, fmt: str) -> str:
        if fmt not in self._abstract:
            numbering = self._numbering()
            ids = [int(a.get(qn("w:abstractNumId"))) for a in numbering.findall(qn("w:abstractNum"))]
            new = _abstract_num(max(ids, default=0) + 1, fmt)
            first_num = numbering.find(qn("w:num"))   # abstractNum harus sebelum w:num
            if first_num is not None:
                first_num.addprevious(new)
            else:
                numbering.append(new)
            self._abstract[fmt] = new.get(qn("w:abstractNumId"))
        return self._abstract[fmt]

    def _num_for(self, fmt: str, level: int) -> str:
        """numId list yang sedang berjalan; list baru (mulai dari 1) kalau belum ada."""
        for key in [k for k in self._lists if k[1] > level]:   # sub-list selesai saat kembali ke level ini
            del self._lists[key]
        key = (fmt, level)
        if key not in self._lists:
            numbering = self._numbering()
            new_id = max((int(n.get(qn("w:numId"))) for n in numbering.findall(qn("w:num"))), default=0) + 1
            num = _el("w:num", numId=new_id)
            num.append(_el("w:abstractNumId", val=self._abstract_for(fmt)))
            ov = _el("w:lvlOverride", ilvl=level)
            ov.append(_el("w:startOverride", val=1))
            num.append(ov)
            numbering.append(num)
            self._lists[key] = str(new_id)
        return self._lists[key]

    def end_list(self):
        self._lists = {}

    def rich(self, runs: list, kind: str = "para", bullet: bool = False, numbered: bool = False,
             level: int = 0, num_fmt: str = "decimal"):
        """Paragraf dengan run apa adanya dari PPT: runs = [(teks, tebal, miring)]; bullet / nomor PPT
        jadi list Word di level yang sama."""
        p = self._para(kind)
        if bullet:
            fmt = num_fmt if numbered else "bullet"
            pr = p._p.get_or_add_pPr()
            numpr = OxmlElement("w:numPr")
            numpr.append(_el("w:ilvl", val=min(level, 8)))
            numpr.append(_el("w:numId", val=self._num_for(fmt, min(level, 8))))
            pr.insert(1 if pr.find(qn("w:pStyle")) is not None else 0, numpr)
        else:
            self.end_list()
        f = PARA[kind]
        for text, b, i in runs:
            _style_run(p.add_run(text), f.get("size"), b or f.get("bold", False), f.get("color"), i)
        return p

    # ------------------------------------------------------------------ paragraf
    def _para(self, kind: str, text: str = "", container=None):
        p = (container or self.doc).add_paragraph()
        _format_para(p, kind)
        if text:
            f = PARA[kind]
            _style_run(p.add_run(text), f.get("size"), f.get("bold", False), f.get("color"))
        return p

    def header(self, text: str):
        for sec in self.doc.sections:
            hdr = sec.header
            p = hdr.paragraphs[0] if hdr.paragraphs else hdr.add_paragraph()
            for r in list(p.runs):
                r._r.getparent().remove(r._r)
            _style_run(p.add_run(text), 9, False, "808080")

    def title(self, title: str, subtitle: str = ""):
        self._para("title", title)
        if subtitle:
            self._para("subtitle", subtitle)

    def heading(self, text: str, level: int):
        self._para({1: "h1", 2: "h2"}.get(level, "label"), text)

    def label(self, text: str):
        self._para("label", text)

    def para(self, text: str):
        self._para("para", text)

    def note(self, text: str):
        self._para("note", text)

    def figures_label(self):
        self._para("figlabel", FIGURES_LABEL)

    def spacer(self):
        self._para("spacer")

    # ------------------------------------------------------------------ tabel
    @staticmethod
    def _picture(cell, img: Path, img_w: int):
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        w, h = _picture_size(img, img_w)
        p.add_run().add_picture(str(img), width=Emu(w), height=Emu(h))

    @staticmethod
    def _caption(cell, caption: str, bold: bool):
        cp = cell.paragraphs[0]
        cp.paragraph_format.space_after = Twips(0)
        if caption:
            _style_run(cp.add_run(caption), 10, bold)

    def figures(self, items: list):
        """Semua gambar satu slide dalam satu tabel. items = [(gambar, keterangan, layout)]:
        icon / chart = satu baris gambar | keterangan; wide = gambar selebar tabel (sel digabung) dengan
        keterangan di baris bawahnya."""
        if not items:
            return
        cols = ICON_COLS if all(layout == "icon" for _, _, layout in items) else FIG_COLS
        t = self.doc.add_table(rows=0, cols=2)
        _table_props(t, list(cols))
        cap_margins = (100, 140, 100, 140)
        for img, caption, layout in items:
            if layout == "wide":
                cells = t.add_row().cells
                img_cell = cells[0].merge(cells[1])
                _cell_props(img_cell, sum(cols))
                self._picture(img_cell, img, WIDE_IMG_W)
                if not caption:
                    continue
                cells = t.add_row().cells
                cap_cell = cells[0].merge(cells[1])
                _cell_props(cap_cell, sum(cols), CAPTION_FILL, cap_margins)
                self._caption(cap_cell, caption, True)
            else:
                img_cell, cap_cell = t.add_row().cells
                _cell_props(img_cell, cols[0])
                _cell_props(cap_cell, cols[1], CAPTION_FILL, cap_margins)
                icon = layout == "icon"
                self._picture(img_cell, img, ICON_IMG_W if icon else min(FIG_IMG_W, (cols[0] - 200) * 635))
                self._caption(cap_cell, caption, not icon)
        self.spacer()

    def table(self, rows: list):
        ncols = max((len(r) for r in rows), default=0)
        if not ncols:
            return
        widths = [TEXT_W // ncols] * ncols
        widths[-1] += TEXT_W - sum(widths)
        size = 8 if ncols > 4 else 9
        t = self.doc.add_table(rows=0, cols=ncols)
        _table_props(t, widths)
        for i, r in enumerate(rows):
            cells = t.add_row().cells
            for c, val, w in zip(cells, list(r) + [""] * (ncols - len(r)), widths):
                _cell_props(c, w, CAPTION_FILL if i == 0 else None, (60, 100, 60, 100))
                for k, line in enumerate((val or "").split("\n")):
                    p = c.paragraphs[0] if k == 0 else c.add_paragraph()
                    p.paragraph_format.space_after = Twips(0)
                    if line.strip():
                        _style_run(p.add_run(line.strip()), size, i == 0)
        self.spacer()

    def save(self, path: Path):
        Path(path).parent.mkdir(parents=True, exist_ok=True)
        self.doc.save(str(path))


# --------------------------------------------------------------------------- HTML (CKEditor)
FIG_PCT = tuple(round(100 * c / TEXT_W) for c in FIG_COLS)      # 60 / 40
ICON_PCT = tuple(round(100 * c / TEXT_W) for c in ICON_COLS)    # 10 / 90
ICON_PX = round(ICON_IMG_W / 914400 * 96)                       # 0,5" pada 96 dpi
_HTML_TABLE = '<table border="1" style="border-collapse:collapse;width:100%"><tbody>'
_HTML_OL_TYPE = {"lowerLetter": "a", "upperLetter": "A", "lowerRoman": "i", "upperRoman": "I"}


def img_data_uri(path: Path) -> str:
    ext = path.suffix.lower().lstrip(".")
    mime = "image/" + {"jpg": "jpeg"}.get(ext, ext)
    return f"data:{mime};base64," + base64.b64encode(path.read_bytes()).decode()


def _runs_html(runs: list) -> str:
    out = []
    for text, b, i in runs:
        s = html.escape(text)
        if i:
            s = f"<i>{s}</i>"
        if b:
            s = f"<strong>{s}</strong>"
        out.append(s)
    return "".join(out)


def html_document(fragment: str, title: str) -> str:
    return (f'<!DOCTYPE html>\n<html lang="id"><head><meta charset="UTF-8"><title>{html.escape(title)}</title>'
            f"<style>body{{font-family:'{FONT}',Arial,sans-serif;font-size:11pt;max-width:900px;margin:20px auto;"
            "line-height:1.4}td{vertical-align:middle;padding:6px}</style></head>\n<body>\n"
            f"{fragment}\n</body></html>\n")


class HtmlReportWriter:
    """Format laporan yang sama dengan ReportWriter, sebagai fragmen HTML tanpa class untuk CKEditor.
    img_src: path gambar -> src (default base64, jadi file HTML-nya mandiri)."""

    def __init__(self, img_src: Callable[[Path], str] = img_data_uri):
        self.img_src = img_src
        self.out = []
        self._lists = []          # tag list yang terbuka per level: "ul" / "ol" / 'ol type="a"'
        self._base = 0            # level PPT item pertama list = level 0 HTML

    # ------------------------------------------------------------------ list (bullet / nomor)
    def _close(self, depth: int) -> str:
        s = ""
        while len(self._lists) > depth:
            s += f"</li></{self._lists.pop().split()[0]}>"
        return s

    def end_list(self):
        if self._lists:
            self.out.append(self._close(0))

    def _item(self, tag: str, level: int) -> str:
        """Penutup / pembuka list sebelum <li> baru. Level relatif terhadap item pertama dan paling banyak
        satu level lebih dalam dari list yang terbuka, supaya setiap sub-list ada di dalam <li> induknya."""
        if not self._lists:
            self._base = level
        lvl = min(max(level - self._base, 0), len(self._lists))
        s = self._close(lvl + 1)
        if len(self._lists) == lvl + 1 and self._lists[lvl] != tag:   # jenis list berganti -> list baru
            s += self._close(lvl)
        if len(self._lists) == lvl + 1:
            s += "</li>"
        else:
            s += f"<{tag}>"
            self._lists.append(tag)
        return s + "<li>"

    def rich(self, runs: list, kind: str = "para", bullet: bool = False, numbered: bool = False,
             level: int = 0, num_fmt: str = "decimal"):
        if bullet:
            tag = "ul" if not numbered else (
                f'ol type="{_HTML_OL_TYPE[num_fmt]}"' if num_fmt in _HTML_OL_TYPE else "ol")
            self.out.append(self._item(tag, level) + _runs_html(runs))
        else:
            self._p(_runs_html(runs))

    # ------------------------------------------------------------------ paragraf
    def _p(self, inner: str, tag: str = "p"):
        self.end_list()
        self.out.append(f"<{tag}>{inner}</{tag.split()[0]}>")

    def header(self, text: str):
        pass                      # HTML tidak punya header halaman

    def title(self, title: str, subtitle: str = ""):
        self._p(f"<strong>{html.escape(title)}</strong>", f'p style="font-size:{PARA["title"]["size"]}pt"')
        if subtitle:
            self._p(html.escape(subtitle))

    def heading(self, text: str, level: int):
        self._p(html.escape(text), {1: "h1", 2: "h2"}.get(level, "p"))

    def label(self, text: str):
        self._p(html.escape(text))

    def para(self, text: str):
        self._p(html.escape(text))

    def note(self, text: str):
        self._p(f"<small>{html.escape(text)}</small>")

    def figures_label(self):
        self._p(html.escape(FIGURES_LABEL))

    def spacer(self):
        pass

    # ------------------------------------------------------------------ tabel
    def figures(self, items: list):
        """Sama dengan ReportWriter.figures: satu tabel per slide, gambar | keterangan; wide = colspan."""
        if not items:
            return
        pct = ICON_PCT if all(layout == "icon" for _, _, layout in items) else FIG_PCT
        shade = f"background:#{CAPTION_FILL}"
        rows = []
        for img, caption, layout in items:
            src = html.escape(self.img_src(Path(img)))
            cap = html.escape(caption)
            if layout == "wide":
                rows.append(f'<tr><td colspan="2" style="text-align:center">'
                            f'<img src="{src}" style="max-width:100%;height:auto"></td></tr>')
                if caption:
                    rows.append(f'<tr><td colspan="2" style="{shade}"><strong>{cap}</strong></td></tr>')
                continue
            icon = layout == "icon"
            size = f'width="{ICON_PX}"' if icon else 'style="max-width:100%;height:auto"'
            rows.append(f'<tr><td style="width:{pct[0]}%;text-align:center"><img src="{src}" {size}></td>'
                        f'<td style="width:{pct[1]}%;{shade}">'
                        f'{cap if icon or not cap else f"<strong>{cap}</strong>"}</td></tr>')
        self.end_list()
        self.out.append(_HTML_TABLE + "".join(rows) + "</tbody></table>")

    def table(self, rows: list):
        ncols = max((len(r) for r in rows), default=0)
        if not ncols:
            return
        out = []
        for i, r in enumerate(rows):
            cells = []
            for val in list(r) + [""] * (ncols - len(r)):
                s = "<br>".join(html.escape(line.strip()) for line in (val or "").split("\n"))
                if i == 0:
                    cells.append(f'<td style="width:{100 / ncols:.0f}%;background:#{CAPTION_FILL}">'
                                 f'{f"<strong>{s}</strong>" if s else ""}</td>')
                else:
                    cells.append(f"<td>{s}</td>")
            out.append("<tr>" + "".join(cells) + "</tr>")
        self.end_list()
        self.out.append(_HTML_TABLE + "".join(out) + "</tbody></table>")

    def fragment(self) -> str:
        self.end_list()
        return "\n".join(self.out)

    def save(self, path: Path, title: str = ""):
        Path(path).parent.mkdir(parents=True, exist_ok=True)
        Path(path).write_text(html_document(self.fragment(), title or Path(path).stem), encoding="utf-8")


class Tee:
    """Panggilan writer yang sama ke beberapa writer (DOCX, HTML, ...); None dilewati."""

    def __init__(self, *writers):
        self.writers = [w for w in writers if w is not None]

    def __getattr__(self, name):
        def call(*args, **kwargs):
            for w in self.writers:
                getattr(w, name)(*args, **kwargs)
        return call


def make_template(example: Path, out: Path = DEFAULT_TEMPLATE) -> Path:
    """Template = contoh hasil yang benar tanpa isi: style, ukuran halaman, header/footer tetap;
    isi body dan gambar dibuang, teks header dikosongkan (diisi judul deck saat konversi)."""
    doc = Document(str(example))
    body = doc.element.body
    for el in list(body):
        if el.tag != qn("w:sectPr"):
            body.remove(el)
    for rid, rel in list(doc.part.rels.items()):
        if rel.reltype == RT.IMAGE:
            doc.part.drop_rel(rid)
    for sec in doc.sections:
        for p in sec.header.paragraphs:
            for r in p.runs:
                r.text = ""
    doc.save(str(out))
    return out


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="Buat template laporan dari contoh DOCX yang benar")
    ap.add_argument("--make-template", metavar="CONTOH_DOCX", required=True)
    ap.add_argument("-o", "--output", default=str(DEFAULT_TEMPLATE))
    a = ap.parse_args()
    print(make_template(Path(a.make_template), Path(a.output)))
