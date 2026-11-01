"""PPTX -> DOCX berformat *buku ringkasan* (Full AI). Contoh hasil yang benar:
docs/new/RDGB_Maret 2026_Buku 2d Pokok Pembahasan dan Rancangan Bauran Kebijakan.pdf (dari deck di folder yang sama).

Alur:
  1. extract   render tiap slide (PowerPoint / LibreOffice) dan ambil elemennya dengan id e1, e2, ...
               (report_engine.extract: koordinat, teks, tabel).
  2. outline   satu panggilan LLM (teks saja) atas seluruh deck: judul buku, bab, bagian, dan slide mana yang
               masuk ke bagian mana dengan gaya apa. Sampul, agenda, pembatas, lampiran, dan catatan kerja
               dilewati. Satu slide boleh dipakai beberapa bagian dengan "focus" (mis. satu kolom saja).
  3. write     per slide terpilih satu panggilan LLM (render + elemen), paralel:
                 topic  kotak: judul (pesan kunci), gambar grafik/tabel, butir ringkasan
                 text   teks buku hampir kata per kata (kesimpulan, rancangan kebijakan), tabel PowerPoint
                        ditulis dari data aslinya
               Gambar tidak dibuat LLM: LLM hanya memilih id elemen, lalu area itu di-crop dari render slide.
               Jawaban divalidasi (id ada, tipe blok dikenal); gagal -> satu kali perbaikan, lalu cadangan
               (judul slide + render utuh).
  4. check     angka di teks buatan LLM yang tidak ada di teks slide ditandai (komentar Word), karena bisa
               saja dibaca dari grafik atau salah tulis.
  5. docx      book_writer.

Jawaban LLM disimpan di cache (work/book_cache) per isi prompt + gambar, jadi menjalankan ulang tidak memanggil
LLM lagi untuk slide yang tidak berubah.

CLI:
    python book_engine.py "docs/new/DKEM RDGB Maret 2026_06_Materi Hari Kedua_afterRDG.pptx" -o work/buku.docx
    python book_engine.py deck.pptx -o work/buku.docx --title "Buku 2d ..." --workers 6
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass, field
from pathlib import Path
from typing import Callable, Optional

from pptx import Presentation

import bedrock_llm
import layout_engine as le
import report_engine as re_
from book_writer import BookHtmlWriter, BookWriter, plain
from report_writer import DEFAULT_TEMPLATE, Tee

HERE = Path(__file__).resolve().parent
DEFAULT_CACHE = HERE / "work" / "book_cache"
DEFAULT_MODEL = bedrock_llm.DEFAULT_MODEL
BOOK_VERSION = "4"            # naikkan kalau prompt / skema berubah supaya cache lama tidak dipakai

OUTLINE_SLIDE_CHARS = 1400    # teks per slide di prompt kerangka
OUTLINE_EL_CHARS = 350
ITEM_EL_CHARS = 2500          # teks per elemen di prompt per slide
ITEM_TABLE_ROWS = 6
PREV_TAIL_CHARS = 500         # akhir teks slide sebelumnya (untuk slide lanjutan)
MAX_FIGURES = 5               # panel per kotak
SIDE_ASPECT = 1.1             # gambar gabungan (satu panel) di bawah rasio lebar/tinggi ini ditaruh di samping butir
PANEL_WIDE_ASPECT = 3.5       # panel terpisah di atas rasio ini (mis. tabel lebar) memakai seluruh lebar kotak
FIX_ATTEMPTS = 1
MAX_NUMBER_NOTES = 6          # angka yang dikutip satu per satu di komentar review
NUMBER_CONTEXT_CHARS = 45     # panjang potongan kalimat di kiri/kanan angka
BLOCK_TYPES = {"heading", "label", "para", "bullet", "item", "table", "figure"}
PANEL_BLOCK_TYPES = {"para", "bullet", "item"}
MAX_CAPTION_WORDS = 7         # keterangan panel yang lebih panjang = kalimat judul (headline) -> jadi butir
STYLES = ("topic", "text")

ProgressFn = Callable[[float, str], None]


def _noop(_f: float, _m: str) -> None:
    pass


# --------------------------------------------------------------------------- prompt
# Prompts are in English; everything the model writes into the book is Indonesian, copied from the slides.
OUTLINE_PROMPT = """You are planning a SUMMARY BOOK (a formal Word document written in Indonesian) made from a meeting's
PowerPoint deck. Below are all slides of the deck: number, layout name, count of charts/pictures/tables, and their
text (truncated).

Your task: decide the book's outline and which slides go into each section.

Example of a correct book, made from a Bank Indonesia Board of Governors meeting (RDG) deck:
  1. Kesimpulan Diskusi Hari 1 dan Arahan ADG
     1.1 Kesimpulan dan Arahan Moneter          <- one three-column summary slide; each section uses one column (focus)
     1.2 Kesimpulan dan Arahan Makroprudensial
     1.3 Kesimpulan dan Arahan Sistem Pembayaran
  2. Pokok Pembahasan dan Rancangan Kebijakan
     2.1 Pokok Pembahasan dan Rancangan Kebijakan Moneter      <- key-message slides (K1, K2, ...) and recommendation
     2.2 Pokok Pembahasan dan Rancangan Kebijakan Makroprudensial   slides (#1, R1, ...) with charts: style "topic"
     2.3 Pokok Pembahasan dan Rancangan Kebijakan Sistem Pembayaran
  3. Rancangan Bauran Kebijakan Bank Sentral
     3.1 Kebijakan Moneter                      <- text slides "Rekomendasi Bauran Kebijakan (1)...(n)": style "text".
     3.2 Kebijakan Makroprudensial                 3.1 covers ALL monetary policy: interest rate, monetary operations,
     3.3 Kebijakan Sistem Pembayaran               exchange-rate stabilisation, FX reserves (do not split it)
     3.4 Kebijakan Pendukung
     3.5 Koordinasi Kebijakan
     3.6 Tema Komunikasi dan Pokok-Pokok Komunikasi Kebijakan
  Left out: cover, agenda, chapter divider slides, closing slide, the APPENDIX (LAMPIRAN) and every slide after the
  appendix title, media/public-communication assessments, empty slides.
Follow this pattern when the deck is similar: the three chapters above, with the policy areas (Moneter,
Makroprudensial, Sistem Pembayaran) as SECTIONS inside a chapter, never as chapters of their own. For other decks
build an equivalent structure (chapter = major topic, section = subtopic).

Style per slide:
  "topic"  slide with a key message plus charts/tables/diagrams -> written as a box: title, picture, summary bullets.
  "text"   slide whose content is long text (conclusions, directives, policy recommendation points) -> written out
           as full text.

Rules:
- The book follows the deck's order: chapters and sections come in the order of their blocks in the deck, and a slide
  goes into the section where it sits in the deck (between two divider slides). Never move a slide to another
  chapter because of its topic; e.g. policy response/recommendation slides with charts inside the monetary block stay
  in the monetary section of chapter 2. Exception: a summary slide split per column.
- In the example pattern, chapter 3 only holds the text slides with recommendation points (the block of the deck
  after the divider "BUTIR REKOMENDASI BAURAN KEBIJAKAN"), grouped into sections 3.1-3.6.
- Set "focus" only when the section uses part of a slide (e.g. "kolom MONETER saja"); otherwise "".
- Record every slide that is not used in "skipped" with a short reason.
- Chapter and section titles in Indonesian, without numbers (the program numbers them), capitalised like the example.
- "title" = the book title, e.g. "<meeting name and period>_Buku <topic>"; take the meeting name and date from the
  cover slide.

Answer ONLY with JSON (no other text):
{{"title": "...",
  "chapters": [{{"title": "...", "sections": [{{"title": "...", "items": [{{"slide": 5, "style": "topic", "focus": ""}}]}}]}}],
  "skipped": [{{"slide": 1, "reason": "cover"}}]}}
A chapter without subsections may hold one section with "title": "".

SLIDES:
{slides}
"""

COMMON_RULES = """Content rules:
- Write in Indonesian, using the slide's own sentences and terms; you may shorten them and keep the slide's
  abbreviations (shg, dg, yg, NT, PDB, ...).
- NEVER add facts, numbers, or conclusions that are not on the slide. Copy numbers, percentages, dates, and names
  exactly.
- Ignore the authors' working notes: "Updated", "Need update", "DONE", "TBU", "Mohon bantuan ...", "Courtesy ...",
  "Will be updated", timestamps such as "Updated 05.00 WIB", revision comments/stickers, page numbers, template labels
  ("HASIL PEMBAHASAN DEWAN GUBERNUR").
- Lists of codes/identifiers are not quantities: e.g. "Bank Rerata AL/DPK < 10%: 097, 485" lists bank codes,
  so write "bank 097 dan 485", never "97 dan 485 bank". Copy codes exactly, leading zeros included.
- Do not end a title or sentence with "..." or "…".
- You may use Markdown **bold** and *italic*: italic for foreign terms (e.g. *safe haven*), bold for emphasis.
"""

TOPIC_PROMPT = """You are writing one box of a SUMMARY BOOK (in Indonesian) from one PowerPoint slide.
Book section: "{section}".{focus}
The slide render is attached. Slide elements (id, kind, position x/y and size w/h in % of the slide, content):
{elements}

The box is laid out like the example book: the box title, then ONE ROW PER PANEL of the slide. A row shows the
panel's chart/table cropped from the slide on the left and that panel's own bullet points on the right. So a slide
with four titled charts, each with its explanation text, becomes four rows, not one picture of the whole slide.

Answer fields:
- "title": the box title = the slide's main key message, one sentence (usually the slide title; drop page numbers
  and "...").
- "figures": the panels, in the slide's reading order, each {{"ids": [...], "caption": "...", "blocks": [...]}}.
  * Split: every chart, table, or diagram that has its own panel title or its own explanatory text is a SEPARATE
    figure. Put elements into one figure only when they form one picture together (a chart with its legend, axis
    labels and source note; small charts that share one title and one explanation). At most {max_fig}.
  * ids = the elements that make up the picture: the chart/table/picture itself, labels drawn on it, its legend and
    source note. Do NOT include text boxes whose content you write as bullets, the slide title, logos, page numbers,
    template labels, or working notes. If the slide's content is one large picture (a screenshot), use that
    picture's id.
  * A panel's HEADLINE BANNER (a sentence in a coloured/filled box above or over the chart that states the
    panel's message, e.g. "HARGA MINYAK NAIK LEBIH TINGGI BILA TENSI PERANG & KERUSAKAN MENINGKAT") is NOT part
    of the picture: leave it out of ids and write it as the FIRST bullet of that panel's blocks, in normal
    sentence case ("Harga minyak naik lebih tinggi bila tensi perang & kerusakan meningkat ..."). A short chart
    title printed inside the chart (e.g. "Asumsi Minyak Brent RDG Mar 2026") stays in the picture.
  * caption = the panel's short title as written on the slide, without its number (e.g. "NPI 2026",
    "DAMPAK KONFLIK KE PDB DAN INFLASI"), at most {max_words} words, only when that title is a separate text box
    on the slide (not text inside the chart picture); otherwise "". Never a headline banner (that is a bullet).
  * Infographics are NOT split: a diagram built from shapes, icons, arrows and small text boxes that reads as one
    picture (e.g. a policy-mix diagram, a transmission-channel scheme, a framework) is ONE figure with
    "full": true; its ids are all elements of the diagram. A full figure is shown across the whole box width with
    its points written below it. A slide that is one infographic gives one full figure. Parts of a diagram that are
    joined by arrows, a shared background, or one framework drawn across the slide are ONE figure; never cut a
    diagram into its boxes. Charts and number tables beside a diagram are still separate figures.
  * blocks = 1-4 points that explain THIS panel. Every chart or table needs its explanation next to it: take the
    text that belongs to it on the slide (its explanation box next to / above / below it, its message), and when
    the slide only has one key-message box for all panels, give each point of that box to the panel it talks
    about: {{"type": "bullet", "text": "..."}}, or
    {{"type": "item", "label": "a.", "text": "...", "level": 0}} when the slide numbers them. [] if the slide has
    no text for this panel.
  A slide without charts: "figures": [].
- "blocks": points that belong to no single panel (an overall conclusion of the slide), or all points of a
  slide without charts. 0-6 points; you may use {{"type": "para", "text": "..."}} for an introductory sentence.
  Never repeat a point already written under a panel.

{rules}
Answer ONLY with JSON:
{{"title": "...", "figures": [{{"ids": ["e3", "e4"], "caption": "", "full": false, "blocks": [...]}}], "blocks": [...]}}
"""

TEXT_PROMPT = """You are writing the content of one slide as BOOK TEXT (in Indonesian), almost word for word.
Book section: "{section}".{focus}{prev}
The slide render is attached. Slide elements (id, kind, position x/y and size w/h in % of the slide, content):
{elements}

"blocks" holds, in slide order:
  {{"type": "heading", "text": "..."}}            sub-heading inside the section (e.g. "Kebijakan Suku Bunga BI-Rate")
  {{"type": "label", "text": "KESIMPULAN"}}         short all-caps label
  {{"type": "para", "text": "..."}}                 paragraph
  {{"type": "bullet", "text": "...", "level": 0}}   bullet point (level 0, 1, 2)
  {{"type": "item", "label": "a.", "text": "...", "level": 1}}
                                                   numbered/lettered point: copy its number/letter from the slide
                                                   ("1.", "a.", "i.", "(i)"); level = depth (0 = outermost)
  {{"type": "table", "id": "e7", "caption": "Tabel 1. ..."}}
                                                   a PowerPoint table (kind table); the program writes its cells
                                                   from the slide
  {{"type": "figure", "ids": ["e9"], "caption": "..."}}
                                                   a table/chart/diagram that is a picture, cropped from the render
Text rules:
- Do not write a slide title that only marks the sequence (e.g. "Rekomendasi Bauran Kebijakan RDG Maret 2026 (3)")
  or only restates the book section (e.g. "Kesimpulan Diskusi Hari 1 dan Arahan ADG - Mei 2025: Moneter" in the
  section "Kesimpulan dan Arahan Moneter").
- If the slide continues the previous slide (title ending in "(lanjutan)", point numbers continuing), do not repeat
  the sub-heading or introductory sentence already written; just continue the content.
- A point number already present in the slide text goes into "label"; do not repeat it in "text".

{rules}
Answer ONLY with JSON: {{"blocks": [...]}}
"""

FIX_PROMPT = """

Your previous answer could not be used:
{errors}
Previous answer:
{previous}
Fix it and answer again with ONLY valid JSON in the format above."""


# --------------------------------------------------------------------------- model
@dataclass
class Slide:
    n: int
    layout: str
    els: dict                      # id -> layout_engine.Box
    render: Optional[Path] = None

    @property
    def title(self) -> str:
        t = next((b for b in self.els.values() if b.kind == "text" and b.is_title and re_.box_text(b)), None)
        if t is None:
            texts = sorted((b for b in self.els.values() if b.kind == "text" and re_.box_text(b)),
                           key=lambda b: (round(b.y, 2), b.x))
            t = texts[0] if texts else None
        return re_.box_text(t) if t else ""

    def texts(self) -> list:
        """Teks elemen urut atas -> bawah, kiri -> kanan."""
        out = []
        for b in sorted(self.els.values(), key=lambda b: (round(b.y, 2), b.x)):
            if b.kind == "text" and re_.box_text(b):
                out.append(re_.box_text(b))
            elif b.kind == "table":
                out.append(" | ".join(c for r in b.rows for c in r if c.strip()))
        return out

    def source_text(self) -> str:
        return "\n".join(self.texts())


@dataclass
class Item:
    chapter: int                   # indeks bab (0-based)
    section: int                   # indeks bagian dalam bab
    slide: int
    style: str = "topic"
    focus: str = ""
    result: dict = field(default_factory=dict)
    warnings: list = field(default_factory=list)
    source: str = "llm"            # llm | cache | fallback


# --------------------------------------------------------------------------- LLM
def _cache_path(cache_dir: Optional[Path], prompt: str, image: Optional[bytes], model: str) -> Optional[Path]:
    if not cache_dir:
        return None
    h = hashlib.sha256("|".join((BOOK_VERSION, model, prompt)).encode())
    if image:
        h.update(image)
    return Path(cache_dir) / f"{h.hexdigest()[:32]}.json"


def ask_json(prompt: str, image: Optional[bytes], provider: str, model: str, cache_dir: Optional[Path],
             validate: Callable[[dict], list]) -> tuple:
    """(data atau None, kesalahan, dari cache?). Satu kali perbaikan kalau jawaban tidak sah."""
    import llm_planner   # provider SDK dimuat hanya kalau dipakai

    cache = _cache_path(cache_dir, prompt, image, model)
    if cache and cache.exists():
        try:
            data = json.loads(cache.read_text(encoding="utf-8"))["data"]
            if not validate(data):
                return data, [], True
        except (ValueError, KeyError):
            pass
    ask, history = prompt, []
    for _ in range(FIX_ATTEMPTS + 1):
        raw = llm_planner.call_llm(ask, image, provider, model)
        try:
            data = _parse(raw)
        except ValueError as e:
            errors = [f"the answer is not valid JSON ({e})"]
        else:
            errors = validate(data)
            if not errors:
                if cache:
                    cache.parent.mkdir(parents=True, exist_ok=True)
                    cache.write_text(json.dumps({"data": data, "model": model,
                                                 "created": time.strftime("%Y-%m-%d %H:%M:%S")},
                                                ensure_ascii=False), encoding="utf-8")
                return data, history, False
        history += errors
        ask = prompt + FIX_PROMPT.format(errors="\n".join("- " + e for e in errors), previous=(raw or "")[:6000])
    return None, history, False


def _parse(raw: str) -> dict:
    raw = (raw or "").strip()
    m = re.search(r"```(?:json)?\s*(.*?)```", raw, re.S)
    if m:
        raw = m.group(1).strip()
    elif not raw.startswith("{"):
        start, end = raw.find("{"), raw.rfind("}")
        if start >= 0 and end > start:
            raw = raw[start:end + 1]
    data = json.loads(raw, strict=False)
    if isinstance(data, list):
        data = data[0] if data else {}
    if not isinstance(data, dict):
        raise ValueError("bukan objek JSON")
    return data


# --------------------------------------------------------------------------- 1. extract
def load_slides(pptx_path: Path, render_dir: Optional[Path], include_hidden: bool) -> tuple:
    prs = Presentation(str(pptx_path))
    W, H = prs.slide_width, prs.slide_height
    slides, skipped = [], []
    for n, slide in enumerate(prs.slides, 1):
        if le.is_hidden(slide) and not include_hidden:
            skipped.append(n)
            continue
        render = render_dir / f"slide{n}.png" if render_dir else None
        slides.append(Slide(n, slide.slide_layout.name, re_.extract(slide, W, H),
                            render if render and render.exists() else None))
    return slides, skipped, W / H


def _pct(v: float) -> str:
    return f"{v * 100:.0f}"


_ROMAN = [(10, "x"), (9, "ix"), (5, "v"), (4, "iv"), (1, "i")]


def _roman(n: int) -> str:
    out = ""
    for v, r in _ROMAN:
        while n >= v:
            out, n = out + r, n - v
    return out


def _num_label(n: int, fmt: str) -> str:
    if fmt == "lowerLetter":
        return chr(96 + (n - 1) % 26 + 1) + "."
    if fmt == "upperLetter":
        return chr(64 + (n - 1) % 26 + 1) + "."
    if fmt == "lowerRoman":
        return _roman(n) + "."
    if fmt == "upperRoman":
        return _roman(n).upper() + "."
    return f"{n}."


def para_labels(paras: list) -> list:
    """Awalan tiap paragraf seperti tampil di PowerPoint: "• " untuk bullet, nomor otomatis ("1. ", "a. ")
    untuk list bernomor, "" selain itu. Nomor otomatis tidak ada di teks PPTX, jadi dihitung di sini."""
    counters, out = {}, []
    for p in paras:
        lvl = p.level
        for k in [k for k in counters if k > lvl]:
            del counters[k]
        if p.bullet and p.numbered:
            counters[lvl] = counters.get(lvl, 0) + 1
            out.append(_num_label(counters[lvl], p.num_fmt) + " ")
        else:
            if re_.para_text(p) and not p.bullet:     # paragraf biasa memutus list di level ini
                counters.pop(lvl, None)
            out.append("• " if p.bullet else "")
    return out


def describe(slide: Slide, el_chars: int, table_rows: int) -> str:
    lines = []
    for k, b in slide.els.items():
        head = f"{k} {b.kind} x={_pct(b.x)} y={_pct(b.y)} w={_pct(b.w)} h={_pct(b.h)}"
        if b.kind == "text":
            paras = [lbl + re_.para_text(p) for p, lbl in zip(b.paras, para_labels(b.paras)) if re_.para_text(p)]
            if not paras:
                continue
            text = " / ".join(paras)
            if len(text) > el_chars:
                text = text[:el_chars] + "…"
            tags = (" TITLE" if b.is_title else "") + (" FILLED" if b.filled else "")
            lines.append(f"{head}{tags}: {text}")
        elif b.kind == "table":
            size = f"{len(b.rows)}x{max((len(r) for r in b.rows), default=0)}"
            rows = [[c.replace("\n", " ") for c in r] for r in b.rows[:table_rows]]
            lines.append(f"{head} {size} first rows: {json.dumps(rows, ensure_ascii=False)}")
        elif b.kind == "picture":
            lines.append(head + (" (small icon)" if b.w < le.ICON_MAX_W else ""))
        else:
            if b.w * b.h > 0.002:         # garis / bentuk kecil tidak perlu
                lines.append(head)
    return "\n".join(lines)


def outline_listing(slides: list) -> str:
    out = []
    for s in slides:
        n_pic = sum(1 for b in s.els.values() if b.kind == "picture")
        n_tab = sum(1 for b in s.els.values() if b.kind == "table")
        parts, total = [], 0
        for t in s.texts():
            t = t if len(t) <= OUTLINE_EL_CHARS else t[:OUTLINE_EL_CHARS] + "…"
            if total + len(t) > OUTLINE_SLIDE_CHARS:
                parts.append("…")
                break
            parts.append(t)
            total += len(t)
        out.append(f"### Slide {s.n} (layout {s.layout}; {n_pic} charts/pictures, {n_tab} tables)\n" +
                   ("\n".join("- " + p for p in parts) if parts else "(no text)"))
    return "\n\n".join(out)


# --------------------------------------------------------------------------- 2. outline
def validate_outline(data: dict, numbers: set) -> list:
    errors = []
    chapters = data.get("chapters")
    if not isinstance(chapters, list) or not chapters:
        return ["'chapters' must hold at least one chapter"]
    for ci, ch in enumerate(chapters, 1):
        if not isinstance(ch, dict) or not str(ch.get("title", "")).strip():
            errors.append(f"chapter {ci}: empty 'title'")
            continue
        sections = ch.get("sections")
        if not isinstance(sections, list) or not sections:
            errors.append(f"chapter {ci}: empty 'sections'")
            continue
        for si, sec in enumerate(sections, 1):
            items = sec.get("items") if isinstance(sec, dict) else None
            if not isinstance(items, list):
                errors.append(f"chapter {ci} section {si}: 'items' must be a list")
                continue
            for it in items:
                if not isinstance(it, dict):
                    errors.append(f"chapter {ci} section {si}: an item is not an object")
                    continue
                try:
                    n = int(it.get("slide"))
                except (TypeError, ValueError):
                    errors.append(f"chapter {ci} section {si}: invalid slide number: {it.get('slide')!r}")
                    continue
                if n not in numbers:
                    errors.append(f"chapter {ci} section {si}: slide {n} does not exist")
                if it.get("style") not in STYLES:
                    errors.append(f"slide {n}: style must be 'topic' or 'text'")
    return errors


def make_outline(slides: list, provider: str, model: str, cache_dir: Optional[Path]) -> tuple:
    numbers = {s.n for s in slides}
    prompt = OUTLINE_PROMPT.format(slides=outline_listing(slides))
    data, errors, cached = ask_json(prompt, None, provider, model, cache_dir,
                                    lambda d: validate_outline(d, numbers))
    if data is None:
        raise RuntimeError("AI gagal menyusun kerangka buku: " + "; ".join(errors[-3:]))
    return data, cached


def outline_items(outline: dict) -> list:
    items = []
    for ci, ch in enumerate(outline["chapters"]):
        for si, sec in enumerate(ch["sections"]):
            for it in sec.get("items") or []:
                items.append(Item(ci, si, int(it["slide"]), it.get("style", "topic"),
                                  str(it.get("focus") or "").strip()))
    return items


# --------------------------------------------------------------------------- 3. tulis per slide
def _check_figures(figs, els: dict, where: str) -> list:
    errors = []
    if not isinstance(figs, list):
        return [f"{where}: 'figures' must be a list"]
    for f in figs:
        ids = f.get("ids") if isinstance(f, dict) else None
        if not isinstance(ids, list) or not ids:
            errors.append(f"{where}: picture without 'ids'")
            continue
        bad = [k for k in ids if k not in els]
        if bad:
            errors.append(f"{where}: ids not on this slide: {', '.join(map(str, bad))}")
    return errors


def _check_blocks(blocks, where: str, types: set) -> list:
    if not isinstance(blocks, list):
        return [f"{where}: 'blocks' must be a list"]
    errors = []
    for i, b in enumerate(blocks, 1):
        if not isinstance(b, dict) or b.get("type") not in types:
            errors.append(f"{where} block {i}: type must be one of {', '.join(sorted(types))} "
                          f"({b.get('type') if isinstance(b, dict) else b!r})")
    return errors


def validate_item(data: dict, slide: Slide, style: str) -> list:
    errors = []
    blocks = data.get("blocks")
    if not isinstance(blocks, list):
        return ["'blocks' must be a list"]
    all_blocks = list(blocks)
    if style == "topic":
        if not str(data.get("title", "")).strip():
            errors.append("empty 'title'")
        figs = data.get("figures", [])
        errors += _check_figures(figs, slide.els, "figures")
        if isinstance(figs, list):
            if len(figs) > MAX_FIGURES:
                errors.append(f"at most {MAX_FIGURES} figures")
            for fi, f in enumerate(figs, 1):
                if isinstance(f, dict) and len(str(f.get("caption") or "").split()) > MAX_CAPTION_WORDS:
                    errors.append(f"figure {fi}: caption longer than {MAX_CAPTION_WORDS} words is a headline: "
                                  "write it as the figure's first bullet in sentence case and set caption \"\"")
                if isinstance(f, dict) and f.get("blocks"):
                    errs = _check_blocks(f["blocks"], f"figure {fi}", PANEL_BLOCK_TYPES)
                    errors += errs
                    if not errs:
                        all_blocks += f["blocks"]
        if isinstance(figs, list) and len(figs) >= 2 and blocks and \
                not any(isinstance(f, dict) and f.get("blocks") for f in figs):
            errors.append("no figure has its own 'blocks': give each point to the figure it explains (the "
                          "figure's 'blocks'); keep in the top-level 'blocks' only points about the whole slide")
    elif not blocks:
        errors.append("empty 'blocks'")
    for i, b in enumerate(all_blocks, 1):
        if not isinstance(b, dict) or b.get("type") not in BLOCK_TYPES:
            errors.append(f"block {i}: unknown type ({b.get('type') if isinstance(b, dict) else b!r})")
            continue
        t = b["type"]
        if t == "table":
            if slide.els.get(b.get("id")) is None or slide.els[b["id"]].kind != "table":
                errors.append(f"block {i}: 'id' must be a table element of this slide")
        elif t == "figure":
            errors += _check_figures([b], slide.els, f"blok {i}")
        elif not str(b.get("text", "")).strip():
            errors.append(f"block {i}: empty 'text'")
        if "level" in b and not isinstance(b["level"], int):
            try:
                b["level"] = int(b["level"])
            except (TypeError, ValueError):
                errors.append(f"block {i}: 'level' must be a number")
    return errors


def write_item(item: Item, slide: Slide, section_title: str, prev_tail: str, provider: str, model: str,
               cache_dir: Optional[Path]) -> None:
    import llm_planner

    focus = f'\nFocus: use only this part of the slide: {item.focus}.' if item.focus else ""
    elements = describe(slide, ITEM_EL_CHARS, ITEM_TABLE_ROWS)
    if item.style == "text":
        prev = (f"\nEnd of the previous slide's text in this section: «{prev_tail}»" if prev_tail else "")
        prompt = TEXT_PROMPT.format(section=section_title, focus=focus, prev=prev, elements=elements,
                                    rules=COMMON_RULES)
    else:
        prompt = TOPIC_PROMPT.format(section=section_title, focus=focus, elements=elements, max_fig=MAX_FIGURES,
                                     max_words=MAX_CAPTION_WORDS, rules=COMMON_RULES)
    image = llm_planner.slide_image(slide.render) if slide.render else None
    try:
        data, errors, cached = ask_json(prompt, image, provider, model, cache_dir,
                                        lambda d: validate_item(d, slide, item.style))
    except Exception as e:          # jaringan / kuota / SDK: slide memakai cadangan
        data, errors, cached = None, [f"{type(e).__name__}: {e}"], False
    if data is None:
        item.source = "fallback"
        item.result = {"title": slide.title, "figures": [{"ids": list(slide.els), "caption": ""}], "blocks": []}
        item.warnings.append("AI gagal menulis slide ini; judul slide dan gambar slide utuh dipakai. "
                             + "; ".join(errors[-2:]))
        return
    item.source = "cache" if cached else "llm"
    item.result = data


# --------------------------------------------------------------------------- 4. cek angka
_NUM_RE = re.compile(r"\d+(?:[.,]\d+)*")


def _num_variants(tok: str) -> set:
    t = tok.strip(".,")
    return {t, t.replace(".", "").replace(",", ""), t.replace(",", "."), t.replace(".", ",")}


def number_set(text: str) -> set:
    out = set()
    for tok in _NUM_RE.findall(text):
        out |= _num_variants(tok)
    return out


def unknown_numbers(text: str, source: set) -> list:
    """Angka (>= 2 digit) di teks LLM yang tidak ada di teks slide."""
    seen, out = set(), []
    for tok in _NUM_RE.findall(text):
        t = tok.strip(".,")
        if sum(c.isdigit() for c in t) < 2 or t in seen:
            continue
        seen.add(t)
        if not (_num_variants(t) & source):
            out.append(t)
    return out


def number_context(text: str, number: str, chars: int = NUMBER_CONTEXT_CHARS) -> str:
    """Potongan kalimat di sekitar angka, untuk komentar review ("...terdapat 97 dan 485 bank...")."""
    m = re.search(r"(?<![\d.,])" + re.escape(number) + r"(?![\d]|[.,]\d)", text)
    if not m:
        return number
    a, b = max(0, m.start() - chars), min(len(text), m.end() + chars)
    snippet = re.sub(r"\s+", " ", text[a:b]).strip()
    return ("…" if a else "") + snippet + ("…" if b < len(text) else "")


def item_text(result: dict) -> str:
    parts = [result.get("title", "")]
    for f in result.get("figures") or []:
        if isinstance(f, dict):
            parts.append(f.get("caption", ""))
            parts += [b.get("text", "") for b in f.get("blocks") or [] if isinstance(b, dict)]
    for b in result.get("blocks") or []:
        if b.get("type") in ("heading", "label", "para", "bullet", "item"):
            parts.append(b.get("text", ""))
        elif b.get("type") in ("table", "figure"):
            parts.append(b.get("caption", ""))
    return "\n".join(plain(p or "") for p in parts)


# --------------------------------------------------------------------------- 5. tulis DOCX
def crop_region(slide: Slide, ids: list) -> tuple:
    return re_.union([slide.els[k] for k in ids if k in slide.els])


def _overlaps(a: tuple, b: tuple, eps: float = 0.005) -> bool:
    return (min(a[0] + a[2], b[0] + b[2]) - max(a[0], b[0]) > eps and
            min(a[1] + a[3], b[1] + b[3]) - max(a[1], b[1]) > eps)


def panel_regions(slide: Slide, figs: list, aspect: float) -> list:
    """Area crop tiap panel. Area panel (gabungan elemennya) dipotong di tepi inti panel tetangga supaya grafik
    tetangga tidak ikut ter-crop; inti = gabungan gambar/tabel panel itu. Potongan tidak melewati tengah inti
    panel sendiri."""
    regs = [crop_region(slide, f["ids"]) for f in figs]
    cores = []
    for f, reg in zip(figs, regs):
        main = [slide.els[k] for k in f["ids"] if k in slide.els and slide.els[k].kind in ("picture", "table")]
        cores.append(re_.union(main) if main else reg)
    out = []
    for i, (x, y, w, h) in enumerate(regs):
        x0, y0, x1, y1 = x, y, x + w, y + h
        ci = cores[i]
        mid_x, mid_y = ci[0] + ci[2] / 2, ci[1] + ci[3] / 2
        for j, cj in enumerate(cores):
            if j == i or not _overlaps((x0, y0, x1 - x0, y1 - y0), cj) or _overlaps(ci, cj):
                continue
            dx = cj[0] + cj[2] / 2 - mid_x
            dy = cj[1] + cj[3] / 2 - mid_y
            if abs(dx) * aspect >= abs(dy):       # tetangga di kiri / kanan
                if dx > 0:
                    x1 = min(x1, max(cj[0], mid_x))
                else:
                    x0 = max(x0, min(cj[0] + cj[2], mid_x))
            else:                                 # tetangga di atas / bawah
                if dy > 0:
                    y1 = min(y1, max(cj[1], mid_y))
                else:
                    y0 = max(y0, min(cj[1] + cj[3], mid_y))
        out.append((x0, y0, max(x1 - x0, 0.0), max(y1 - y0, 0.0)))
    return out


def save_figure(slide: Slide, ids: list, path: Path, render, reg: Optional[tuple] = None) -> Optional[Path]:
    reg = reg or crop_region(slide, ids)
    if reg[2] <= 0 or reg[3] <= 0:
        return None
    box = le.Box("picture", *reg, images=[i for k in ids if k in slide.els for i in slide.els[k].images])
    return le.save_box_image(box, path, render)


def _norm(t: str) -> str:
    return re.sub(r"[^0-9a-z]+", "", plain(t).lower())


def caption_in_image(caption: str, slide: Slide, ids: list) -> bool:
    """Keterangan yang sudah tertulis di dalam area crop (judul panel ikut ter-crop) tidak ditulis lagi."""
    cap = _norm(caption)
    if not cap:
        return True
    reg = le.Box("picture", *crop_region(slide, ids))
    for b in slide.els.values():
        if b.kind == "text" and re_.inside(b, reg):
            t = _norm(re_.box_text(b))
            if t and (cap in t or t in cap and len(t) >= 0.6 * len(cap)):
                return True
    return False


def table_rows(el) -> list:
    return [[re.sub(r"[ \t]+", " ", c).strip() for c in r] for r in el.rows]


def topic_panels(slide: Slide, res: dict, blocks: list, aspect: float, fig: Callable) -> tuple:
    """(butir sebelum panel, panel, butir setelah panel) untuk BookWriter.topic.
    Panel = (gambar, keterangan, butir panel, lebar?). Panel "full" (infografis) selalu selebar kotak dengan
    butirnya di bawah. Satu gambar tanpa butir sendiri memakai butir slide (sempit: di samping butir; lebar: di
    atasnya). Beberapa gambar tanpa butir sendiri: tiap gambar satu baris, butir slide setelahnya; begitu juga
    kalau panel pertama selebar kotak (infografis). Selain itu butir slide di bawah judul, sebelum panel."""
    box_title = _norm(res.get("title", ""))

    def chrome(k):
        """Tidak menentukan batas crop: judul slide (sudah jadi judul kotak), nomor halaman, dan garis tipis
        (garis pemisah bisa melintang sampai tepi slide; tetap terlihat di render)."""
        b = slide.els.get(k)
        if b is None:
            return False
        if b.kind == "shape":
            return min(b.w * aspect, b.h) < 0.03
        if b.kind != "text":
            return False
        t = _norm(re_.box_text(b))
        return b.is_title or t.isdigit() or (len(t) >= 12 and t in box_title)

    figs = []
    for f in res.get("figures") or []:
        ids = [k for k in f.get("ids") or [] if not chrome(k)]
        if ids:
            figs.append({**f, "ids": ids})
    if not figs:
        return blocks, [], []

    slide_texts = [_norm(re_.box_text(b)) for b in slide.els.values() if b.kind == "text"]

    def caption(f, ids):
        cap = (f.get("caption") or "").strip()
        if not cap or caption_in_image(cap, slide, ids):
            return ""
        # judul yang tidak ada di teks slide dibaca dari dalam gambar grafik: sudah terlihat di gambar
        return cap if any(_norm(cap) in t for t in slide_texts) else ""

    if len(figs) == 1 and not figs[0].get("blocks") and not figs[0].get("full"):
        f = figs[0]                       # satu gambar + butir slide: sempit di samping butir, lebar di atasnya
        img = fig(f["ids"])
        if not img:
            return blocks, [], []
        x, y, fw, fh = crop_region(slide, f["ids"])
        return [], [(img, caption(f, f["ids"]), blocks, fw * aspect / max(fh, 1e-6) >= SIDE_ASPECT)], []
    panels = []
    for f, reg in zip(figs, panel_regions(slide, figs, aspect)):
        img = fig(f["ids"], reg)
        if img:
            wide = bool(f.get("full")) or reg[2] * aspect / max(reg[3], 1e-6) > PANEL_WIDE_ASPECT
            panels.append((img, caption(f, f["ids"]), f.get("blocks") or [], wide))
    if not any(pb for _, _, pb, _ in panels) or (panels and panels[0][3]):
        return [], panels, blocks         # butir slide setelah gambar: tidak dibagi per panel / infografis di atas
    return blocks, panels, []


def write_book(outline: dict, items: list, slides: dict, docx_path: Path, media_dir: Path, aspect: float,
               template: Path = DEFAULT_TEMPLATE, title: str = "", comments: bool = True,
               page: Optional[BookHtmlWriter] = None) -> int:
    """Menulis DOCX (dan HTML CKEditor lewat `page` kalau diisi); mengembalikan jumlah komentar review."""
    docx = BookWriter(template)
    w = Tee(docx, page)
    w.title(title or outline.get("title") or "Buku Ringkasan")
    renders, n_comments, counter = {}, 0, {}
    by_section = {}
    for it in items:
        by_section.setdefault((it.chapter, it.section), []).append(it)
    for ci, ch in enumerate(outline["chapters"]):
        w.chapter(str(ci + 1), ch["title"].strip())
        numbered = [s for s in ch["sections"] if str(s.get("title", "")).strip()]
        for si, sec in enumerate(ch["sections"]):
            sec_title = str(sec.get("title", "")).strip()
            if sec_title:
                w.section(f"{ci + 1}.{numbered.index(sec) + 1}", sec_title)
            for it in by_section.get((ci, si), []):
                slide = slides[it.slide]
                if slide.n not in renders:
                    renders[slide.n] = le.load_render(slide.render)
                render = renders[slide.n]

                def fig(ids, reg=None, _s=slide, _r=render):
                    counter[_s.n] = counter.get(_s.n, 0) + 1
                    return save_figure(_s, ids, media_dir / f"s{_s.n:03d}_{counter[_s.n]}.png", _r, reg)

                start = docx.mark()
                res = it.result
                blocks = []
                for b in res.get("blocks") or []:
                    if b["type"] == "table":
                        blocks.append({"type": "table", "rows": table_rows(slide.els[b["id"]]),
                                       "caption": b.get("caption", "")})
                    elif b["type"] == "figure":
                        img = fig(b["ids"])
                        if img:
                            cap = (b.get("caption") or "").strip()
                            if cap and caption_in_image(cap, slide, b["ids"]):
                                cap = ""
                            blocks.append({"type": "figure", "img": img, "caption": cap})
                    else:
                        blocks.append(b)
                if it.style == "topic":
                    w.topic(res.get("title", "").strip(), *topic_panels(slide, res, blocks, aspect, fig))
                else:
                    w.blocks(blocks)
                if comments and it.warnings:
                    docx.comment(start, [f"Slide {slide.n}: perlu dicek."] + ["- " + x for x in it.warnings])
                    n_comments += 1
    docx.save(docx_path)
    return n_comments


# --------------------------------------------------------------------------- orkestrasi
def convert_book(
    pptx_path,
    docx_path,
    provider: str = "bedrock",
    model: str = DEFAULT_MODEL,
    render: bool = True,
    work_dir=None,
    template=DEFAULT_TEMPLATE,
    include_hidden: bool = False,
    cache_dir=DEFAULT_CACHE,
    workers: int = 4,
    progress: ProgressFn = _noop,
    title: str = "",
    comments: bool = True,
    slides_dir=None,
    html_path=None,
    img_src: Optional[Callable[[Path], str]] = None,
) -> dict:
    """title: judul buku (kosong = usulan AI). comments: komentar Word pada isi yang perlu dicek.
    slides_dir: folder render slide yang sudah ada (slideN.png dari deck yang sama), dipakai tanpa render ulang.
    html_path: juga tulis HTML untuk CKEditor; img_src: path gambar -> src (default data URI, HTML mandiri)."""
    pptx_path, docx_path = Path(pptx_path), Path(docx_path)
    work = Path(work_dir) if work_dir else docx_path.parent / (docx_path.stem + "_build")
    render_dir, media_dir = work / "slides", work / "media"
    work.mkdir(parents=True, exist_ok=True)
    cache = Path(cache_dir) if cache_dir else None
    t0 = time.time()

    progress(0.02, "Merender slide")
    if slides_dir and (Path(slides_dir) / "slide1.png").exists():
        render_dir, rendered = Path(slides_dir), True
    else:
        rendered = le.render_slides(pptx_path, render_dir) if render else False
    slides, hidden, aspect = load_slides(pptx_path, render_dir if rendered else None, include_hidden)
    by_n = {s.n: s for s in slides}
    t_render = time.time()

    progress(0.15, "AI menyusun kerangka buku")
    outline, outline_cached = make_outline(slides, provider, model, cache)
    items = outline_items(outline)
    t_outline = time.time()

    progress(0.25, f"AI menulis isi {len(items)} slide")
    titles = {}
    for ci, ch in enumerate(outline["chapters"]):
        for si, sec in enumerate(ch["sections"]):
            titles[(ci, si)] = " - ".join(t for t in (ch["title"], str(sec.get("title", ""))) if str(t).strip())
    prev_tail, last = {}, {}
    for it in items:              # akhir teks slide sebelumnya di bagian yang sama (untuk slide lanjutan)
        key = (it.chapter, it.section)
        if key in last and last[key] != it.slide:
            prev_tail[id(it)] = by_n[last[key]].source_text()[-PREV_TAIL_CHARS:]
        last[key] = it.slide
    with ThreadPoolExecutor(max(1, workers)) as ex:
        futures = {ex.submit(write_item, it, by_n[it.slide], titles[(it.chapter, it.section)],
                             prev_tail.get(id(it), ""), provider, model, cache): it for it in items}
        for done, f in enumerate(as_completed(futures), 1):
            f.result()
            progress(0.25 + 0.65 * done / max(len(items), 1),
                     f"AI: slide {futures[f].slide} selesai ({done}/{len(items)})")
    t_items = time.time()

    for it in items:              # angka yang tidak ada di teks slide
        if it.source == "fallback":
            continue
        text = item_text(it.result)
        missing = unknown_numbers(text, number_set(by_n[it.slide].source_text()))
        if missing:
            it.warnings.append(f"Angka di teks buku yang tidak ada di teks slide {it.slide} (mungkin dibaca dari "
                               "grafik, atau salah tafsir); cocokkan dengan slide:")
            it.warnings += [f'angka "{n}": «{number_context(text, n)}»' for n in missing[:MAX_NUMBER_NOTES]]
            if len(missing) > MAX_NUMBER_NOTES:
                it.warnings.append("angka lain: " + ", ".join(missing[MAX_NUMBER_NOTES:]))

    progress(0.92, "Menulis dokumen Word")
    page = BookHtmlWriter(img_src) if img_src else BookHtmlWriter()
    n_comments = write_book(outline, items, by_n, docx_path, media_dir, aspect, Path(template), title, comments,
                            page if html_path else None)
    if html_path:
        page.save(Path(html_path), title or outline.get("title", ""))
    used = {it.slide for it in items}
    report = {"outline": outline, "items": [
        {"slide": it.slide, "chapter": it.chapter + 1, "section": it.section + 1, "style": it.style,
         "focus": it.focus, "source": it.source, "warnings": it.warnings, "result": it.result} for it in items]}
    (work / "book.json").write_text(json.dumps(report, ensure_ascii=False, indent=1), encoding="utf-8")
    progress(1.0, "Selesai")
    return {
        "title": title or outline.get("title"), "slides": len(slides), "hidden_skipped": hidden,
        "rendered": rendered, "chapters": len(outline["chapters"]), "items": len(items),
        "slides_used": len(used), "slides_skipped": sorted(s.n for s in slides if s.n not in used),
        "llm_calls": sum(1 for it in items if it.source == "llm") + (0 if outline_cached else 1),
        "cache_hits": sum(1 for it in items if it.source == "cache") + (1 if outline_cached else 0),
        "fallback": [it.slide for it in items if it.source == "fallback"],
        "comments": n_comments,
        "seconds": {"render": round(t_render - t0, 1), "outline": round(t_outline - t_render, 1),
                    "write": round(t_items - t_outline, 1), "docx": round(time.time() - t_items, 1)},
        "docx": str(docx_path), "html": str(html_path) if html_path else None, "book": str(work / "book.json"),
        "check": sorted({it.slide for it in items if it.warnings}),
    }


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="PPTX -> DOCX buku ringkasan (Full AI)")
    ap.add_argument("pptx")
    ap.add_argument("-o", "--output", default="Buku_Output.docx")
    ap.add_argument("--title", default="", help="judul buku (default: usulan AI)")
    ap.add_argument("--html", default=None, help="juga tulis HTML mandiri untuk CKEditor ke path ini")
    ap.add_argument("--provider", choices=["bedrock", "ollama"], default="bedrock")
    ap.add_argument("--model", default=DEFAULT_MODEL)
    ap.add_argument("--template", default=str(DEFAULT_TEMPLATE))
    ap.add_argument("--work-dir", default=None)
    ap.add_argument("--slides-dir", default=None, help="folder render slide yang sudah ada (slideN.png)")
    ap.add_argument("--workers", type=int, default=4, help="jumlah panggilan LLM paralel")
    ap.add_argument("--no-cache", action="store_true", help="jangan pakai/simpan cache jawaban LLM")
    ap.add_argument("--no-render", action="store_true", help="tanpa render: gambar asli dari PPTX")
    ap.add_argument("--include-hidden", action="store_true", help="ikut slide yang di-hide")
    ap.add_argument("--no-comments", action="store_true", help="tanpa komentar Word untuk hal yang perlu dicek")
    a = ap.parse_args()
    stats = convert_book(a.pptx, a.output, provider=a.provider, model=a.model, render=not a.no_render,
                         work_dir=a.work_dir, template=a.template, include_hidden=a.include_hidden,
                         cache_dir=None if a.no_cache else DEFAULT_CACHE, workers=a.workers,
                         progress=lambda f, m: print(f"[{f:4.0%}] {m}", flush=True), title=a.title,
                         comments=not a.no_comments, slides_dir=a.slides_dir, html_path=a.html)
    print(json.dumps(stats, ensure_ascii=False, indent=1))
