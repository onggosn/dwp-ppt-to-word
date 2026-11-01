"""book_engine tanpa LLM sungguhan:  python -m unittest discover tests

- cek angka: angka buatan LLM yang tidak ada di teks slide ditandai; format 4,75 / 4.75 / 1.234 dianggap sama
- nomor otomatis PowerPoint (1. a. i.) ikut ke deskripsi slide untuk LLM
- validasi kerangka dan jawaban per slide
- crop panel tidak ikut memotong grafik panel tetangga
- alur lengkap dengan LLM palsu (jawaban JSON tetap) menghasilkan DOCX dengan bab, bagian, kotak berpanel
  (gambar | butir panel), indentasi badan teks seperti contoh, dan komentar
"""
import json
import re
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

import book_engine as be  # noqa: E402
import llm_planner  # noqa: E402
from book_writer import md_runs  # noqa: E402
from docx import Document  # noqa: E402
from docx.oxml.ns import qn  # noqa: E402
import book_writer as bw  # noqa: E402
from layout_engine import Box, Para  # noqa: E402

DECK = ROOT / "docs" / "test.pptx"


class NumbersTest(unittest.TestCase):
    def test_unknown_numbers(self):
        source = be.number_set("BI Rate tetap 4,75%; cadev USD151,9 miliar; 1.234 bank pada 2026")
        self.assertEqual(be.unknown_numbers("BI Rate 4.75% dan 151,9 miliar, 1234 bank 2026", source), [])
        self.assertEqual(be.unknown_numbers("inflasi 3,3% dan 5 bank", source), ["3,3"])   # 1 digit diabaikan


class LabelsTest(unittest.TestCase):
    def test_auto_numbers(self):
        def p(text, level=0, numbered=False, fmt="decimal", bullet=None):
            return Para([(text, False, False)], level, numbered if bullet is None else bullet, numbered, fmt)
        paras = [p("Kebijakan Suku Bunga", 0, True), p("tetap", 1, True, "lowerLetter"),
                 p("naik", 1, True, "lowerLetter"), p("Operasi Moneter", 0, True),
                 p("SBO", 1, True, "lowerLetter"), p("catatan", 0, bullet=True)]
        self.assertEqual(be.para_labels(paras), ["1. ", "a. ", "b. ", "2. ", "a. ", "• "])

    def test_markdown_runs(self):
        self.assertEqual(md_runs("ke *safe haven* dan **bold**"),
                         [("ke ", False, False), ("safe haven", False, True), (" dan ", False, False),
                          ("bold", True, False)])
        self.assertEqual(md_runs("**K2: *funding*** bank *) catatan"),
                         [("K2: ", True, False), ("funding", True, True), (" bank *) catatan", False, False)])


class ValidateTest(unittest.TestCase):
    def test_outline(self):
        good = {"chapters": [{"title": "A", "sections": [{"title": "", "items": [{"slide": 2, "style": "text"}]}]}]}
        self.assertEqual(be.validate_outline(good, {1, 2}), [])
        bad = {"chapters": [{"title": "A", "sections": [{"title": "", "items": [{"slide": 9, "style": "x"}]}]}]}
        self.assertEqual(len(be.validate_outline(bad, {1, 2})), 2)


class PanelTest(unittest.TestCase):
    def test_regions_clip_neighbours(self):
        # dua grafik berdampingan; teks judul panel kiri melebar sampai ke atas grafik kanan
        els = {"e1": Box("picture", 0.05, 0.3, 0.4, 0.5), "e2": Box("text", 0.05, 0.2, 0.9, 0.08),
               "e3": Box("picture", 0.55, 0.3, 0.4, 0.5)}
        slide = be.Slide(1, "x", els)
        left, right = be.panel_regions(slide, [{"ids": ["e1", "e2"]}, {"ids": ["e3"]}], 16 / 9)
        self.assertAlmostEqual(left[0] + left[2], 0.55)      # berhenti di tepi kiri grafik kanan
        self.assertAlmostEqual(right[0], 0.55)


def fake_llm(prompt, image, provider, model):
    """Jawaban tetap: kerangka dengan dua slide pertama yang berteks; kotak / teks memakai elemen yang ada."""
    if "SUMMARY BOOK (a formal" in prompt:
        slides = [int(n) for n in re.findall(r"### Slide (\d+) \(", prompt)]
        with_pics = [int(n) for n, k in re.findall(r"### Slide (\d+) \([^;]*; (\d+) charts", prompt) if int(k)]
        return json.dumps({"title": "Buku Uji", "chapters": [
            {"title": "Bab Satu", "sections": [
                {"title": "Bagian Topik", "items": [{"slide": (with_pics or slides)[0], "style": "topic", "focus": ""}]},
                {"title": "Bagian Teks", "items": [{"slide": slides[-1], "style": "text", "focus": ""}]}]}],
            "skipped": []})
    ids = re.findall(r"^(e\d+) (\w+)", prompt, re.M)
    pics = [k for k, kind in ids if kind == "picture"]
    if "one box" in prompt:
        return json.dumps({"title": "Pesan kunci", "figures": [
            {"ids": pics[:1], "caption": "", "blocks": [{"type": "bullet", "text": "Penjelasan panel"}]}]
            if pics else [], "blocks": [{"type": "bullet", "text": "Pertumbuhan 98,76% di luar slide"}]})
    return json.dumps({"blocks": [{"type": "label", "text": "KESIMPULAN"},
                                  {"type": "item", "label": "a.", "text": "Teks *miring*", "level": 0}]})


@unittest.skipUnless(DECK.exists(), "deck contoh tidak ada")
class PipelineTest(unittest.TestCase):
    def setUp(self):
        self._orig = llm_planner.call_llm
        llm_planner.call_llm = fake_llm

    def tearDown(self):
        llm_planner.call_llm = self._orig

    def test_convert(self):
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "buku.docx"
            stats = be.convert_book(DECK, out, render=False, work_dir=Path(tmp) / "build", cache_dir=None,
                                    workers=2)
            self.assertEqual(stats["fallback"], [])
            doc = Document(str(out))
            texts = [p.text for p in doc.paragraphs]
            self.assertEqual(texts[0], "Buku Uji")
            self.assertIn("1. Bab Satu", texts)
            self.assertIn("1.1 Bagian Topik", texts)
            self.assertIn("1.2 Bagian Teks", texts)
            self.assertIn("a.\tTeks miring", texts)
            box = doc.tables[0]
            self.assertEqual(box.rows[0].cells[0].text, "Pesan kunci")
            # panel: gambar kiri | butir kanan (dua sel berbeda)
            self.assertTrue(any(r.cells[0]._tc is not r.cells[1]._tc and "Penjelasan panel" in r.cells[1].text
                                for r in box.rows), "baris panel (gambar | butir) tidak ada")
            # indentasi seperti contoh: label < butir
            label = next(p for p in doc.paragraphs if p.text == "KESIMPULAN")
            item = next(p for p in doc.paragraphs if p.text == "a.\tTeks miring")
            self.assertEqual(label.paragraph_format.left_indent.twips, bw.BODY_INDENT)
            self.assertEqual(item.paragraph_format.left_indent.twips, bw.ITEM_TEXT)   # list masuk ke dalam
            # angka 98,76 tidak ada di slide -> komentar Word
            self.assertEqual(stats["comments"], 1)
            self.assertTrue(any(el.tag == qn("w:commentRangeStart") for el in doc.element.body.iter()))


if __name__ == "__main__":
    unittest.main()
