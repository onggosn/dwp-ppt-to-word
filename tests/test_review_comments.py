"""Versi review DOCX: komentar Word dari "Digital Workplace" per slide (tanpa LLM, tanpa PowerPoint)."""
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

import report_engine  # noqa: E402
from docx import Document  # noqa: E402
from report_writer import REVIEWER  # noqa: E402

DECK2 = ROOT / "docs" / "test2.pptx"


class ReviewNotes(unittest.TestCase):
    def sp(self, **kw):
        return report_engine.SlidePlan(n=7, els={}, info={}, plan={"blocks": [], "drop": []}, **kw)

    def test_clean_slide_has_no_comment(self):
        self.assertEqual(report_engine.review_notes(self.sp()), [])

    def test_rules_flags_are_things_to_check(self):
        notes = report_engine.review_notes(self.sp(flags=["uncaptioned", "colour_table"]))
        self.assertEqual(notes[0], "Slide 7: perlu dicek.")
        self.assertEqual(notes[1:], ["- " + report_engine.FLAG_INFO[f][0] for f in ("uncaptioned", "colour_table")])

    def test_llm_plan_says_fixed_by_ai_with_reasons(self):
        for source in ("llm", "cache"):
            notes = report_engine.review_notes(self.sp(source=source, flags=["dense", "llm_fixed"]))
            self.assertTrue(notes[0].startswith("Slide 7: diperbaiki AI."))
            self.assertEqual(notes[1:], ["Alasan dikirim ke AI:", "- " + report_engine.FLAG_INFO["dense"][0]])

    def test_infographic_asks_to_check_the_image(self):
        notes = report_engine.review_notes(self.sp(kind="infographic"))
        self.assertIn("satu gambar", notes[1])


@unittest.skipUnless(DECK2.exists(), "docs/test2.pptx tidak ada")
class ReviewDocx(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.TemporaryDirectory()
        out = Path(cls.tmp.name)
        cls.docx = out / "t2.docx"
        # slide 10: tabel warna (Gantt) -> bertanda; slide 39: aman
        cls.stats = report_engine.convert_report(DECK2, cls.docx, planner="rules", render=False,
                                                 work_dir=out / "build", only={10, 39}, comments=True)

    @classmethod
    def tearDownClass(cls):
        cls.tmp.cleanup()

    def test_one_comment_per_flagged_slide_by_digital_workplace(self):
        comments = list(Document(str(self.docx)).comments)
        self.assertEqual(self.stats["comments"], 1)
        self.assertEqual(len(comments), 1)
        self.assertEqual((comments[0].author, comments[0].initials), (REVIEWER, "DW"))
        self.assertTrue(comments[0].text.startswith("Slide 10: perlu dicek."))

    def test_no_comments_unless_asked(self):
        out = Path(self.tmp.name) / "plain.docx"
        report_engine.convert_report(DECK2, out, planner="rules", render=False,
                                     work_dir=Path(self.tmp.name) / "b2", only={10})
        self.assertEqual(len(list(Document(str(out)).comments)), 0)


if __name__ == "__main__":
    unittest.main()
