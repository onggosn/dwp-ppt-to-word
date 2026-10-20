"""Rencana layout satu slide dengan LLM (dipakai report_engine untuk slide yang sulit).

Masukan: render slide (JPEG) + daftar elemen (id, jenis, posisi, teks) + rencana draf dari aturan.
Keluaran: rencana JSON yang hanya berisi id elemen. LLM tidak pernah menulis teks slide, jadi isi dan
angka di dokumen selalu berasal dari PPTX. Jawaban divalidasi; kalau salah, LLM diberi daftar
kesalahannya dan diminta memperbaiki sekali.
"""
from __future__ import annotations

import io
import json
import os
import re
import threading
import time
from pathlib import Path
from typing import Callable, Optional

from PIL import Image

LLM_TEMPERATURE = 0.0
IMAGE_MAX_W = 1600         # render slide dikecilkan sebelum dikirim
IMAGE_QUALITY = 80
MAX_PARAS = 8              # paragraf per elemen yang ditampilkan di prompt
MAX_PARA_CHARS = 110
FIX_ATTEMPTS = 1           # jawaban tidak sah -> minta perbaikan sebanyak ini
API_RETRIES = 3            # error jaringan / kuota -> coba ulang dengan jeda 2, 4, 8 detik

PROMPT = """You are planning how ONE PowerPoint slide becomes a section of a Word report.
You get the rendered slide image, the list of the slide's elements (id, kind, position and size in % of
slide width/height, text), and a draft plan produced by heuristics that may contain mistakes.

Return ONLY a JSON object: {{"blocks": [...], "drop": [...]}}
You never write or rewrite slide text; you only reference element ids.

Block types:
- {{"type":"heading","level":1,"id":"eN"}}  the slide title (at most one)
- {{"type":"heading","level":2,"id":"eN"}}  heading of a column, panel or section of the slide
- {{"type":"heading","level":3,"id":"eN"}}  small sub-heading inside a section
- {{"type":"text","id":"eN"}}  a text element, written as paragraphs
- {{"type":"table","id":"eN"}}  a native table element (kind "table") written as a Word table
- {{"type":"table","cells":[[["eA"],["eB","eC"]],[["eD"],["eE"]]]}}  a table rebuilt from separate text
  elements laid out as a grid; first row = header; each cell lists the ids whose text goes into it
- {{"type":"figure","ids":["eN",...],"caption":"eM" or null}}  an image cropped from the rendered slide.
  "ids" = every element that makes up the visual: pictures, charts, shapes and the small texts on or inside
  it (axis labels, legends, overlaid labels, stamps). The crop is the bounding box of these ids, so never
  include elements outside the visual. "caption" = the text element that titles the visual (usually a
  short bar or label directly above it); the caption is not repeated in "ids".
- {{"type":"note","id":"eN"}}  source / footnote line at the bottom of the slide
"drop": ids that must not appear: template boilerplate repeated on every slide (e.g. "HASIL PEMBAHASAN
DEWAN GUBERNUR"), stickers ("UPDATED", "Tindak Lanjut", "NEW"), page numbers, logos, decorative shapes,
number badges.

How the report is written:
1. Title first, then the text content in reading order. When the slide has side-by-side columns or panels,
   write one column/panel completely (its heading, then its texts and tables) before the next one, left
   to right. Tables stay in reading order next to the heading/text they belong to.
2. Figures come after all text and tables (they are re-sorted by position afterwards), notes last.
3. Sentences and bullet lists stay text (heading/text blocks) so they remain editable. Never put a long
   text element inside a figure.
4. Charts, pictures, maps, flow/process diagrams, timelines and Gantt bars, and grids whose meaning depends
   on colours, icons, dots or check marks become figures, together with all their small labels.
   A figure's crop must not cover any text that you write as heading/text/table, so never put large
   background pictures, panels, frames or full-width shapes into a figure's "ids".
   Chart panels: the coloured bar or label right above a chart/picture (often an all-caps message like
   "PROSPEK DXY TETAP RENDAH") is that figure's "caption", never a heading. The chart's own small title,
   axis labels, legend and the "Sumber: ..." source line directly under it go into the figure's "ids".
5. A grid of short text boxes that reads as a plain table (header row + rows, no meaning in colours or
   icons) becomes a "cells" table.
6. Every text element appears exactly once: as heading/text/note/table cell, inside a figure's "ids", as a
   figure caption, or in "drop". Shapes and pictures that belong to nothing may be left out.
7. Small icon pictures sitting on a heading are added to the report automatically; leave them out.

Slide elements:
{elements}

Draft plan (heuristics, may be wrong):
{draft}
"""

FIX_PROMPT = """

Your previous answer had these problems:
{errors}

Previous answer:
{previous}

Return the corrected JSON object only."""

_ALLOWED = {"heading": ("type", "level", "id"), "text": ("type", "id"), "note": ("type", "id"),
            "table": ("type", "id", "cells"), "figure": ("type", "ids", "caption")}


def slide_image(render_png: Path) -> bytes:
    with Image.open(render_png) as im:
        im = im.convert("RGB")
        if im.width > IMAGE_MAX_W:
            im = im.resize((IMAGE_MAX_W, round(im.height * IMAGE_MAX_W / im.width)), Image.LANCZOS)
        buf = io.BytesIO()
        im.save(buf, "JPEG", quality=IMAGE_QUALITY)
        return buf.getvalue()


def describe(elements: list) -> str:
    def pct(v):
        return f"{v * 100:.1f}"

    lines = []
    for e in elements:
        head = f'{e["id"]} {e["kind"]} x={pct(e["x"])} y={pct(e["y"])} w={pct(e["w"])} h={pct(e["h"])}'
        if e["kind"] == "text":
            tags = [t for t, on in (("TITLE-PLACEHOLDER", e.get("title")), ("FILLED", e.get("filled"))) if on]
            paras = [p if len(p) <= MAX_PARA_CHARS else p[:MAX_PARA_CHARS] + "…" for p in e["paras"][:MAX_PARAS]]
            more = f' (+{len(e["paras"]) - MAX_PARAS} more paragraphs)' if len(e["paras"]) > MAX_PARAS else ""
            lines.append(f'{head} {" ".join(tags)}: ' + " | ".join(json.dumps(p, ensure_ascii=False) for p in paras)
                         + more)
        elif e["kind"] == "table":
            lines.append(f'{head} {e["size"]} first rows: {json.dumps(e["rows"], ensure_ascii=False)}')
        elif e["kind"] == "picture":
            lines.append(head + (" small-icon" if e.get("small") else ""))
        else:
            lines.append(head)
    return "\n".join(lines)


def parse(raw: str):
    raw = re.sub(r"^```(?:json)?\s*|\s*```$", "", (raw or "").strip())
    data = json.loads(raw, strict=False)   # strict=False: tab / baris baru mentah di dalam string tetap sah
    if isinstance(data, list):        # sebagian model membungkus objek dalam list
        data = data[0] if data else {}
    return sanitize(data)


def sanitize(plan):
    """Buang kunci yang tidak dikenal (mis. "box" atau teks buatan LLM) dan rapikan tipe nilai."""
    if not isinstance(plan, dict):
        return plan
    blocks = []
    for b in plan.get("blocks") or []:
        if not isinstance(b, dict) or b.get("type") not in _ALLOWED:
            blocks.append(b)          # biar validasi yang melaporkan
            continue
        clean = {k: b[k] for k in _ALLOWED[b["type"]] if k in b}
        if "level" in clean:
            try:
                clean["level"] = int(clean["level"])
            except (TypeError, ValueError):
                pass
        if clean.get("caption") in ("", "null"):
            clean["caption"] = None
        blocks.append(clean)
    drop = plan.get("drop") or []
    return {"blocks": blocks, "drop": [k for k in drop if isinstance(k, str)]}


# --------------------------------------------------------------------------- provider
_gemini_client = None
_gemini_lock = threading.Lock()


def _gemini(prompt: str, image: Optional[bytes], model: str) -> str:
    global _gemini_client
    from google import genai
    from google.genai import types

    with _gemini_lock:
        if _gemini_client is None:
            key = os.environ.get("GOOGLE_API_KEY") or os.environ.get("GEMINI_API_KEY")
            if not key:
                raise RuntimeError("GOOGLE_API_KEY / GEMINI_API_KEY belum diisi")
            _gemini_client = genai.Client(api_key=key)
    parts = ([types.Part.from_bytes(data=image, mime_type="image/jpeg")] if image else []) + [prompt]
    resp = _gemini_client.models.generate_content(
        model=model, contents=parts,
        config=types.GenerateContentConfig(temperature=LLM_TEMPERATURE, response_mime_type="application/json"))
    return resp.text or ""


def _ollama(prompt: str, image: Optional[bytes], model: str) -> str:
    import ollama

    msg = {"role": "user", "content": prompt}
    if image:
        msg["images"] = [image]
    resp = ollama.chat(model=model, messages=[msg], format="json", options={"temperature": LLM_TEMPERATURE})
    return resp["message"]["content"]


def call_llm(prompt: str, image: Optional[bytes], provider: str, model: str) -> str:
    fn = {"gemini": _gemini, "ollama": _ollama}.get(provider.lower())
    if fn is None:
        raise ValueError(f"provider LLM tidak dikenal: {provider}")
    for attempt in range(API_RETRIES + 1):
        try:
            return fn(prompt, image, model)
        except (RuntimeError, ValueError, ImportError):
            raise
        except Exception as e:
            # 4xx selain 429 (model salah, key ditolak) tidak akan berhasil dengan mencoba ulang
            if attempt == API_RETRIES or getattr(e, "code", None) in (400, 401, 403, 404):
                raise
            time.sleep(2 ** (attempt + 1))
    return ""


def plan_slide(elements: list, draft: dict, image: Optional[bytes], provider: str, model: str,
               validate: Callable[[dict], list]) -> tuple:
    """Mengembalikan (rencana atau None kalau tetap tidak sah, kesalahan dari setiap jawaban yang ditolak)."""
    prompt = PROMPT.format(elements=describe(elements), draft=json.dumps(draft, ensure_ascii=False))
    ask, history = prompt, []
    for _ in range(FIX_ATTEMPTS + 1):
        raw = call_llm(ask, image, provider, model)
        try:
            plan = parse(raw)
        except (ValueError, IndexError) as e:
            errors = [f"the answer is not valid JSON ({e})"]
        else:
            errors = validate(plan)
            if not errors:
                return plan, history
        history += errors
        ask = prompt + FIX_PROMPT.format(errors="\n".join("- " + e for e in errors), previous=(raw or "")[:6000])
    return None, history
