import os
import re
import shutil
import subprocess
import torch
import pypandoc
import ollama
from pathlib import Path
from bs4 import BeautifulSoup, Comment

import bedrock_llm

from docling.document_converter import DocumentConverter, PowerpointFormatOption, PdfFormatOption
from docling.datamodel.base_models import InputFormat
from docling.datamodel.pipeline_options import PaginatedPipelineOptions, PdfPipelineOptions
from docling.datamodel.accelerator_options import AcceleratorOptions, AcceleratorDevice
from docling_core.types.doc.document import ImageRefMode

from docx import Document  # pip install python-docx
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Inches, Mm

# =================================================================
# AWS BEDROCK API KEY (only needed for the Bedrock provider)
# Set it as an environment variable: AWS_BEARER_TOKEN_BEDROCK (+ AWS_REGION)
# =================================================================
DEFAULT_BEDROCK_MODEL = bedrock_llm.DEFAULT_MODEL


def check_cuda_availability():
    print("Memeriksa status perangkat keras (CUDA)...")
    if torch.cuda.is_available():
        print(f"  [✔] CUDA Aktif! Menggunakan GPU: {torch.cuda.get_device_name(0)}")
    else:
        print("  [!] Peringatan: CUDA tidak terdeteksi. Docling berjalan menggunakan CPU.")


def convert_pptx_to_pdf(pptx_path, output_dir="./output"):
    """PPTX -> PDF with LibreOffice (headless). Returns the PDF path."""
    soffice = shutil.which("soffice") or shutil.which("libreoffice")
    if not soffice:
        for p in (
            r"C:\Program Files\LibreOffice\program\soffice.exe",
            r"C:\Program Files (x86)\LibreOffice\program\soffice.exe",
            "/Applications/LibreOffice.app/Contents/MacOS/soffice",
        ):
            if os.path.exists(p):
                soffice = p
                break
    if not soffice:
        raise RuntimeError("LibreOffice was not found. Install it (or add 'soffice' to PATH) to use the PDF route.")

    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)
    print(f"Mengonversi {pptx_path} ke PDF menggunakan LibreOffice...")
    subprocess.run(
        [soffice, "--headless", "--convert-to", "pdf", "--outdir", str(out), str(pptx_path)],
        check=True, capture_output=True, timeout=600,
    )
    pdf = out / (Path(pptx_path).stem + ".pdf")
    if not pdf.exists():
        raise RuntimeError("LibreOffice did not produce a PDF file.")
    return str(pdf)


def convert_document_to_html_with_docling(source_path, output_dir="./output"):
    """Docling -> HTML + figures. Works for .pptx (PPTX reader) and .pdf (PDF pipeline)."""
    src = Path(source_path)
    is_pdf = src.suffix.lower() == ".pdf"
    print(f"Memproses {src} menggunakan Docling ({'PDF' if is_pdf else 'PPTX'} pipeline)...")
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    accel = AcceleratorOptions(num_threads=4, device=AcceleratorDevice.AUTO)
    if is_pdf:
        opts = PdfPipelineOptions()
        opts.generate_picture_images = True
        opts.images_scale = 2.0
        opts.accelerator_options = accel
        format_options = {InputFormat.PDF: PdfFormatOption(pipeline_options=opts)}
    else:
        opts = PaginatedPipelineOptions()
        opts.generate_picture_images = True
        opts.images_scale = 2.0
        opts.accelerator_options = accel
        format_options = {InputFormat.PPTX: PowerpointFormatOption(pipeline_options=opts)}

    doc = DocumentConverter(format_options=format_options).convert(str(src)).document

    if not is_pdf:
        remove_off_slide_elements(doc)

    html_file_path = output_path / f"{src.stem}.html"
    # A RELATIVE artifacts_dir is resolved against the HTML file's folder -> src="figures/xxx.png"
    doc.save_as_html(
        filename=html_file_path,
        artifacts_dir=Path("figures"),
        image_mode=ImageRefMode.REFERENCED,
    )
    print(f"  [+] Berkas HTML & Gambar berhasil dibuat di: {output_dir}")
    return str(html_file_path)


def convert_pptx_to_html_with_docling(pptx_path, output_dir="./output", via_pdf=False):
    """Convenience wrapper: optionally go PPTX -> PDF first."""
    source = convert_pptx_to_pdf(pptx_path, output_dir) if via_pdf else pptx_path
    return convert_document_to_html_with_docling(source, output_dir)


def remove_off_slide_elements(doc):
    """Remove elements whose bounding box is entirely outside the slide canvas."""

    def filter_node(node):
        if hasattr(node, "children") and node.children:
            valid_children = []
            for child_ref in node.children:
                item = child_ref.resolve(doc) if hasattr(child_ref, "resolve") else child_ref
                is_inside_canvas = True

                try:
                    if getattr(item, "prov", None):
                        prov = item.prov[0]
                        bbox = prov.bbox
                        page_info = doc.pages.get(prov.page_no)  # FIX: page_no lives on prov, not bbox

                        if page_info is not None and getattr(page_info, "size", None):
                            slide_w, slide_h = page_info.size.width, page_info.size.height
                            x_left, x_right = bbox.l, bbox.r
                            y_a, y_b = sorted((bbox.t, bbox.b))
                            if x_right <= 0 or x_left >= slide_w or y_b <= 0 or y_a >= slide_h:
                                is_inside_canvas = False
                except Exception:
                    pass  # keep the element if its geometry can't be read

                if is_inside_canvas:
                    filter_node(item)
                    valid_children.append(child_ref)

            node.children = valid_children

    if hasattr(doc, "body"):
        filter_node(doc.body)
        print("  [✔] Off-slide objects have been successfully removed.")


def sanitize_html_for_llm(html_str):
    """Strip <head>/<style> to speed up the LLM."""
    html_str = re.sub(r"<style.*?>.*?</style>", "", html_str, flags=re.DOTALL)
    html_str = re.sub(r"<head.*?>.*?</head>", "", html_str, flags=re.DOTALL)
    return html_str.strip()


def _span(cell):
    try:
        return max(1, int(cell.get("colspan", 1)))
    except (TypeError, ValueError):
        return 1


def apply_deterministic_html_styles(html_str):
    """Python-only rules (no LLM): black 1px borders, images fit their column,
    and 2-column tables always get 50/50 columns."""
    soup = BeautifulSoup(html_str, "html.parser")

    for img in soup.find_all("img"):
        img["style"] = "max-width: 100%; height: auto;"

    for table in soup.find_all("table"):
        rows = table.find_all("tr")
        ncols = max((sum(_span(c) for c in r.find_all(["td", "th"], recursive=False)) for r in rows), default=0)
        two_col = ncols == 2

        table["border"] = "1"
        style = "border-collapse: collapse; width: 100%; border: 1px solid #000000;"
        if two_col:
            style += " table-layout: fixed;"
            for old in table.find_all("colgroup"):
                old.decompose()
            colgroup = soup.new_tag("colgroup")
            for _ in range(2):
                colgroup.append(soup.new_tag("col", style="width: 50%;"))
            table.insert(0, colgroup)
        table["style"] = style

        for cell in table.find_all(["td", "th"]):
            width = " width: 50%;" if two_col and _span(cell) == 1 else ""
            existing = cell.get("style", "")
            cell["style"] = f"border: 1px solid #000000; padding: 6px; vertical-align: top;{width} {existing}".strip()

    return str(soup)


# Merapikan HTML butuh hasil konsisten, bukan kreatif: dipakai oleh Ollama.
LLM_TEMPERATURE = 0.0


def _call_llm(prompt, provider, model_name, progress_cb=None):
    """Returns the raw LLM text, or None if the provider isn't usable."""
    provider = provider.lower()

    if provider == "bedrock":
        if not os.environ.get("AWS_BEARER_TOKEN_BEDROCK"):
            print("  [!] AWS_BEARER_TOKEN_BEDROCK belum diisi. Melewati proses perapian LLM.")
            return None

        def on_text(total):
            if progress_cb:
                progress_cb(total)
            print(f"\r  [LLM] menerima respons... {total} karakter", end="", flush=True)

        text = bedrock_llm.generate(prompt, model=model_name, on_text=on_text)
        print()
        return text

    if provider == "ollama":
        parts, total = [], 0
        for chunk in ollama.chat(
            model=model_name,
            messages=[{"role": "user", "content": prompt}],
            options={"temperature": LLM_TEMPERATURE},
            stream=True,
        ):
            piece = chunk["message"]["content"]
            parts.append(piece)
            total += len(piece)
            if progress_cb:
                progress_cb(total)
        return "".join(parts)

    print(f"  [!] Provider LLM '{provider}' tidak dikenal. Menggunakan HTML asli.")
    return None


def _slim_and_extract_tables(html_str, drop_tables=False):
    """Shrink the HTML before sending it to the LLM:
    - remove <head>/<style>/comments and every attribute except img src/width/height
    - swap each top-level <table> for a [[TABLE_n]] placeholder (restored afterwards)
    Returns (slim_html, [original table html, ...])."""
    soup = BeautifulSoup(sanitize_html_for_llm(html_str), "html.parser")
    for c in soup.find_all(string=lambda t: isinstance(t, Comment)):
        c.extract()

    tables = []
    for t in soup.find_all("table"):
        if t.find_parent("table"):
            continue
        if drop_tables:
            t.decompose()
            continue
        tables.append(str(t))
        p = soup.new_tag("p")
        p.string = f"[[TABLE_{len(tables) - 1}]]"
        t.replace_with(p)

    for tag in soup.find_all(True):
        keep = ("src", "width", "height") if tag.name == "img" else ()
        tag.attrs = {k: v for k, v in tag.attrs.items() if k in keep}
    return str(soup), tables


def _restore_tables(llm_html, tables):
    """Put the original tables back where the [[TABLE_n]] placeholders are."""
    missing = []
    for i, table_html in enumerate(tables):
        token = re.escape(f"[[TABLE_{i}]]")
        pattern = re.compile(r"<p[^>]*>\s*" + token + r"\s*</p>|" + token)
        if pattern.search(llm_html):
            llm_html = pattern.sub(lambda m: table_html, llm_html, count=1)
        else:
            missing.append(table_html)
    if missing:
        print(f"  [!] {len(missing)} tabel hilang dari output LLM - ditambahkan di akhir dokumen.")
        llm_html += "\n" + "\n".join(missing)
    return llm_html


def _reference_digest(ref_html, limit=6000):
    """Short style sample of the reference file (no tables/images, truncated)."""
    slim, _ = _slim_and_extract_tables(ref_html, drop_tables=True)
    soup = BeautifulSoup(slim, "html.parser")
    for img in soup.find_all("img"):
        img.decompose()
    return str(soup)[:limit]


def clean_html_with_llm(html_path, reference_html_path=None, provider="bedrock", model_name=DEFAULT_BEDROCK_MODEL, progress_cb=None):
    skip_llm = provider.lower() == "none"
    if skip_llm:
        print("Melewati LLM (mode tanpa LLM) - hanya aturan Python yang diterapkan...")
    else:
        print(f"Merapikan HTML menggunakan {provider.upper()} (Model: '{model_name}')...")

    if not os.path.exists(html_path):
        print(f"Error: Berkas HTML {html_path} tidak ditemukan.")
        return None

    with open(html_path, "r", encoding="utf-8", errors="ignore") as f:
        raw_html = f.read()

    cleaned_html = None
    if not skip_llm:
        slim_html, tables = _slim_and_extract_tables(raw_html)
        print(f"  [i] Input LLM diperkecil: {len(raw_html)} -> {len(slim_html)} karakter, {len(tables)} tabel dipisahkan.")

        reference_instruction = ""
        reference_content = ""
        if reference_html_path and os.path.exists(reference_html_path):
            print(f"  [i] Menggunakan file referensi: {reference_html_path}")
            with open(reference_html_path, "r", encoding="utf-8", errors="ignore") as ref_f:
                digest = _reference_digest(ref_f.read())
            reference_instruction = (
                "Analyze the structural style, heading levels, and list formatting of the REFERENCE HTML "
                "(a shortened sample) and apply those styling standards to the TARGET HTML."
            )
            reference_content = f"\n--- REFERENCE HTML STYLE (sample) ---\n{digest}\n----------------------------\n"

        prompt = f"""
You are an expert HTML layout architect. Your task is to reformat the structure and text content of the TARGET HTML extracted from a presentation document.
{reference_instruction}

STRICT LAYOUT & REFORMATTING RULES:

1. IMAGE & TEXT COLUMN LAYOUT RULES:
   - DO NOT automatically force every image into a 2-column side-by-side table.
   - IF AN IMAGE WIDTH IS < 50% OF THE SLIDE WIDTH:
     Format it into a 2-column table row where the image sits on the LEFT cell, and its corresponding caption/text sits on the RIGHT cell.
     Example: <tr><td><img src="..."></td><td>Text/Caption</td></tr>
   - IF AN IMAGE WIDTH IS >= 50% OF THE SLIDE WIDTH (or spans across the slide):
     Format it into a single full-width row or merged row (colspan="2"). Place the image across the full width, with its caption/description text directly UNDERNEATH it across the full width.
     Example: <tr><td colspan="2"><img src="..."><p>Caption Text</p></td></tr>

2. CONTENT & ASSET PRESERVATION:
   - NEVER modify, remove, or translate the 'src' attribute inside any <img> tag (e.g., <img src="figures/image.jpg"> MUST keep its exact original path).
   - Fix broken line breaks, merge split sentences, correct typos, and format headings properly (<h1>, <h2>, <ul>/<li>).

3. TABLE PLACEHOLDERS:
   - The TARGET contains placeholders such as [[TABLE_0]] (each inside its own <p>). They stand for data tables that are restored later.
   - Keep every placeholder EXACTLY as written, exactly once, in the same relative order. Do not wrap, translate, expand or delete them.

4. OUTPUT FORMAT:
   - Return ONLY valid HTML code inside <body>...</body>.
   - Do NOT add any markdown formatting blocks (do NOT use ```html or ```).
   - Do NOT add any commentary or extra explanations.
{reference_content}
--- TARGET HTML TO PROCESS ---
{slim_html}
"""
        try:
            out = _call_llm(prompt, provider, model_name, progress_cb)
            if out:
                out = re.sub(r"^```html\s*", "", out.strip())
                out = re.sub(r"^```\s*", "", out)
                out = re.sub(r"\s*```$", "", out).strip()
                cleaned_html = _restore_tables(out, tables)
        except Exception as e:
            print(f"  [!] Gagal memanggil {provider.upper()} API: {e}")
            print("  [!] Melanjutkan menggunakan HTML asli.")

    if cleaned_html is None:
        cleaned_html = raw_html

    print("  [i] Mengaplikasikan aturan border tabel dan ukuran gambar secara otomatis (Python DOM)...")
    final_html = apply_deterministic_html_styles(cleaned_html)

    clean_html_path = str(Path(html_path).with_name(Path(html_path).stem + "_cleaned.html"))
    with open(clean_html_path, "w", encoding="utf-8") as f:
        f.write(final_html)

    print("  [✔] HTML berhasil dirapikan dan disesuaikan nilainya.")
    return clean_html_path


def convert_html_to_docx(html_file_path, output_docx="Report_Output.docx"):
    if not html_file_path or not os.path.exists(html_file_path):
        print(f"Error: Berkas HTML tidak ditemukan di {html_file_path}")
        return

    print(f"Mengonversi HTML ke Word (.docx) menggunakan Pandoc: {output_docx}...")

    # FIX: let Pandoc find figures/... relative to the HTML file, not the current working dir.
    resource_dir = str(Path(html_file_path).resolve().parent)
    pypandoc.convert_file(
        html_file_path,
        "docx",
        outputfile=output_docx,
        extra_args=[f"--resource-path={resource_dir}"],
    )

    print(f"Selesai! Dokumen Word berhasil disimpan ke: {output_docx}")


BORDER_SZ = 6      # eighths of a point: 6 = 0.75pt = 1 CSS px (use 8 for 1pt)
CELL_MARGIN = 100  # twips, left/right cell padding
_A_NS = "{http://schemas.openxmlformats.org/drawingml/2006/main}"


def _fit_inline(inline, max_emu):
    """Scale a picture down (keeping aspect ratio) so its width <= max_emu."""
    ext = inline.find(qn("wp:extent"))
    cx, cy = int(ext.get("cx")), int(ext.get("cy"))
    if cx <= max_emu or cx == 0:
        return
    ratio = max_emu / cx
    ncx, ncy = int(cx * ratio), int(cy * ratio)
    ext.set("cx", str(ncx))
    ext.set("cy", str(ncy))
    for a_ext in inline.iter(_A_NS + "ext"):
        if a_ext.get("cx") is not None:
            a_ext.set("cx", str(ncx))
            a_ext.set("cy", str(ncy))


def format_docx_tables(docx_path):
    """Pandoc ignores HTML table styling, so fix the DOCX directly with python-docx:
    black borders, full-page width, 2-column tables 50/50, images capped to their cell."""
    doc = Document(docx_path)
    if doc.sections:
        sec = doc.sections[0]
        # Pandoc's default template may not define page size / margins -> use A4 with 1-inch margins
        if sec.page_width is None or sec.page_height is None:
            sec.page_width, sec.page_height = Mm(210), Mm(297)
        for side in ("left_margin", "right_margin", "top_margin", "bottom_margin"):
            if getattr(sec, side) is None:
                setattr(sec, side, Inches(1))
        avail_tw = int((sec.page_width - sec.left_margin - sec.right_margin) / 635)  # EMU -> twips
    else:
        avail_tw = 9026  # A4 text width with 1-inch margins

    for table in doc.tables:
        tbl = table._tbl
        grid = tbl.find(qn("w:tblGrid"))
        cols = grid.findall(qn("w:gridCol")) if grid is not None else []
        n = len(cols)
        if n == 0:
            continue

        # column widths
        if n == 2:
            widths = [avail_tw // 2, avail_tw - avail_tw // 2]
        else:
            old = [int(c.get(qn("w:w"), 0) or 0) for c in cols]
            total = sum(old)
            widths = [round(w * avail_tw / total) for w in old] if total > 0 else [avail_tw // n] * n
        for c, w in zip(cols, widths):
            c.set(qn("w:w"), str(w))

        # table properties (order matters for Word)
        tblPr = tbl.tblPr
        for tag in ("tblW", "jc", "tblCellSpacing", "tblInd", "tblBorders", "shd", "tblLayout", "tblCellMar"):
            for e in tblPr.findall(qn("w:" + tag)):
                tblPr.remove(e)

        new = []
        tblW = OxmlElement("w:tblW")
        tblW.set(qn("w:w"), str(avail_tw))
        tblW.set(qn("w:type"), "dxa")
        new.append(tblW)

        borders = OxmlElement("w:tblBorders")
        for side in ("top", "left", "bottom", "right", "insideH", "insideV"):
            b = OxmlElement("w:" + side)
            b.set(qn("w:val"), "single")
            b.set(qn("w:sz"), str(BORDER_SZ))
            b.set(qn("w:space"), "0")
            b.set(qn("w:color"), "000000")
            borders.append(b)
        new.append(borders)

        layout = OxmlElement("w:tblLayout")
        layout.set(qn("w:type"), "fixed")
        new.append(layout)

        mar = OxmlElement("w:tblCellMar")
        for side in ("top", "left", "bottom", "right"):
            m = OxmlElement("w:" + side)
            m.set(qn("w:w"), str(CELL_MARGIN if side in ("left", "right") else 40))
            m.set(qn("w:type"), "dxa")
            mar.append(m)
        new.append(mar)

        look = tblPr.find(qn("w:tblLook"))
        for e in new:
            if look is not None:
                look.addprevious(e)
            else:
                tblPr.append(e)

        # cell widths + image fitting
        for tr in tbl.findall(qn("w:tr")):
            idx = 0
            for tc in tr.findall(qn("w:tc")):
                tcPr = tc.get_or_add_tcPr()
                span_el = tcPr.find(qn("w:gridSpan"))
                span = int(span_el.get(qn("w:val"))) if span_el is not None else 1
                width = sum(widths[idx: idx + span])
                idx += span

                tcW = tcPr.get_or_add_tcW()
                tcW.set(qn("w:w"), str(width))
                tcW.set(qn("w:type"), "dxa")

                max_emu = max(width - 2 * CELL_MARGIN, 200) * 635
                for inline in tc.iter(qn("wp:inline")):
                    _fit_inline(inline, max_emu)

    # pictures outside tables: cap to the text width
    for inline in doc.element.body.iter(qn("wp:inline")):
        if not inline.xpath("ancestor::w:tc"):
            _fit_inline(inline, avail_tw * 635)

    doc.save(docx_path)
    print("  [✔] Border tabel, lebar kolom 50/50, dan ukuran gambar sudah diterapkan pada DOCX.")


if __name__ == "__main__":
    check_cuda_availability()

    source_pptx = "test.pptx"
    output_folder = "./output"
    reference_html = "example.html"

    VIA_PDF = False                       # True: PPTX -> PDF (LibreOffice) -> Docling
    USE_LLM = True                        # False: skip the LLM, Python rules only
    SELECTED_PROVIDER = "bedrock"         # "ollama" or "bedrock"
    SELECTED_MODEL = DEFAULT_BEDROCK_MODEL  # or "qwen2.5-coder:7b"

    if not os.path.exists(source_pptx):
        print(f"Error: Berkas {source_pptx} tidak ditemukan.")
    else:
        raw_html_path = convert_pptx_to_html_with_docling(source_pptx, output_dir=output_folder, via_pdf=VIA_PDF)
        cleaned_html_path = clean_html_with_llm(
            raw_html_path,
            reference_html_path=reference_html if USE_LLM else None,
            provider=SELECTED_PROVIDER if USE_LLM else "none",
            model_name=SELECTED_MODEL,
        )
        convert_html_to_docx(cleaned_html_path, "Report_Output.docx")
        format_docx_tables("Report_Output.docx")