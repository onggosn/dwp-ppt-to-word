"""Model non-Claude di Amazon Bedrock (mis. Kimi K2.5) lewat Converse API (boto3), dengan Bedrock API key yang sama.

Env (export, atau tulis di backend/.env):
  AWS_BEARER_TOKEN_BEDROCK  Bedrock API key (wajib), dibuat di region AWS_REGION
  AWS_REGION                region Bedrock, mis. ap-southeast-3 (Jakarta)
  CONVERSE_MAX_TOKENS       batas jawaban (default 16000 = batas Kimi K2.5)
"""
from __future__ import annotations

import os
import threading
from pathlib import Path

try:   # .env di backend/ (tidak ikut git); variabel yang sudah di-export tetap menang
    from dotenv import load_dotenv
    load_dotenv(Path(__file__).resolve().parent / ".env")
except ImportError:
    pass

MAX_TOKENS = int(os.environ.get("CONVERSE_MAX_TOKENS") or 16000)
READ_TIMEOUT = 900             # detik; jawaban panjang untuk slide padat bisa lama

_client = None
_lock = threading.Lock()


class ConverseError(Exception):
    """Error dari Bedrock dengan status HTTP, supaya llm.call_llm tahu boleh mencoba ulang atau tidak."""

    def __init__(self, message: str, status_code: int):
        super().__init__(message)
        self.status_code = status_code


def client():
    global _client
    with _lock:
        if _client is None:
            import boto3
            from botocore.config import Config

            if not os.environ.get("AWS_BEARER_TOKEN_BEDROCK"):
                raise RuntimeError("AWS_BEARER_TOKEN_BEDROCK (Bedrock API key) belum diisi")
            region = os.environ.get("AWS_REGION") or os.environ.get("AWS_DEFAULT_REGION") or "ap-southeast-3"
            # coba ulang diatur llm.call_llm; botocore sendiri tidak mengulang
            _client = boto3.client("bedrock-runtime", region_name=region,
                                   config=Config(read_timeout=READ_TIMEOUT, retries={"max_attempts": 1}))
    return _client


def generate(prompt: str, images=None, model: str = "moonshotai.kimi-k2.5") -> str:
    """Satu permintaan; mengembalikan teks jawaban (blok penalaran model dibuang). images: daftar JPEG, urutannya
    dijelaskan di prompt."""
    from botocore.exceptions import ClientError

    imgs = [images] if isinstance(images, (bytes, bytearray)) else list(images or [])
    content = [{"image": {"format": "jpeg", "source": {"bytes": bytes(b)}}} for b in imgs]
    content.append({"text": prompt})
    try:
        resp = client().converse(modelId=model, messages=[{"role": "user", "content": content}],
                                 inferenceConfig={"maxTokens": MAX_TOKENS, "temperature": 0.0})
    except ClientError as e:
        status = e.response.get("ResponseMetadata", {}).get("HTTPStatusCode") or 0
        raise ConverseError(f"{e.response.get('Error', {}).get('Code', '')}: {e}", status) from None
    blocks = resp.get("output", {}).get("message", {}).get("content", [])
    return "".join(b.get("text", "") for b in blocks)
