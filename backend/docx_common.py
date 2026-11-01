"""Bagian bersama penulis Word/HTML: template, gaya, gambar, tabel, dan komentar review
"Digital Workplace". Dipakai book_writer."""
from __future__ import annotations

import base64
import html
from pathlib import Path

from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Pt, RGBColor
from docx.text.paragraph import Paragraph
from PIL import Image


HERE = Path(__file__).resolve().parent
DEFAULT_TEMPLATE = HERE / "templates" / "report_template.docx"


FONT, FONT_EAST_ASIA = "Frutiger 45 Light", "SimSun"


MAX_IMG_H = 8 * 914400              # gambar setinggi ini atau lebih diperkecil supaya muat satu halaman
BORDER_COLOR = "BFBFBF"


REVIEWER, REVIEWER_INITIALS = "Digital Workplace", "DW"     # penulis komentar review di Word


def review_mark(doc) -> int:
    """Posisi akhir isi dokumen sekarang; review_comment(doc, mark, ...) menempel pada isi sesudahnya."""
    return len(doc.element.body) - 1                    # elemen terakhir body = sectPr


def review_comment(doc, start: int, lines: list):
    """Komentar Word dari REVIEWER pada paragraf berteks pertama sejak mark() (biasanya judul slide; bisa juga
    di dalam tabel). Satu baris = satu paragraf komentar."""
    if not lines:
        return
    for el in list(doc.element.body)[start:]:
        for p_el in el.iter(qn("w:p")):
            runs = [r for r in Paragraph(p_el, doc._body).runs if r.text.strip()]
            if runs:
                c = doc.add_comment(runs, lines[0], REVIEWER, REVIEWER_INITIALS)
                for line in lines[1:]:
                    c.add_paragraph(line)
                return


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


class Tee:
    """Panggilan writer yang sama ke beberapa writer (DOCX, HTML, ...); None dilewati."""

    def __init__(self, *writers):
        self.writers = [w for w in writers if w is not None]

    def __getattr__(self, name):
        def call(*args, **kwargs):
            for w in self.writers:
                getattr(w, name)(*args, **kwargs)
        return call
