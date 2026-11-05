"""Token accounting without network calls."""
from concurrent.futures import ThreadPoolExecutor
from contextvars import copy_context
import io
import json
from pathlib import Path
import sys
import threading
from types import SimpleNamespace
import unittest
from unittest.mock import MagicMock, Mock, patch

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import bedrock_llm
import converse_llm
from token_usage import record_usage, track_conversion


class TokenUsageTest(unittest.TestCase):
    def test_isolated_parallel_conversions(self):
        barrier = threading.Barrier(2)

        @track_conversion
        def convert(pptx_path, count):
            barrier.wait(timeout=5)
            with ThreadPoolExecutor(4) as executor:
                futures = [executor.submit(
                    copy_context().run, record_usage, "test-model",
                    input_tokens=10, output_tokens=2, cache_read_input_tokens=3,
                    cache_creation_input_tokens=4, total_tokens=19,
                ) for _ in range(count)]
                for future in futures:
                    future.result()
            return {}

        output = io.StringIO()
        with patch("sys.stdout", output), ThreadPoolExecutor(2) as executor:
            first = executor.submit(convert, "first.pptx", 5)
            second = executor.submit(convert, "second.pptx", 7)
            a, b = first.result()["token_usage"], second.result()["token_usage"]
        for usage, count in ((a, 5), (b, 7)):
            self.assertEqual(usage["responses"], count)
            self.assertEqual(usage["input_tokens"], 10 * count)
            self.assertEqual(usage["output_tokens"], 2 * count)
            self.assertEqual(usage["cache_read_input_tokens"], 3 * count)
            self.assertEqual(usage["cache_creation_input_tokens"], 4 * count)
            self.assertEqual(usage["total_tokens"], 19 * count)
        summaries = [json.loads(line.split(" ", 1)[1]) for line in output.getvalue().splitlines()]
        self.assertEqual(len(summaries), 2)
        self.assertNotEqual(summaries[0]["conversion"], summaries[1]["conversion"])

    def test_failure_and_missing_usage(self):
        @track_conversion
        def convert(pptx_path):
            record_usage("test-model", input_tokens=10, output_tokens=2, total_tokens=12)
            record_usage("test-model")
            raise RuntimeError("failed")

        output = io.StringIO()
        with patch("sys.stdout", output):
            with self.assertRaisesRegex(RuntimeError, "failed"):
                convert("failed.pptx")
            record_usage("outside", input_tokens=100, total_tokens=100)
        summary = json.loads(output.getvalue().split(" ", 1)[1])
        self.assertEqual(summary["status"], "error")
        self.assertEqual(summary["responses"], 2)
        self.assertEqual(summary["missing_usage"], 1)
        self.assertEqual(summary["total_tokens"], 12)

    def test_cached_conversion(self):
        @track_conversion
        def convert(pptx_path):
            return {}

        with patch("sys.stdout"):
            usage = convert(pptx_path="cached.pptx")["token_usage"]
        self.assertEqual(usage["responses"], 0)
        self.assertEqual(usage["total_tokens"], 0)

    def test_provider_usage_is_collected_without_changing_text(self):
        stream = MagicMock()
        stream.text_stream = iter(["answer"])
        stream.get_final_message.return_value = SimpleNamespace(
            usage=SimpleNamespace(input_tokens=10, output_tokens=2,
                                  cache_read_input_tokens=3, cache_creation_input_tokens=4),
            stop_reason="end_turn", content=[SimpleNamespace(type="text", text="answer")],
        )
        claude = MagicMock()
        claude.messages.stream.return_value.__enter__.return_value = stream
        converse = Mock()
        converse.converse.return_value = {
            "usage": {"inputTokens": 10, "outputTokens": 2, "totalTokens": 12},
            "output": {"message": {"content": [{"text": "answer"}]}},
        }

        @track_conversion
        def convert(pptx_path):
            self.assertEqual(bedrock_llm.generate("private prompt", model="claude"), "answer")
            self.assertEqual(converse_llm.generate("private prompt", model="kimi"), "answer")
            return {}

        output = io.StringIO()
        with patch.object(bedrock_llm, "client", return_value=claude), \
                patch.object(converse_llm, "client", return_value=converse), \
                patch("sys.stdout", output):
            usage = convert("test.pptx")["token_usage"]
        self.assertEqual(usage["models"], ["claude", "kimi"])
        self.assertEqual(usage["responses"], 2)
        self.assertEqual(usage["total_tokens"], 31)
        self.assertNotIn("private prompt", output.getvalue())
        self.assertNotIn("answer", output.getvalue())


if __name__ == "__main__":
    unittest.main()
