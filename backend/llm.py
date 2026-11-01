"""Panggilan LLM (Claude di Bedrock, atau Ollama) dan gambar slide untuk LLM. Dipakai book_engine."""
from __future__ import annotations

import io
import time
from pathlib import Path
from typing import Optional

from PIL import Image


LLM_TEMPERATURE = 0.0
IMAGE_MAX_W = 1600         # render slide dikecilkan sebelum dikirim
IMAGE_QUALITY = 80
API_RETRIES = 3            # error jaringan / kuota -> coba ulang dengan jeda 2, 4, 8 detik


def slide_image(render_png: Path) -> bytes:
    with Image.open(render_png) as im:
        im = im.convert("RGB")
        if im.width > IMAGE_MAX_W:
            im = im.resize((IMAGE_MAX_W, round(im.height * IMAGE_MAX_W / im.width)), Image.LANCZOS)
        buf = io.BytesIO()
        im.save(buf, "JPEG", quality=IMAGE_QUALITY)
        return buf.getvalue()


# --------------------------------------------------------------------------- provider
def _bedrock(prompt: str, image: Optional[bytes], model: str) -> str:
    import bedrock_llm

    return bedrock_llm.generate(prompt, image, model)


def _ollama(prompt: str, image: Optional[bytes], model: str) -> str:
    import ollama

    msg = {"role": "user", "content": prompt}
    if image:
        msg["images"] = [image]
    resp = ollama.chat(model=model, messages=[msg], format="json", options={"temperature": LLM_TEMPERATURE})
    return resp["message"]["content"]


def call_llm(prompt: str, image: Optional[bytes], provider: str, model: str) -> str:
    fn = {"bedrock": _bedrock, "ollama": _ollama}.get(provider.lower())
    if fn is None:
        raise ValueError(f"provider LLM tidak dikenal: {provider}")
    for attempt in range(API_RETRIES + 1):
        try:
            return fn(prompt, image, model)
        except (RuntimeError, ValueError, ImportError):
            raise
        except Exception as e:
            # 4xx selain 429 (model salah, key ditolak) tidak akan berhasil dengan mencoba ulang
            if attempt == API_RETRIES or getattr(e, "status_code", getattr(e, "code", None)) in (400, 401, 403, 404):
                raise
            time.sleep(2 ** (attempt + 1))
    return ""
