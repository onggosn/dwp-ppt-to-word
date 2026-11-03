"""Panggilan LLM (Claude atau model lain di Bedrock, atau Ollama) dan gambar slide untuk LLM. Dipakai book_engine."""
from __future__ import annotations

import io
import re
import time
from pathlib import Path
from typing import Union

from PIL import Image

Images = Union[bytes, list, None]   # satu gambar, beberapa gambar (urutannya dijelaskan di prompt), atau tanpa gambar


LLM_TEMPERATURE = 0.0
IMAGE_MAX_W = 1600         # render slide dikecilkan sebelum dikirim
IMAGE_QUALITY = 80
CROP_MAX_SIDE = 1568       # crop gambar/grafik: sisi terpanjang (Claude mengecilkan gambar yang lebih besar)
CROP_MAX_PIXELS = 1_150_000   # ... dan jumlah piksel maksimum sebelum Claude mengecilkannya
API_RETRIES = 3            # error jaringan / kuota -> coba ulang dengan jeda 2, 4, 8 detik


def slide_image(render_png: Path) -> bytes:
    with Image.open(render_png) as im:
        im = im.convert("RGB")
        if im.width > IMAGE_MAX_W:
            im = im.resize((IMAGE_MAX_W, round(im.height * IMAGE_MAX_W / im.width)), Image.LANCZOS)
        buf = io.BytesIO()
        im.save(buf, "JPEG", quality=IMAGE_QUALITY)
        return buf.getvalue()


def crop_image(im: Image.Image) -> bytes:
    """JPEG crop grafik/tabel untuk LLM, diperbesar/diperkecil ke ukuran terbaik untuk Claude (sisi terpanjang
    CROP_MAX_SIDE, paling banyak CROP_MAX_PIXELS): huruf kecil di label grafik jadi lebih mudah dibaca. Bagian
    transparan (PNG) jadi putih, bukan hitam, supaya teks gelap tetap terbaca."""
    if im.mode in ("RGBA", "LA", "P"):
        im = im.convert("RGBA")
        bg = Image.new("RGB", im.size, "white")
        bg.paste(im, mask=im.getchannel("A"))
        im = bg
    im = im.convert("RGB")
    scale = min(CROP_MAX_SIDE / max(im.size), (CROP_MAX_PIXELS / (im.width * im.height)) ** 0.5)
    if abs(scale - 1) > 0.02:
        im = im.resize((max(1, round(im.width * scale)), max(1, round(im.height * scale))), Image.LANCZOS)
    buf = io.BytesIO()
    im.save(buf, "JPEG", quality=IMAGE_QUALITY)
    return buf.getvalue()


def tiles(im: Image.Image, max_aspect: float = 2.0, max_tiles: int = 3, overlap: float = 0.06) -> list:
    """Gambar yang sangat lebar (tabel banyak kolom) atau tinggi dipotong jadi beberapa bagian yang saling
    menimpa sedikit. Dikirim utuh, tabel 20+ kolom dikecilkan Claude sampai kolomnya tertukar saat dibaca."""
    W, H = im.size
    wide = W >= H
    aspect = W / H if wide else H / W
    n = min(max_tiles, max(1, -(-int(aspect * 100) // int(max_aspect * 100))))
    if n == 1:
        return [im]
    L = W if wide else H
    out = []
    for i in range(n):
        a, b = max(0, int(i * L / n - overlap * L)), min(L, int((i + 1) * L / n + overlap * L))
        out.append(im.crop((a, 0, b, H) if wide else (0, a, W, b)))
    return out


def image_list(images: Images) -> list:
    if not images:
        return []
    return [images] if isinstance(images, (bytes, bytearray)) else [i for i in images if i]


# --------------------------------------------------------------------------- provider
def is_claude(model: str) -> bool:
    """ID Claude di Bedrock: anthropic.… atau profil global./us./apac.anthropic.…"""
    return bool(re.search(r"(^|\.)anthropic\.", model or ""))


def _bedrock(prompt: str, images: Images, model: str) -> str:
    """Claude lewat Anthropic SDK (bedrock_llm); model lain di Bedrock (Kimi, Nova, ...) lewat Converse API."""
    if is_claude(model):
        import bedrock_llm

        return bedrock_llm.generate(prompt, image_list(images), model)
    import converse_llm

    return converse_llm.generate(prompt, image_list(images), model)


def _ollama(prompt: str, images: Images, model: str) -> str:
    import ollama

    msg = {"role": "user", "content": prompt}
    if image_list(images):
        msg["images"] = image_list(images)
    resp = ollama.chat(model=model, messages=[msg], format="json", options={"temperature": LLM_TEMPERATURE})
    return resp["message"]["content"]


def call_llm(prompt: str, image: Images, provider: str, model: str) -> str:
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
