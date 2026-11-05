"""Bedrock TLS configuration without real LLM calls."""
import os
from pathlib import Path
import ssl
import sys
import tempfile
from types import SimpleNamespace
import unittest
from unittest.mock import Mock, patch

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import bedrock_llm


class BedrockClientTest(unittest.TestCase):
    def setUp(self):
        self.sdk = SimpleNamespace(AnthropicBedrock=Mock(), DefaultHttpxClient=Mock())
        self.environment = patch.dict(os.environ, {
            "AWS_BEARER_TOKEN_BEDROCK": "test-key",
            "AWS_REGION": "ap-southeast-3",
            "AWS_CA_BUNDLE": "",
        })
        self.environment.start()
        self.addCleanup(self.environment.stop)
        self.modules = patch.dict(sys.modules, {"anthropic": self.sdk})
        self.modules.start()
        self.addCleanup(self.modules.stop)
        self.cached_client = patch.object(bedrock_llm, "_client", None)
        self.cached_client.start()
        self.addCleanup(self.cached_client.stop)

    def test_default_sdk_certificates(self):
        result = bedrock_llm.client()
        self.sdk.AnthropicBedrock.assert_called_once_with(aws_region="ap-southeast-3")
        self.sdk.DefaultHttpxClient.assert_not_called()
        self.assertIs(result, bedrock_llm.client())

    def test_custom_ca_bundle(self):
        os.environ["AWS_CA_BUNDLE"] = r"C:\certificates\company-ca.pem"
        context = ssl.create_default_context()
        with patch.object(bedrock_llm.ssl, "create_default_context", return_value=context) as create:
            bedrock_llm.client()
        create.assert_called_once_with(cafile=r"C:\certificates\company-ca.pem")
        self.sdk.DefaultHttpxClient.assert_called_once_with(verify=context)
        self.sdk.AnthropicBedrock.assert_called_once_with(
            aws_region="ap-southeast-3",
            http_client=self.sdk.DefaultHttpxClient.return_value,
        )
        self.assertEqual(context.verify_mode, ssl.CERT_REQUIRED)
        self.assertTrue(context.check_hostname)

    def test_invalid_bundle_fails_without_creating_client(self):
        with tempfile.TemporaryDirectory() as directory:
            bundle = Path(directory) / "invalid.pem"
            bundle.write_text("not a certificate", encoding="ascii")
            os.environ["AWS_CA_BUNDLE"] = str(bundle)
            with self.assertRaises(ssl.SSLError):
                bedrock_llm.client()
            os.environ["AWS_CA_BUNDLE"] = str(Path(directory) / "missing.pem")
            with self.assertRaises(FileNotFoundError):
                bedrock_llm.client()
        self.sdk.AnthropicBedrock.assert_not_called()
        self.sdk.DefaultHttpxClient.assert_not_called()
        self.assertIsNone(bedrock_llm._client)


if __name__ == "__main__":
    unittest.main()
