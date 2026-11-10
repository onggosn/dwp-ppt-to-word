"""Topic panel pagination without LLM calls."""
from pathlib import Path
import sys
import tempfile
import unittest

from PIL import Image

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from book_writer import BookWriter


class TopicPaginationTest(unittest.TestCase):
    def test_text_panels_can_continue_on_next_page(self):
        with tempfile.TemporaryDirectory() as tmp:
            image = Path(tmp) / "panel.png"
            Image.new("RGB", (400, 200), "white").save(image)
            for wide in (False, True):
                with self.subTest(wide=wide):
                    writer = BookWriter()
                    writer.title("Book title")
                    writer.chapter("1", "Chapter")
                    blocks = [{"type": "bullet", "text": "Long panel text. " * 40}] * 20
                    writer.topic("Topic title", [], [(image, "", blocks, wide)])
                    table = writer.doc.tables[0]
                    self.assertTrue(table.rows[0]._tr.xpath("./w:trPr/w:cantSplit"))
                    self.assertFalse(table.rows[1]._tr.xpath("./w:trPr/w:cantSplit"))
                    self.assertTrue(table.cell(0, 0).paragraphs[0].paragraph_format.keep_with_next)
                    panel_text = " ".join(cell.text for cell in table.rows[1].cells)
                    self.assertIn("Long panel text.", panel_text)

    def test_image_only_panels_stay_together(self):
        with tempfile.TemporaryDirectory() as tmp:
            image = Path(tmp) / "panel.png"
            Image.new("RGB", (400, 200), "white").save(image)
            writer = BookWriter()
            writer.topic("Topic title", [], [(image, "Caption", [], True)])
            for row in writer.doc.tables[0].rows:
                self.assertTrue(row._tr.xpath("./w:trPr/w:cantSplit"))


if __name__ == "__main__":
    unittest.main()
