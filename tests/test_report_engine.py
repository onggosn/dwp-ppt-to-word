"""Regresi report_engine tanpa LLM:  python -m unittest discover tests

- test3 (aturan saja, tanpa render PowerPoint) = 100% terhadap docs/test3.docx
- HTML CKEditor berisi teks, gambar, tabel, heading dan item list yang sama dengan DOCX
- list HTML bersarang dengan benar; parse jawaban LLM menerima karakter kontrol mentah

Setiap panggilan LLM membuat test gagal (llm_planner.call_llm diganti dengan exception yang tidak ditangkap
fallback engine). Deck contoh tidak ada di git, jadi test yang membutuhkannya dilewati kalau filenya tidak ada.
"""
import html.parser
import re
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

import evaluate  # noqa: E402
import llm_planner  # noqa: E402
import report_engine  # noqa: E402
from docx import Document  # noqa: E402
from docx.oxml.ns import qn  # noqa: E402
from report_writer import HtmlReportWriter  # noqa: E402

DECK, GOLD = ROOT / "docs" / "test3.pptx", ROOT / "docs" / "test3.docx"


class LLMCalled(BaseException):
    """BaseException: tidak tertangkap `except Exception` di report_engine.plan_with_llm."""


def _no_llm(*_args, **_kwargs):
    raise LLMCalled("test memanggil LLM")


def setUpModule():
    llm_planner.call_llm = _no_llm


def _norm(s: str) -> str:
    return re.sub(r"\s+", " ", s).strip()


def docx_view(path: Path) -> tuple:
    body = Document(str(path)).element.body
    texts, counts = [], {"img": 0, "table": 0, "h1": 0, "h2": 0, "list": 0}
    for p in body.iter(qn("w:p")):
        texts.append("".join(t.text or "" for t in p.iter(qn("w:t"))))
        style = p.find(qn("w:pPr") + "/" + qn("w:pStyle"))
        if style is not None and style.get(qn("w:val")) in ("Heading1", "Heading2"):
            counts["h" + style.get(qn("w:val"))[-1]] += 1
        if p.find(qn("w:pPr") + "/" + qn("w:numPr")) is not None:
            counts["list"] += 1
    counts["img"] = sum(1 for _ in body.iter("{http://schemas.openxmlformats.org/drawingml/2006/main}blip"))
    counts["table"] = sum(1 for _ in body.iter(qn("w:tbl")))
    return _norm(" ".join(texts)), counts


class HtmlView(html.parser.HTMLParser):
    BLOCKS = {"p", "h1", "h2", "li", "td", "tr", "table", "ul", "ol"}

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.parts, self.stack, self.errors, self.body = [], [], [], False
        self.counts = {"img": 0, "table": 0, "h1": 0, "h2": 0, "list": 0}

    def handle_starttag(self, tag, attrs):
        self.body |= tag == "body"
        if tag in ("img", "br", "meta"):
            self.counts["img"] += tag == "img"
            return
        self.stack.append(tag)
        if tag in ("table", "h1", "h2"):
            self.counts[tag] += 1
        self.counts["list"] += tag == "li"
        if tag in self.BLOCKS:
            self.parts.append(" ")

    def handle_endtag(self, tag):
        if self.stack and self.stack[-1] == tag:
            self.stack.pop()
        else:
            self.errors.append(tag)
        if tag in self.BLOCKS:
            self.parts.append(" ")

    def handle_data(self, data):
        if self.body:
            self.parts.append(data)


@unittest.skipUnless(DECK.exists() and GOLD.exists(), "docs/test3.pptx / docs/test3.docx tidak ada")
class Test3Rules(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.TemporaryDirectory()
        out = Path(cls.tmp.name)
        cls.docx, cls.html = out / "test3.docx", out / "test3.html"
        cls.stats = report_engine.convert_report(DECK, cls.docx, cls.html, planner="rules", render=False,
                                                 work_dir=out / "build")

    @classmethod
    def tearDownClass(cls):
        cls.tmp.cleanup()

    def test_no_llm(self):
        self.assertEqual(self.stats["llm_slides"], 0)

    def test_matches_gold(self):
        res = evaluate.evaluate(GOLD, self.docx, Path(self.stats["plans"]))
        low = {r["title"][:60]: round(r["score"], 3) for r in res["slides"] if r["score"] < 1}
        self.assertEqual(low, {})
        self.assertEqual(res["overall"], 1.0)

    def test_html_matches_docx(self):
        text, counts = docx_view(self.docx)
        view = HtmlView()
        view.feed(self.html.read_text(encoding="utf-8"))
        self.assertEqual(view.errors, [])
        self.assertEqual([t for t in view.stack if t not in ("html", "body")], [])
        self.assertEqual(view.counts, counts)
        self.assertEqual(_norm("".join(view.parts)), text)


class HtmlLists(unittest.TestCase):
    @staticmethod
    def frag(items) -> str:
        w = HtmlReportWriter(img_src=str)
        for level, numbered, fmt in items:
            w.rich([(f"L{level}", False, False)], bullet=True, numbered=numbered, level=level, num_fmt=fmt)
        return w.fragment().replace("\n", "")

    def test_nesting(self):
        cases = [
            ([(0, False, "decimal"), (1, False, "decimal"), (1, False, "decimal"), (0, False, "decimal")],
             "<ul><li>L0<ul><li>L1</li><li>L1</li></ul></li><li>L0</li></ul>"),
            ([(1, False, "decimal"), (1, False, "decimal"), (2, False, "decimal")],      # list mulai di level 1
             "<ul><li>L1</li><li>L1<ul><li>L2</li></ul></li></ul>"),
            ([(0, False, "decimal"), (2, False, "decimal")],                            # loncat 0 -> 2
             "<ul><li>L0<ul><li>L2</li></ul></li></ul>"),
            ([(0, False, "decimal"), (0, True, "decimal")],                             # bullet -> nomor
             "<ul><li>L0</li></ul><ol><li>L0</li></ol>"),
            ([(0, True, "decimal"), (1, True, "lowerLetter")],
             '<ol><li>L0<ol type="a"><li>L1</li></ol></li></ol>'),
        ]
        for items, expected in cases:
            self.assertEqual(self.frag(items), expected)


class LlmAnswerParsing(unittest.TestCase):
    def test_raw_control_characters(self):
        raw = '```json\n{"blocks": [{"type": "heading", "level": 1, "id": "e1"}], "drop": ["e2"], "x": "a\tb\nc"}\n```'
        self.assertEqual(llm_planner.parse(raw)["blocks"], [{"type": "heading", "level": 1, "id": "e1"}])


if __name__ == "__main__":
    unittest.main()
