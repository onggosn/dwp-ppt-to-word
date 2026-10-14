"""
PPTX -> Word pipeline: Docling (PPTX -> HTML + figures) -> optional LLM text cleanup -> Pandoc (.docx).

Install:
    pip install docling pypandoc_binary beautifulsoup4 ollama google-genai
Gemini key: set the GOOGLE_API_KEY environment variable (never hard-code it).

CLI:
    python pipeline.py test.pptx -o Report_Output.docx --provider ollama --model qwen2.5-coder:7b
"""
from __future__ import annotations

import argparse
import os
import re
import tempfile
from pathlib import Path
from typing import Callable, Optional

from bs4 import BeautifulSoup

ProgressFn = Callable[[float, str], None]


def _noop(_: float, __: str) -> None:
    pass


# --------------------------------------------------------------------------- #
# Step 1: PPTX -> HTML (+ figures) with Docling
# --------------------------------------------------------------------------- #
def pptx_to_html(pptx_path: Path, out_dir: Path) -> Path:
    from docling.document_converter import DocumentConverter
    from docling_core.types.doc.document import ImageRefMode

    out_dir.mkdir(parents=True, exist_ok=True)
    result = DocumentConverter().convert(str(pptx_path))  # PPTX uses the CPU-only parser
    html_path = out_dir / f"{pptx_path.stem}.html"
    # save_as_html writes the images to "<name>_artifacts/" next to the HTML and links them
    # with paths relative to the HTML file (export_to_html does not write image files).
    result.document.save_as_html(html_path, image_mode=ImageRefMode.REFERENCED)
    return html_path


# --------------------------------------------------------------------------- #
# Step 2: LLM cleanup, chunked and validated
# --------------------------------------------------------------------------- #
PROMPT = """You fix and format text inside an HTML fragment extracted from presentation slides.

Do:
- merge lines that were broken in the middle of a sentence, fix typos, improve paragraph flow;
- keep headings, lists and tables as proper HTML (<h1>-<h3>, <ul>/<li>, <table>).
{reference_rule}
Strict rules:
1. Keep the ORIGINAL LANGUAGE. Do not translate.
2. Never delete, shorten, summarize or invent content. Every sentence and number must remain.
3. Every <img> tag must stay exactly as it is, including its src attribute.
4. Output ONLY the HTML fragment: no explanations, no markdown fences, no <html> or <body> tags.
{reference_block}
HTML fragment to fix:
{fragment}
"""

REFERENCE_RULE = ("- follow the heading levels, list style and general structure shown in the "
                  "REFERENCE HTML below (the reference is for style only; never copy its content).\n")


def _strip_fences(text: str) -> str:
    text = text.strip()
    text = re.sub(r"^```(?:html)?\s*", "", text)
    text = re.sub(r"\s*```$", "", text)
    return text.strip()


def split_html(html: str, max_chars: int) -> tuple[str, list[str], str]:
    """Split a full HTML page into (head, body chunks, tail). Chunks end on element boundaries."""
    soup = BeautifulSoup(html, "html.parser")
    body = soup.body
    if body is None:
        return "", [html], ""
    m = re.search(r"<body[^>]*>", html, flags=re.IGNORECASE)
    head = html[: m.end()] if m else ""
    chunks, current = [], ""
    for child in body.children:
        piece = str(child)
        if not piece.strip():
            continue
        if current and len(current) + len(piece) > max_chars:
            chunks.append(current)
            current = ""
        current += piece + "\n"
    if current.strip():
        chunks.append(current)
    return head, chunks, "\n</body>\n</html>\n"


def _img_srcs(fragment: str) -> list[str]:
    return [i.get("src", "") for i in BeautifulSoup(fragment, "html.parser").find_all("img")]


def _text_len(fragment: str) -> int:
    return len(re.sub(r"\s+", "", BeautifulSoup(fragment, "html.parser").get_text()))


def is_safe_rewrite(original: str, cleaned: str) -> bool:
    """Accept the LLM output only if images are intact and no real amount of text went missing."""
    if sorted(_img_srcs(original)) != sorted(_img_srcs(cleaned)):
        return False
    before, after = _text_len(original), _text_len(cleaned)
    if before == 0:
        return True
    return 0.85 <= after / before <= 1.3


def call_llm(prompt: str, provider: str, model: str, api_key: Optional[str]) -> str:
    provider = provider.lower()
    if provider == "ollama":
        import ollama
        # trust_env=False: ignore corporate proxy settings for the local server.
        client = ollama.Client(host=_ollama_host(), trust_env=False, timeout=600)
        resp = client.chat(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            # Ollama's default context is small and silently truncates long prompts.
            options={"temperature": 0, "num_ctx": 8192},
        )
        return resp["message"]["content"]
    if provider == "gemini":
        from google import genai
        key = api_key or os.environ.get("GOOGLE_API_KEY")
        if not key:
            raise RuntimeError("Gemini selected but no API key was provided (GOOGLE_API_KEY).")
        resp = genai.Client(api_key=key).models.generate_content(model=model, contents=prompt)
        return resp.text or ""
    raise ValueError(f"Unknown provider: {provider}")


def _ollama_host() -> str:
    host = (os.environ.get("OLLAMA_HOST") or "http://127.0.0.1:11434").strip()
    if not host.startswith(("http://", "https://")):
        host = "http://" + host
    scheme, rest = host.split("://", 1)
    name, _, port = rest.rstrip("/").partition(":")
    if name in ("", "0.0.0.0", "::", "[::]", "localhost"):
        name = "127.0.0.1"
    return f"{scheme}://{name}:{port or 11434}"


def clean_html(
    html_path: Path,
    provider: str = "ollama",
    model: str = "qwen2.5-coder:7b",
    api_key: Optional[str] = None,
    reference_html: Optional[Path] = None,
    max_chars: int = 4000,
    progress: ProgressFn = _noop,
) -> tuple[Path, dict]:
    """Rewrite text chunk by chunk. A chunk the LLM damages (lost image/text) is kept as original."""
    html = html_path.read_text(encoding="utf-8", errors="ignore")
    head, chunks, tail = split_html(html, max_chars)

    reference_rule, reference_block = "", ""
    if reference_html and Path(reference_html).exists():
        ref = Path(reference_html).read_text(encoding="utf-8", errors="ignore")
        ref_body = BeautifulSoup(ref, "html.parser").body
        excerpt = (str(ref_body) if ref_body else ref)[:3000]  # a style sample is enough
        reference_rule = REFERENCE_RULE
        reference_block = f"\n--- REFERENCE HTML (style only) ---\n{excerpt}\n-----------------------------------\n"

    stats = {"chunks": len(chunks), "refined": 0, "kept_original": 0, "errors": 0}
    out = []
    for i, chunk in enumerate(chunks, start=1):
        progress(i / max(len(chunks), 1), f"Refining text, section {i} of {len(chunks)}")
        prompt = PROMPT.format(reference_rule=reference_rule,
                               reference_block=reference_block, fragment=chunk)
        try:
            cleaned = _strip_fences(call_llm(prompt, provider, model, api_key))
        except ConnectionError:
            raise  # server unreachable: fail now instead of looping through every chunk
        except Exception:
            stats["errors"] += 1
            cleaned = ""
        if cleaned and is_safe_rewrite(chunk, cleaned):
            out.append(cleaned)
            stats["refined"] += 1
        else:
            out.append(chunk)
            stats["kept_original"] += 1

    cleaned_path = html_path.with_name(html_path.stem + "_cleaned.html")
    cleaned_path.write_text(head + "\n".join(out) + tail, encoding="utf-8")
    return cleaned_path, stats


# --------------------------------------------------------------------------- #
# Step 3: HTML -> DOCX with Pandoc
# --------------------------------------------------------------------------- #
def html_to_docx(html_path: Path, docx_path: Path, reference_docx: Optional[Path] = None) -> Path:
    import pypandoc

    try:
        pypandoc.get_pandoc_version()
    except OSError:
        raise RuntimeError("Pandoc was not found. Run: pip install pypandoc_binary")

    args = [f"--resource-path={html_path.parent.resolve()}"]  # so figures/ images are found
    if reference_docx and Path(reference_docx).exists():
        args.append(f"--reference-doc={Path(reference_docx).resolve()}")
    pypandoc.convert_file(str(html_path), "docx", format="html",
                          outputfile=str(docx_path), extra_args=args)
    return docx_path


# --------------------------------------------------------------------------- #
# Orchestration
# --------------------------------------------------------------------------- #
def convert_presentation(
    pptx_path: str | Path,
    docx_path: str | Path,
    provider: str = "none",          # "none" | "ollama" | "gemini"
    model: str = "qwen2.5-coder:7b",
    api_key: Optional[str] = None,
    reference_html: Optional[str | Path] = None,
    work_dir: Optional[str | Path] = None,
    progress: ProgressFn = _noop,
) -> dict:
    pptx_path, docx_path = Path(pptx_path), Path(docx_path)
    work = Path(work_dir) if work_dir else Path(tempfile.mkdtemp(prefix="pptx2docx_"))

    progress(0.05, "Reading the presentation")
    html_path = pptx_to_html(pptx_path, work)
    n_images = len(_img_srcs(html_path.read_text(encoding="utf-8", errors="ignore")))

    stats = {"images": n_images}
    if provider.lower() != "none":
        def scaled(f: float, msg: str) -> None:
            progress(0.25 + 0.6 * f, msg)
        progress(0.25, "Refining text")
        html_path, llm_stats = clean_html(html_path, provider, model, api_key,
                                          Path(reference_html) if reference_html else None,
                                          progress=scaled)
        stats.update(llm_stats)

    progress(0.9, "Creating the Word document")
    html_to_docx(html_path, docx_path)
    progress(1.0, "Done")
    stats["docx"] = str(docx_path)
    return stats


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="Convert a PPTX to Word via Docling + optional LLM cleanup")
    ap.add_argument("pptx")
    ap.add_argument("-o", "--output", default="Report_Output.docx")
    ap.add_argument("--provider", choices=["none", "ollama", "gemini"], default="none")
    ap.add_argument("--model", default="qwen2.5-coder:7b")
    ap.add_argument("--reference-html", default=None)
    a = ap.parse_args()
    print(convert_presentation(a.pptx, a.output, a.provider, a.model,
                               reference_html=a.reference_html,
                               progress=lambda f, m: print(f"[{f:4.0%}] {m}")))