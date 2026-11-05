"""Completed conversion usage survives API state reloads."""
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import app
from token_usage import TokenUsage


class AppUsageTest(unittest.TestCase):
    def test_usage_is_saved_and_returned_after_reload(self):
        usage = TokenUsage(responses=1, input_tokens=100, output_tokens=20, total_tokens=120).snapshot()
        stats = {key: 0 for key in (
            "title", "slides", "chapters", "slides_used", "llm_calls", "cache_hits",
            "fallback", "comments", "numbers", "rendered", "seconds", "check",
        )}
        stats["token_usage"] = usage

        def convert(pptx, docx, **kwargs):
            docx.write_bytes(b"test document")
            return stats

        with tempfile.TemporaryDirectory() as tmp, patch.object(app, "WORK", Path(tmp)), \
                patch.object(app, "_docs", {}), \
                patch.object(app.book_engine, "convert_book", side_effect=convert):
            doc = app._load("test")
            doc["conversion"] = {"status": "converting", "runId": "run", "steps": []}
            app._run("test", "run", Path("test.pptx"), Path(tmp), 1)
            saved = json.loads((Path(tmp) / "test" / "state.json").read_text(encoding="utf-8"))
            self.assertEqual(saved["conversion"]["stats"]["token_usage"], usage)
            app._docs.clear()
            response = app.app.test_client().get("/api/poc/documents/test")
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json["conversion"]["status"], "complete")
            self.assertEqual(response.json["conversion"]["stats"]["token_usage"], usage)


if __name__ == "__main__":
    unittest.main()
