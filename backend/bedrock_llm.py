"""Claude di Amazon Bedrock (bedrock-runtime, inference profile) dengan Bedrock API key.

Env (export, atau tulis di backend/.env):
  AWS_BEARER_TOKEN_BEDROCK  Bedrock API key (wajib)
  AWS_REGION                region Bedrock, default us-east-1
  AWS_CA_BUNDLE             path PEM CA bundle opsional untuk verifikasi TLS
  BEDROCK_MODEL             inference profile, default global.anthropic.claude-opus-4-6-v1
                            (model terbaik yang aktif di akun ini; global. jalan di semua region; us./eu./apac. hanya di region-nya)
"""
from __future__ import annotations

import base64
import os
import re
import ssl
import threading
from pathlib import Path
from typing import Callable, Optional, Union

from token_usage import record_usage

try:   # .env di root repo (tidak ikut git); variabel yang sudah di-export tetap menang
    from dotenv import load_dotenv
    load_dotenv(Path(__file__).resolve().parent / ".env")
except ImportError:
    pass

DEFAULT_MODEL = os.environ.get("BEDROCK_MODEL") or "global.anthropic.claude-opus-4-6-v1"
BEDROCK_API_VERSION = "bedrock-2023-05-31"
EFFORT = "medium"
MAX_TOKENS = 64000

_client = None
_lock = threading.Lock()


def client():
    global _client
    with _lock:
        if _client is None:
            from anthropic import AnthropicBedrock, DefaultHttpxClient

            if not os.environ.get("AWS_BEARER_TOKEN_BEDROCK"):
                raise RuntimeError("AWS_BEARER_TOKEN_BEDROCK (Bedrock API key) belum diisi")
            region = os.environ.get("AWS_REGION") or os.environ.get("AWS_DEFAULT_REGION") or "us-east-1"
            ca_bundle = os.environ.get("AWS_CA_BUNDLE")
            if ca_bundle:
                context = ssl.create_default_context(cafile=ca_bundle)
                _client = AnthropicBedrock(
                    aws_region=region,
                    http_client=DefaultHttpxClient(verify=context),
                )
            else:
                _client = AnthropicBedrock(aws_region=region)
    return _client


def generate(prompt: str, image: Union[bytes, list, None] = None, model: str = DEFAULT_MODEL,
             on_text: Optional[Callable[[int], None]] = None) -> str:
    """Satu permintaan ke Claude; mengembalikan teks jawaban. image: JPEG (render slide), atau daftar JPEG
    (render slide lalu crop grafik, urutannya dijelaskan di prompt).
    on_text(total karakter) dipanggil selama jawaban di-stream."""
    content = []
    for img in ([image] if isinstance(image, (bytes, bytearray)) else image or []):
        content.append({"type": "image", "source": {"type": "base64", "media_type": "image/jpeg",
                                                     "data": base64.standard_b64encode(img).decode()}})
    content.append({"type": "text", "text": prompt})
    total = 0
    model = model or DEFAULT_MODEL
    # adaptive thinking + effort hanya untuk Claude 4.6 ke atas; Haiku/Sonnet/Opus 4.5 dan lebih lama menolaknya
    body = {"anthropic_version": BEDROCK_API_VERSION}
    if re.search(r"claude-(3|(haiku|sonnet|opus)-4-[0-5]\b)", model):
        # model tanpa thinking: temperature 0 supaya hasil konversi dan cek angka tidak berubah-ubah antar run
        # (SDK anthropic 2.x tidak punya argumen temperature lagi; Bedrock masih menerimanya di body)
        extra, body["temperature"] = {}, 0.0
    else:
        extra = {"thinking": {"type": "adaptive"}, "output_config": {"effort": EFFORT}}
    with client().messages.stream(
        model=model,
        max_tokens=MAX_TOKENS,
        messages=[{"role": "user", "content": content}],
        # SDK anthropic >= 2.x mengirim versi API baru ("2026-10-21") yang ditolak Bedrock untuk
        # Opus 4.5 / 4.6 ("Invalid API version"); versi Bedrock ini diterima semua model Claude
        extra_body=body,
        **extra,
    ) as stream:
        for piece in stream.text_stream:
            total += len(piece)
            if on_text:
                on_text(total)
        message = stream.get_final_message()
    usage = message.usage
    cache_read = usage.cache_read_input_tokens or 0
    cache_creation = usage.cache_creation_input_tokens or 0
    record_usage(
        model, input_tokens=usage.input_tokens, output_tokens=usage.output_tokens,
        cache_read_input_tokens=cache_read, cache_creation_input_tokens=cache_creation,
        total_tokens=usage.input_tokens + usage.output_tokens + cache_read + cache_creation,
    )
    if message.stop_reason == "refusal":
        raise RuntimeError("Claude menolak permintaan ini (refusal)")
    return "".join(b.text for b in message.content if b.type == "text")
