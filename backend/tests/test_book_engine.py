"""book_engine tanpa LLM sungguhan:  python -m unittest discover backend/tests

- cek angka: angka buatan LLM yang tidak ada di teks slide ditandai; format 4,75 / 4.75 / 1.234 dianggap sama
- nomor otomatis PowerPoint (1. a. i.) ikut ke deskripsi slide untuk LLM
- validasi kerangka dan jawaban per slide
- cek angka ke gambar slide: hanya angka yang AI tidak yakin diberi komentar
- gambar/grafik besar dikirim ke AI juga sebagai crop resolusi penuh
- crop panel tidak ikut memotong grafik panel tetangga
- alur lengkap dengan LLM palsu (jawaban JSON tetap) menghasilkan DOCX dengan bab, bagian, kotak berpanel
  (gambar | butir panel), indentasi badan teks seperti contoh, dan komentar
"""
import io
import json
import re
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

BACKEND = Path(__file__).resolve().parent.parent
ROOT = BACKEND.parent
sys.path.insert(0, str(BACKEND))

import book_engine as be  # noqa: E402
import llm  # noqa: E402
from book_writer import md_runs  # noqa: E402
from docx import Document  # noqa: E402
from docx.oxml.ns import qn  # noqa: E402
import book_writer as bw  # noqa: E402
from slide_reader import Box, Para  # noqa: E402
from token_usage import record_usage  # noqa: E402

DECK = ROOT / "samples" / "test.pptx"


class NumbersTest(unittest.TestCase):
    def test_unknown_numbers(self):
        source = be.number_set("BI Rate tetap 4,75%; cadev USD151,9 miliar; 1.234 bank pada 2026")
        self.assertEqual(be.unknown_numbers("BI Rate 4.75% dan 151,9 miliar, 1234 bank 2026", source), [])
        self.assertEqual(be.unknown_numbers("inflasi 3,3% dan 5 bank", source), ["3,3"])   # 1 digit diabaikan
        self.assertEqual(be.unknown_numbers("pada 2025 dan Mar'26 naik 12,5", set()), ["12,5"])   # tahun diabaikan


class NumberPlacesTest(unittest.TestCase):
    def test_each_use_hidden(self):
        text = "PDB Dunia 2,9% (2026) dan 2,9% (2027), inflasi 4,5%"
        places = be.number_places(text, "2,9", 20)
        self.assertEqual(len(places), 2)
        self.assertIn("[[?]]% (2026) dan [[#]]", places[0])
        self.assertIn("[[#]]% (2026) dan [[?]]", places[1])
        self.assertNotIn("2,9", "".join(places))

    def test_same_number(self):
        self.assertTrue(be.same_number("2,8", "2.8"))
        self.assertTrue(be.same_number("0,8", "-0.8"))
        self.assertTrue(be.same_number("4.831", "4,831"))
        self.assertTrue(be.same_number("86", "USD86/bl"))
        self.assertFalse(be.same_number("2,9", "2.8"))


class VerifyTest(unittest.TestCase):
    """AI membaca nilai di tempat yang dimaksud tanpa melihat angkanya; program yang membandingkan"""
    def setUp(self):
        self._orig = llm.call_llm

    def tearDown(self):
        llm.call_llm = self._orig

    def item(self):
        it = be.Item(slide=1, chapter=0, section=0, style="topic")
        it.result = {"title": "Brent 84,0 dan PDB 2,9% (2026) dan 2,9% (2027)", "figures": [], "blocks": []}
        it.numbers = ["84,0", "2,9"]
        return it

    def test_wrong_use_flagged(self):
        def fake(prompt, image, provider, model):
            self.assertIn("p1 | Brent [[?]]", prompt)
            lines = [ln for ln in prompt.splitlines() if ln.startswith(("p2 |", "p3 |"))]
            self.assertEqual(len(lines), 2)
            self.assertNotIn("2,9", "".join(lines))                 # angka yang dicek tidak terlihat oleh AI
            return json.dumps({"places": [
                {"id": "p1", "at": "Brent Tw.I", "kind": "printed", "value": "84.0", "certain": True},
                {"id": "p2", "at": "PDB kolom 2026", "kind": "printed", "value": "2.8", "certain": True},
                {"id": "p3", "at": "PDB kolom 2027", "kind": "printed", "value": "2.9", "certain": True}]})
        llm.call_llm = fake
        it = self.item()
        be.verify_numbers(it, be.Slide(1, "", {}), "bedrock", "m", None)
        self.assertEqual(be.flagged_numbers(it), ["2,9"])
        self.assertEqual(it.verdicts["2,9"], ("mismatch", "PDB kolom 2026 tertulis 2.8"))

    def test_unclear_and_missing(self):
        llm.call_llm = lambda *a: json.dumps({"places": [
            {"id": "p1", "at": "Brent Tw.I", "kind": "printed", "value": "84.0", "certain": False},
            {"id": "p2", "at": "", "kind": "no_spot", "value": "", "certain": False},
            {"id": "p3", "at": "", "kind": "no_spot", "value": "", "certain": False}]})
        it = self.item()
        be.verify_numbers(it, be.Slide(1, "", {}), "bedrock", "m", None)
        self.assertEqual(it.verdicts["84,0"][0], "unsure")
        self.assertEqual(it.verdicts["2,9"][0], "absent")

    def test_failure_keeps_all(self):
        llm.call_llm = lambda *a: '{"places": []}'
        it = self.item()
        be.verify_numbers(it, be.Slide(1, "", {}), "bedrock", "m", None)
        self.assertEqual(be.flagged_numbers(it), ["84,0", "2,9"])


class CropsTest(unittest.TestCase):
    """grafik/tabel bergambar dikirim juga sebagai crop resolusi penuh, urutannya dijelaskan di prompt"""
    @staticmethod
    def png(w, h, mode="RGB"):
        import io
        from PIL import Image
        buf = io.BytesIO()
        Image.new(mode, (w, h)).save(buf, "PNG")
        return buf.getvalue()

    def test_big_pictures_only(self):
        big = Box("picture", 0.6, 0.3, 0.35, 0.3, images=[(self.png(1000, 600, "RGBA"), "png", 0.1)])
        icon = Box("picture", 0.0, 0.0, 0.05, 0.05, images=[(self.png(200, 200), "png", 0.0025)])
        cut = Box("picture", 0.0, 0.3, 0.4, 0.4, images=[(self.png(900, 900), "png", 0.16)], cropped=True)
        slide = be.Slide(1, "", {"e1": big, "e2": icon, "e3": cut})
        images, note = be.slide_images(slide)
        self.assertEqual([k for k, _, _ in slide.crops], ["e1"])   # tanpa render: gambar terpotong dilewati
        self.assertEqual(len(images), 1)
        self.assertIn("e1", note)
        self.assertEqual(images[0][:2], b"\xff\xd8")             # JPEG

    def test_wide_table_split(self):
        wide = Box("picture", 0.3, 0.7, 0.66, 0.29, images=[(self.png(1958, 408), "png", 0.19)])
        slide = be.Slide(1, "", {"e1": wide})
        images, note = be.slide_images(slide)
        self.assertEqual([p for _, p, _ in slide.crops], ["1/3", "2/3", "3/3"])
        self.assertIn("e1 part 2/3", note)
        from PIL import Image
        import io
        w, h = Image.open(io.BytesIO(images[0])).size                  # diperbesar sampai batas ukuran Claude
        self.assertGreater(w, 1300)
        self.assertLessEqual(w * h, llm.CROP_MAX_PIXELS * 1.01)

    def test_no_pictures(self):
        images, note = be.slide_images(be.Slide(1, "", {}))
        self.assertEqual(images, [])
        self.assertIn("No slide render", note)


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
        self._orig = llm.call_llm
        llm.call_llm = fake_llm

    def tearDown(self):
        llm.call_llm = self._orig

    def test_usage_includes_parallel_slide_calls(self):
        def fake_with_usage(prompt, image, provider, model):
            record_usage(model, input_tokens=100, output_tokens=20, total_tokens=120)
            return fake_llm(prompt, image, provider, model)

        with tempfile.TemporaryDirectory() as tmp, patch("sys.stdout", new_callable=io.StringIO), \
                patch.object(llm, "call_llm", side_effect=fake_with_usage):
            stats = be.convert_book(
                DECK, Path(tmp) / "book.docx", render=False,
                work_dir=Path(tmp) / "build", cache_dir=None, workers=2,
            )
        self.assertEqual(stats["token_usage"]["responses"], 3)
        self.assertEqual(stats["token_usage"]["input_tokens"], 300)
        self.assertEqual(stats["token_usage"]["output_tokens"], 60)
        self.assertEqual(stats["token_usage"]["total_tokens"], 360)

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
            # angka 98,76 tidak ada di slide -> komentar Word di angka itu
            self.assertEqual(stats["comments"], 1)
            # komentar menempel tepat pada angkanya, bukan pada judul kotak
            inside, covered = False, ""
            for el in doc.element.body.iter():
                if el.tag == qn("w:commentRangeStart"):
                    inside = True
                elif el.tag == qn("w:commentRangeEnd"):
                    inside = False
                elif inside and el.tag == qn("w:t"):
                    covered += el.text
            self.assertEqual(covered, "98,76")


if __name__ == "__main__":
    unittest.main()
