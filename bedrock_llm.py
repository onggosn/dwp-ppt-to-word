"""Claude di Amazon Bedrock (bedrock-runtime, inference profile) dengan Bedrock API key.

Env (export, atau tulis di file .env di root repo):
  AWS_BEARER_TOKEN_BEDROCK  Bedrock API key (wajib)
  AWS_REGION                region Bedrock, default us-east-1
  BEDROCK_MODEL             inference profile, default us.anthropic.claude-opus-4-6-v1
                            (model terbaik yang aktif di akun ini; prefix us./global. harus cocok dengan region)
"""
from __future__ import annotations

import base64
import os
import re
import threading
from pathlib import Path
from typing import Callable, Optional

try:   # .env di root repo (tidak ikut git); variabel yang sudah di-export tetap menang
    from dotenv import load_dotenv
    load_dotenv(Path(__file__).resolve().parent / ".env")
except ImportError:
    pass

DEFAULT_MODEL = os.environ.get("BEDROCK_MODEL") or "us.anthropic.claude-opus-4-6-v1"
EFFORT = "medium"
MAX_TOKENS = 64000

_client = None
_lock = threading.Lock()


def client():
    global _client
    with _lock:
        if _client is None:
            from anthropic import AnthropicBedrock

            if not os.environ.get("AWS_BEARER_TOKEN_BEDROCK"):
                raise RuntimeError("AWS_BEARER_TOKEN_BEDROCK (Bedrock API key) belum diisi")
            region = os.environ.get("AWS_REGION") or os.environ.get("AWS_DEFAULT_REGION") or "us-east-1"
            _client = AnthropicBedrock(aws_region=region)   # api_key dari AWS_BEARER_TOKEN_BEDROCK
    return _client


def generate(prompt: str, image: Optional[bytes] = None, model: str = DEFAULT_MODEL,
             on_text: Optional[Callable[[int], None]] = None) -> str:
    """Satu permintaan ke Claude; mengembalikan teks jawaban. image: JPEG (render slide).
    on_text(total karakter) dipanggil selama jawaban di-stream."""
    content = []
    if image:
        content.append({"type": "image", "source": {"type": "base64", "media_type": "image/jpeg",
                                                     "data": base64.standard_b64encode(image).decode()}})
    content.append({"type": "text", "text": prompt})
    total = 0
    model = model or DEFAULT_MODEL
    # adaptive thinking + effort hanya untuk Claude 4.6 ke atas; Haiku/Sonnet/Opus 4.5 dan lebih lama menolaknya
    extra = {} if re.search(r"claude-(3|(haiku|sonnet|opus)-4-[0-5]\b)", model) else \
        {"thinking": {"type": "adaptive"}, "output_config": {"effort": EFFORT}}
    with client().messages.stream(
        model=model,
        max_tokens=MAX_TOKENS,
        messages=[{"role": "user", "content": content}],
        **extra,
    ) as stream:
        for piece in stream.text_stream:
            total += len(piece)
            if on_text:
                on_text(total)
        message = stream.get_final_message()
    if message.stop_reason == "refusal":
        raise RuntimeError("Claude menolak permintaan ini (refusal)")
    return "".join(b.text for b in message.content if b.type == "text")
