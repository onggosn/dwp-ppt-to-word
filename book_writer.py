"""DOCX berformat buku ringkasan (contoh: docs/new/RDGB_Maret 2026_Buku 2d ....pdf). Hanya urusan format; isi
dan urutan datang dari book_engine.

Format:
  - judul buku, lalu bab ("1. ...", Heading 1) dan bagian ("1.1 ...", Heading 2); nomor ditulis sebagai teks
  - teks bab/bagian (gaya "text"): sub-judul, label kapital, paragraf, bullet Word, butir bernomor dengan
    label apa adanya ("a.", "1.", "i.") dan indentasi gantung, tabel Word, gambar dengan keterangan
  - indentasi seperti contoh: bab rata kiri, bagian sedikit menjorok, label/paragraf/butir lebih menjorok
  - kotak topik (gaya "topic"; contoh: docs/new/RDGB_Maret 2026_Buku 1a Asesmen Moneter.pdf): tabel berbingkai
    berisi judul, lalu satu baris per panel (grafik/tabel slide): gambar kiri, butir panel itu di kanan; panel
    yang lebar (tabel besar) memakai seluruh lebar kotak dengan butir di bawahnya
  - komentar Word (opsional) untuk hal yang perlu dicek, mis. angka yang tidak ditemukan di slide

Teks blok boleh memakai **tebal** dan *miring* (Markdown) dari LLM.
"""
from __future__ import annotations

import html
import re
from pathlib import Path
from typing import Callable

from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Emu, Pt, Twips

from report_writer import (DEFAULT_TEMPLATE, _abstract_num, _cell_props, _el, _picture_size, _runs_html,
                           _style_run, _table_props, html_document, img_data_uri, review_comment, review_mark)

TEXT_W = 9020                         # lebar teks A4 (twips), sama dengan report_writer
CELL_PAD = 120
PANEL_COLS = (5100, 3920)             # baris panel di kotak topik: gambar | butir
TITLE_FILL = "F2F6FA"
ITEM_INDENT = 400                     # twips per level butir bernomor (di dalam kotak)
# indentasi badan teks (twips dari margin kiri), diukur dari contoh buku
SECTION_INDENT = 220                  # "1.1 ..."
BODY_INDENT = 600                     # label (KESIMPULAN), sub-judul, paragraf
BULLET_INDENT = 720                   # tanda bullet level 0
LIST_TEXT = 960                       # teks bullet level 0; nomor butir level 0 (list bernomor masuk ke dalam)
ITEM_TEXT = 1260                      # teks butir bernomor level 0
LEVEL_STEP = 360                      # tambahan per level
NO_SECTION_SHIFT = -300               # isi langsung di bawah bab (tanpa "1.1"): semua indentasi badan lebih dangkal
MAX_IMG_H = int(6.2 * 914400)         # gambar di badan teks paling tinggi ~6,2"
BOX_IMG_H = int(4.0 * 914400)         # gambar dalam kotak topik paling tinggi 4" (kira-kira dua kotak per halaman)
PANEL_IMG_H = int(3.6 * 914400)       # gambar panel di kolom kiri

PARA = {
    "book_title": dict(size=14, bold=True, before=0, after=360),
    "chapter": dict(style="Heading1", size=11, bold=True, before=360, after=160),
    "section": dict(style="Heading2", size=11, bold=True, before=240, after=160, indent=SECTION_INDENT),
    "heading": dict(size=11, bold=True, before=200, after=80),
    "label": dict(size=11, bold=True, before=160, after=60),
    "para": dict(size=11, after=100, line=1.15, justify=True),
    "bullet": dict(size=11, after=60, line=1.15, justify=True),
    "item": dict(size=11, after=60, line=1.15, justify=True),
    "box_title": dict(size=11, bold=True, after=0, align="center"),
    "caption": dict(size=10, bold=True, before=120, after=60, align="center"),
    "panel_caption": dict(size=10, bold=True, after=60),
    "small": dict(size=9, after=0),
}

_MD_TOKEN = re.compile(r"\*\*|\*")


def md_runs(text: str) -> list:
    """'**tebal** dan *miring*' -> [(teks, tebal, miring)]. Boleh bersarang ('**K2: *funding***'); penanda yang
    tidak berpasangan (mis. catatan kaki '*)') tetap teks biasa."""
    parts, last = [], 0
    for m in _MD_TOKEN.finditer(text or ""):
        parts.append(text[last:m.start()])
        parts.append(m.group())
        last = m.end()
    parts.append((text or "")[last:])
    for marker in ("**", "*"):          # penanda terakhir yang tidak berpasangan -> teks
        idx = [i for i, p in enumerate(parts) if i % 2 and p == marker]
        if len(idx) % 2:
            parts[idx[-1]] = "\0" + marker
    runs, bold, italic = [], False, False
    for i, p in enumerate(parts):
        if i % 2 and p == "**":
            bold = not bold
        elif i % 2 and p == "*":
            italic = not italic
        elif p:
            p = p.replace("\0", "")
            if runs and runs[-1][1:] == (bold, italic):
                runs[-1] = (runs[-1][0] + p, bold, italic)
            else:
                runs.append((p, bold, italic))
    return runs


def plain(text: str) -> str:
    return "".join(t for t, _, _ in md_runs(text))


class BookWriter:
    def __init__(self, template: Path = DEFAULT_TEMPLATE):
        self.doc = Document(str(template))
        body = self.doc.element.body
        for el in list(body):
            if el.tag != qn("w:sectPr"):
                body.remove(el)
        for sec in self.doc.sections:        # header template berisi judul laporan; buku tidak memakainya
            for p in sec.header.paragraphs:
                for r in list(p.runs):
                    r._r.getparent().remove(r._r)
        self._bullet_abstract = None
        self._bullet_num = None
        self.shift = 0                    # NO_SECTION_SHIFT setelah judul bab, 0 setelah judul bagian

    # ------------------------------------------------------------------ paragraf
    def _para(self, kind: str, container=None, fresh_cell: bool = False):
        if fresh_cell:
            p = container.paragraphs[0]
        else:
            p = (container or self.doc).add_paragraph()
        f = PARA[kind]
        if f.get("style"):
            p._p.get_or_add_pPr().style = f["style"]
        pf = p.paragraph_format
        pf.space_before = Twips(f.get("before", 0))
        pf.space_after = Twips(f.get("after", 0))
        if "line" in f:
            pf.line_spacing = f["line"]
        if "indent" in f:
            pf.left_indent = Twips(f["indent"])
        if f.get("align") == "center":
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        elif f.get("justify"):
            p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        return p

    def _runs(self, p, kind: str, runs: list):
        f = PARA[kind]
        for text, b, i in runs:
            _style_run(p.add_run(text), f.get("size"), b or f.get("bold", False), None, i)

    def _text(self, kind: str, text: str, container=None, fresh_cell=False):
        p = self._para(kind, container, fresh_cell)
        self._runs(p, kind, md_runs(text))
        return p

    def _bullet_id(self) -> str:
        """Satu list bullet untuk seluruh dokumen (bullet tidak perlu mulai ulang)."""
        if self._bullet_num is None:
            numbering = self.doc.part.numbering_part.element
            ids = [int(a.get(qn("w:abstractNumId"))) for a in numbering.findall(qn("w:abstractNum"))]
            an = _abstract_num(max(ids, default=0) + 1, "bullet")
            first_num = numbering.find(qn("w:num"))
            if first_num is not None:
                first_num.addprevious(an)
            else:
                numbering.append(an)
            num_id = max((int(n.get(qn("w:numId"))) for n in numbering.findall(qn("w:num"))), default=0) + 1
            num = _el("w:num", numId=num_id)
            num.append(_el("w:abstractNumId", val=an.get(qn("w:abstractNumId"))))
            numbering.append(num)
            self._bullet_num = str(num_id)
        return self._bullet_num

    def _bullet(self, text: str, level: int, container=None, fresh_cell=False):
        level = min(max(level, 0), 6)
        p = self._para("bullet", container, fresh_cell)
        pr = p._p.get_or_add_pPr()
        numpr = OxmlElement("w:numPr")
        numpr.append(_el("w:ilvl", val=level))
        numpr.append(_el("w:numId", val=self._bullet_id()))
        pr.insert(1 if pr.find(qn("w:pStyle")) is not None else 0, numpr)
        if container is None:             # badan teks: menjorok seperti contoh; di kotak: indentasi list bawaan
            pf = p.paragraph_format
            pf.left_indent = Twips(LIST_TEXT + LEVEL_STEP * level + self.shift)
            pf.first_line_indent = Twips(BULLET_INDENT - LIST_TEXT)
        self._runs(p, "bullet", md_runs(text))

    def _item(self, label: str, text: str, level: int, container=None, fresh_cell=False):
        """Butir bernomor dengan label apa adanya ("a.", "2.", "ii.") dan indentasi gantung."""
        level = min(max(level, 0), 6)
        p = self._para("item", container, fresh_cell)
        pf = p.paragraph_format
        if container is None:
            left, hang = ITEM_TEXT + LEVEL_STEP * level + self.shift, ITEM_TEXT - LIST_TEXT
        else:
            left, hang = ITEM_INDENT * (level + 1), ITEM_INDENT
        pf.left_indent = Twips(left)
        pf.first_line_indent = Twips(-hang)
        pf.tab_stops.add_tab_stop(Twips(left))
        self._runs(p, "item", [(label.strip() + "\t", False, False)] + md_runs(text))

    # ------------------------------------------------------------------ struktur
    def title(self, text: str):
        self._text("book_title", text)

    def chapter(self, number: str, text: str):
        self._text("chapter", f"{number}. {text}").paragraph_format.keep_with_next = True
        self.shift = NO_SECTION_SHIFT

    def section(self, number: str, text: str):
        self._text("section", f"{number} {text}").paragraph_format.keep_with_next = True
        self.shift = 0

    def blocks(self, blocks: list, container=None):
        """Blok teks (lihat book_engine): heading, label, para, bullet, item, table, figure.
        container: sel tabel (kotak topik) atau None (badan dokumen)."""
        fresh = container is not None and not container.paragraphs[0].text and \
            not container.paragraphs[0]._p.findall(qn("w:r"))
        for b in blocks:
            t = b["type"]
            if t in ("heading", "label", "para"):
                p = self._text(t, b["text"], container, fresh)
                if container is None:
                    p.paragraph_format.left_indent = Twips(BODY_INDENT + self.shift)
            elif t == "bullet":
                self._bullet(b["text"], b.get("level", 0), container, fresh)
            elif t == "item":
                self._item(b.get("label", ""), b["text"], b.get("level", 0), container, fresh)
            elif t == "table":
                if fresh:                     # sel kosong: paragraf pertamanya dipakai keterangan / dibiarkan
                    fresh = False
                self.table(b["rows"], container, b.get("caption", ""))
                continue
            elif t == "figure":
                self.figure(b["img"], b.get("caption", ""), container, fresh)
            fresh = False

    def figure(self, img: Path, caption: str = "", container=None, fresh_cell=False):
        if caption:
            self._text("caption", caption, container, fresh_cell)
            fresh_cell = False
        p = self._para("para", container, fresh_cell)
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        width = (TEXT_W - 2 * CELL_PAD) * 635 if container is None else (TEXT_W - 4 * CELL_PAD) * 635
        w, h = _fit(img, width, MAX_IMG_H)
        p.add_run().add_picture(str(img), width=Emu(w), height=Emu(h))

    def table(self, rows: list, container=None, caption: str = ""):
        ncols = max((len(r) for r in rows), default=0)
        if not ncols:
            return
        if caption:
            self._text("caption", caption, container)
        total = TEXT_W if container is None else TEXT_W - 2 * CELL_PAD
        widths = [total // ncols] * ncols
        widths[-1] += total - sum(widths)
        size = 8 if ncols > 4 else 9
        t = (container or self.doc).add_table(rows=0, cols=ncols)
        _table_props(t, widths)
        for i, r in enumerate(rows):
            cells = t.add_row().cells
            for c, val, w in zip(cells, list(r) + [""] * (ncols - len(r)), widths):
                _cell_props(c, w, TITLE_FILL if i == 0 else None, (40, 80, 40, 80))
                for k, line in enumerate((val or "").split("\n")):
                    p = c.paragraphs[0] if k == 0 else c.add_paragraph()
                    p.paragraph_format.space_after = Twips(0)
                    if line.strip():
                        _style_run(p.add_run(line.strip()), size, i == 0)
        self._para("small", container)

    def topic(self, title: str, blocks: list, panels: list, after: list = ()):
        """Kotak topik: judul, butir umum (kalau ada), satu baris per panel, lalu butir `after`.
        panels = [(gambar, keterangan, butir panel, lebar?)]: panel biasa = gambar kiri | butir kanan;
        panel lebar atau tanpa butir = gambar selebar kotak, butirnya di bawah."""
        cols = list(PANEL_COLS)
        t = self.doc.add_table(rows=0, cols=2)
        _table_props(t, cols)
        pad = (CELL_PAD, CELL_PAD, CELL_PAD, CELL_PAD)

        def full_row():
            cells = t.add_row().cells
            cell = cells[0].merge(cells[1])
            _cell_props(cell, sum(cols), None, pad)
            return cell

        if title:
            cell = full_row()
            _cell_props(cell, sum(cols), TITLE_FILL, pad)
            self._text("box_title", title, cell, True).paragraph_format.keep_with_next = True
            _cant_split(t.rows[-1])
        if blocks:
            cell = full_row()
            self.blocks(blocks, cell)
            if panels:                    # butir pembuka tetap satu halaman dengan panel pertama
                for p in cell.paragraphs:
                    p.paragraph_format.keep_with_next = True
        for img, caption, pblocks, wide in panels:
            if wide or not pblocks:
                cell = full_row()
                self._box_figure(cell, img, caption, (sum(cols) - 2 * CELL_PAD) * 635, BOX_IMG_H)
                if pblocks:
                    self.blocks(pblocks, cell)
            else:
                img_cell, txt_cell = t.add_row().cells
                _cell_props(img_cell, cols[0], None, pad)
                _cell_props(txt_cell, cols[1], None, pad)
                _valign_top(img_cell)
                _valign_top(txt_cell)
                self._box_figure(img_cell, img, caption, (cols[0] - 2 * CELL_PAD) * 635, PANEL_IMG_H)
                self.blocks(pblocks, txt_cell)
            _cant_split(t.rows[-1])
        if after:
            self.blocks(list(after), full_row())
        self._para("para")

    def _box_figure(self, cell, img: Path, caption: str, width: int, max_h: int = BOX_IMG_H):
        fresh = True
        if caption:                       # judul panel di atas gambar, rata kiri seperti contoh (baris tidak terpotong,
            self._text("panel_caption", caption, cell, True)    # jadi tanpa keep_with_next yang merantai baris)
            fresh = False
        p = self._para("small", cell, fresh)
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        w, h = _fit(img, width, max_h)
        p.add_run().add_picture(str(img), width=Emu(w), height=Emu(h))

    # ------------------------------------------------------------------ komentar review
    def mark(self) -> int:
        return review_mark(self.doc)

    def comment(self, start: int, lines: list):
        review_comment(self.doc, start, lines)

    def save(self, path: Path):
        Path(path).parent.mkdir(parents=True, exist_ok=True)
        self.doc.save(str(path))


def _cant_split(row):
    """Baris tabel tidak dipotong di dua halaman (judul kotak tidak tertinggal sendiri)."""
    tr_pr = row._tr.get_or_add_trPr()
    tr_pr.append(_el("w:cantSplit"))


def _valign_top(cell):
    tc_pr = cell._tc.get_or_add_tcPr()
    tc_pr.append(_el("w:vAlign", val="top"))


def _fit(img: Path, width: int, max_h: int) -> tuple:
    w, h = _picture_size(img, width)
    if h > max_h:
        w, h = round(w * max_h / h), max_h
    return w, h


# --------------------------------------------------------------------------- HTML (CKEditor)
def _px(twips: int) -> int:
    return round(twips / 15)



class BookHtmlWriter:
    """Isi buku yang sama dengan BookWriter sebagai HTML bersih untuk CKEditor: h1/h2/h3, p, ul, tabel berbingkai
    untuk kotak topik. img_src: path gambar -> nilai src (default data URI)."""

    BOX = 'border="1" cellpadding="6" style="border-collapse:collapse;width:100%;margin:0 0 12px"'

    def __init__(self, img_src: Callable[[Path], str] = img_data_uri):
        self.parts = []
        self.img_src = img_src
        self.shift = 0

    @staticmethod
    def _md(text: str) -> str:
        return _runs_html(md_runs(text))

    def title(self, text: str):
        self.parts.append(f"<h1>{html.escape(text)}</h1>")

    def chapter(self, number: str, text: str):
        self.parts.append(f"<h2>{html.escape(number)}. {html.escape(text)}</h2>")
        self.shift = NO_SECTION_SHIFT

    def section(self, number: str, text: str):
        self.parts.append(f'<h3 style="margin-left:{_px(SECTION_INDENT)}px">{html.escape(number)} '
                          f"{html.escape(text)}</h3>")
        self.shift = 0

    def _blocks(self, blocks: list, body: bool = False) -> str:
        """body: badan teks (menjorok seperti DOCX); False: isi sel kotak."""
        out, depth = [], -1          # depth: level <ul> bullet yang sedang terbuka
        ind = (lambda tw: f' style="margin-left:{_px(tw + self.shift)}px"') if body else (lambda tw: "")

        def close(to: int):
            nonlocal depth
            while depth > to:
                out.append("</ul>")
                depth -= 1

        for b in blocks:
            t = b["type"]
            if t == "bullet":
                lvl = min(max(b.get("level", 0), 0), 4)
                close(lvl)
                while depth < lvl:
                    out.append(f"<ul{ind(BULLET_INDENT) if depth < 0 else ''}>")
                    depth += 1
                out.append(f"<li>{self._md(b['text'])}</li>")
                continue
            close(-1)
            if t == "heading":
                out.append(f"<h4{ind(BODY_INDENT)}>{self._md(b['text'])}</h4>")
            elif t == "label":
                out.append(f"<p{ind(BODY_INDENT)}><strong>{self._md(b['text'])}</strong></p>")
            elif t == "para":
                out.append(f"<p{ind(BODY_INDENT)}>{self._md(b['text'])}</p>")
            elif t == "item":
                lvl = min(max(b.get("level", 0), 0), 6)
                pad = _px(ITEM_TEXT + LEVEL_STEP * lvl + self.shift) if body else 24 * (lvl + 1)
                hang = _px(ITEM_TEXT - LIST_TEXT) if body else 24
                out.append(f'<p style="margin-left:{pad}px;text-indent:-{hang}px">'
                           f"{html.escape(b.get('label', ''))}&nbsp;{self._md(b['text'])}</p>")
            elif t == "table":
                out.append(self._table(b["rows"], b.get("caption", "")))
            elif t == "figure":
                out.append(self._figure(b["img"], b.get("caption", "")))
        close(-1)
        return "".join(out)

    def _figure(self, img: Path, caption: str = "", align: str = "center") -> str:
        cap = f'<p style="text-align:{align}"><strong>{html.escape(caption)}</strong></p>' if caption else ""
        return f'{cap}<p style="text-align:center"><img src="{self.img_src(img)}" style="max-width:100%"></p>'

    @staticmethod
    def _table(rows: list, caption: str = "") -> str:
        cap = f'<p style="text-align:center"><strong>{html.escape(caption)}</strong></p>' if caption else ""
        body = "".join("<tr>" + "".join(
            (f"<th>{html.escape(c)}</th>" if i == 0 else f"<td>{html.escape(c)}</td>").replace("\n", "<br>")
            for c in r) + "</tr>" for i, r in enumerate(rows))
        return f'{cap}<table border="1" cellpadding="4" style="border-collapse:collapse;width:100%">{body}</table>'

    def blocks(self, blocks: list, container=None):
        self.parts.append(self._blocks(blocks, body=container is None))

    def figure(self, img: Path, caption: str = "", container=None, fresh_cell=False):
        self.parts.append(self._figure(img, caption))

    def table(self, rows: list, container=None, caption: str = ""):
        self.parts.append(self._table(rows, caption))

    def topic(self, title: str, blocks: list, panels: list, after: list = ()):
        rows = []
        if title:
            rows.append(f'<tr><td colspan="2" style="text-align:center;background:#{TITLE_FILL}">'
                        f"<strong>{self._md(title)}</strong></td></tr>")
        if blocks:
            rows.append(f'<tr><td colspan="2">{self._blocks(blocks)}</td></tr>')
        for img, caption, pblocks, wide in panels:
            fig = self._figure(img, caption, "left")
            if wide or not pblocks:
                rows.append(f'<tr><td colspan="2">{fig}{self._blocks(pblocks)}</td></tr>')
            else:
                rows.append(f'<tr><td style="width:56%;vertical-align:top">{fig}</td>'
                            f'<td style="vertical-align:top">{self._blocks(pblocks)}</td></tr>')
        if after:
            rows.append(f'<tr><td colspan="2">{self._blocks(list(after))}</td></tr>')
        self.parts.append(f"<table {self.BOX}>{''.join(rows)}</table>")

    def fragment(self) -> str:
        return "\n".join(self.parts)

    def save(self, path: Path, title: str = ""):
        Path(path).parent.mkdir(parents=True, exist_ok=True)
        Path(path).write_text(html_document(self.fragment(), title), encoding="utf-8")
