"""Logika catatan slide add-in (::ignore::, ::penyusun::) tanpa PowerPoint:  python -m unittest discover tests"""
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "addin"))
import dwp_addin as a  # noqa: E402


class SlideNotes(unittest.TestCase):
    def test_ignore(self):
        self.assertEqual(a.add_ignore("")[0], "::ignore::")
        self.assertEqual(a.add_ignore("catatan")[0], "catatan\r::ignore::")
        self.assertIsNone(a.add_ignore("catatan\r::ignore::")[0])

    def test_add_nip_keeps_existing_notes(self):
        self.assertEqual(a.add_nip("catatan pembicara", "123")[0], "catatan pembicara\r::penyusun::\r123")
        self.assertEqual(a.add_nip("", "123")[0], "::penyusun::\r123")
        self.assertEqual(a.add_nip("::penyusun::\r123", "456")[0], "::penyusun::\r123\r456")
        self.assertIsNone(a.add_nip("::penyusun::\r123", "123")[0])

    def test_view_and_remove_nip(self):
        notes = "catatan\r::penyusun::\r123\r456"
        self.assertEqual(a.penyusun(notes), "123\r456")
        self.assertEqual(a.penyusun("catatan"), "")
        self.assertEqual(a.remove_nip(notes, "123")[0], "catatan\r::penyusun::\r456")
        self.assertIsNone(a.remove_nip(notes, "999")[0])


if __name__ == "__main__":
    unittest.main()
