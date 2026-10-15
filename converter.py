import os
import re
import torch
import pypandoc
import ollama
from pathlib import Path
from bs4 import BeautifulSoup

# NEW Google SDK (pip install google-genai). The old `google.generativeai` is deprecated.
from google import genai
from google.genai import types as genai_types

from docling.document_converter import DocumentConverter, PowerpointFormatOption
from docling.datamodel.base_models import InputFormat
from docling.datamodel.pipeline_options import PaginatedPipelineOptions
from docling.datamodel.accelerator_options import AcceleratorOptions, AcceleratorDevice
from docling_core.types.doc.document import ImageRefMode

# =================================================================
# GOOGLE AI STUDIO API KEY (only needed for Gemini)
# Set it as an environment variable: GOOGLE_API_KEY or GEMINI_API_KEY
# =================================================================
GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY") or os.environ.get("GEMINI_API_KEY") or ""
_gemini_client = genai.Client(api_key=GOOGLE_API_KEY) if GOOGLE_API_KEY else None


def check_cuda_availability():
    print("Memeriksa status perangkat keras (CUDA)...")
    if torch.cuda.is_available():
        print(f"  [✔] CUDA Aktif! Menggunakan GPU: {torch.cuda.get_device_name(0)}")
    else:
        print("  [!] Peringatan: CUDA tidak terdeteksi. Docling berjalan menggunakan CPU.")


def convert_pptx_to_html_with_docling(pptx_path, output_dir="./output"):
    print(f"Memproses {pptx_path} menggunakan Docling PPTX Reader...")
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    pipeline_options = PaginatedPipelineOptions()
    pipeline_options.generate_picture_images = True
    pipeline_options.images_scale = 2.0
    pipeline_options.accelerator_options = AcceleratorOptions(
        num_threads=4, device=AcceleratorDevice.AUTO
    )

    converter = DocumentConverter(
        format_options={
            InputFormat.PPTX: PowerpointFormatOption(pipeline_options=pipeline_options)
        }
    )

    result = converter.convert(pptx_path)
    doc = result.document

    remove_off_slide_elements(doc)

    base_name = os.path.splitext(os.path.basename(str(pptx_path)))[0]
    html_file_path = output_path / f"{base_name}.html"

    # FIX: export_to_html() has no `image_dir` argument.
    # save_as_html() writes the images to `artifacts_dir` and links them in the HTML.
    # A RELATIVE artifacts_dir is resolved against the HTML file's folder,
    # so the HTML contains src="figures/xxx.png".
    doc.save_as_html(
        filename=html_file_path,
        artifacts_dir=Path("figures"),
        image_mode=ImageRefMode.REFERENCED,
    )

    print(f"  [+] Berkas HTML & Gambar berhasil dibuat di: {output_dir}")
    return str(html_file_path)


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


def apply_deterministic_html_styles(html_str):
    """Force full-width images and explicit table borders (done in Python, not by the LLM)."""
    soup = BeautifulSoup(html_str, "html.parser")

    for img in soup.find_all("img"):
        img["style"] = "width: 100%; height: auto;"

    for table in soup.find_all("table"):
        table["border"] = "1"
        table["style"] = "border-collapse: collapse; width: 100%; border: 1px solid #000000;"
        for cell in table.find_all(["td", "th"]):
            existing_style = cell.get("style", "")
            cell["style"] = f"border: 1px solid #000000; padding: 6px; {existing_style}".strip()

    return str(soup)


def _call_llm(prompt, provider, model_name):
    """Returns the raw LLM text, or None if the provider isn't usable."""
    provider = provider.lower()

    if provider == "gemini":
        if _gemini_client is None:
            print("  [!] GOOGLE_API_KEY belum diisi. Melewati proses perapian LLM.")
            return None
        response = _gemini_client.models.generate_content(
            model=model_name,
            contents=prompt,
            config=genai_types.GenerateContentConfig(temperature=0.1),
        )
        return response.text

    if provider == "ollama":
        response = ollama.chat(
            model=model_name,
            messages=[{"role": "user", "content": prompt}],
            options={"temperature": 0.1},
        )
        return response["message"]["content"]

    print(f"  [!] Provider LLM '{provider}' tidak dikenal. Menggunakan HTML asli.")
    return None


def clean_html_with_llm(html_path, reference_html_path=None, provider="gemini", model_name="gemini-2.5-flash"):
    print(f"Merapikan HTML menggunakan {provider.upper()} (Model: '{model_name}')...")

    if not os.path.exists(html_path):
        print(f"Error: Berkas HTML {html_path} tidak ditemukan.")
        return None

    with open(html_path, "r", encoding="utf-8", errors="ignore") as f:
        raw_html = f.read()

    light_raw_html = sanitize_html_for_llm(raw_html)

    reference_instruction = ""
    reference_content = ""
    if reference_html_path and os.path.exists(reference_html_path):
        print(f"  [i] Menggunakan file referensi: {reference_html_path}")
        with open(reference_html_path, "r", encoding="utf-8", errors="ignore") as ref_f:
            light_ref_html = sanitize_html_for_llm(ref_f.read())
        reference_instruction = (
            "Analyze the structural style, heading levels, and list formatting of the REFERENCE HTML "
            "and apply those styling standards to the TARGET HTML."
        )
        reference_content = f"\n--- REFERENCE HTML STYLE ---\n{light_ref_html}\n----------------------------\n"

    prompt = f"""
You are an expert HTML layout architect. Your task is to reformat the structure and text content of the TARGET HTML extracted from a presentation document.
{reference_instruction}

STRICT LAYOUT & REFORMATTING RULES:

1. IMAGE & TEXT COLUMN LAYOUT RULES:
   - DO NOT automatically force every image into a 2-column side-by-side table.
   - IF AN IMAGE WIDTH IS < 50% OF THE SLIDE WIDTH:
     Format it into a 2-column table row where the image sits on the LEFT cell, and its corresponding caption/text sits on the RIGHT cell.
     Example: <tr><td style="width: 50%;"><img src="..."></td><td style="width: 50%;">Text/Caption</td></tr>
   - IF AN IMAGE WIDTH IS >= 50% OF THE SLIDE WIDTH (or spans across the slide):
     Format it into a single full-width row or merged row (colspan="2"). Place the image across the full width, with its caption/description text directly UNDERNEATH it across the full width.
     Example: <tr><td colspan="2"><img src="..."><p style="text-align: center;">Caption Text</p></td></tr>

2. CONTENT & ASSET PRESERVATION:
   - NEVER modify, remove, or translate the 'src' attribute inside any <img> tag (e.g., <img src="figures/image.jpg"> MUST keep its exact original path).
   - Fix broken line breaks, merge split sentences, correct typos, and format headings properly (<h1>, <h2>, <ul>/<li>).

3. OUTPUT FORMAT:
   - Return ONLY valid HTML code inside <body>...</body>.
   - Do NOT add any markdown formatting blocks (do NOT use ```html or ```).
   - Do NOT add any commentary or extra explanations.

{reference_content}
--- TARGET HTML TO PROCESS ---
{light_raw_html}
"""

    try:
        cleaned_html = _call_llm(prompt, provider, model_name)
        if not cleaned_html:
            cleaned_html = raw_html
        else:
            cleaned_html = re.sub(r"^```html\s*", "", cleaned_html.strip())
            cleaned_html = re.sub(r"^```\s*", "", cleaned_html)
            cleaned_html = re.sub(r"\s*```$", "", cleaned_html).strip()
    except Exception as e:
        print(f"  [!] Gagal memanggil {provider.upper()} API: {e}")
        print("  [!] Melanjutkan menggunakan HTML asli.")
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


if __name__ == "__main__":
    check_cuda_availability()

    source_pptx = "test.pptx"
    output_folder = "./output"
    reference_html = "example.html"
    SELECTED_PROVIDER = "gemini"          # "ollama" or "gemini"
    SELECTED_MODEL = "gemini-2.5-flash"   # or "qwen2.5-coder:7b"

    if not os.path.exists(source_pptx):
        print(f"Error: Berkas {source_pptx} tidak ditemukan.")
    else:
        raw_html_path = convert_pptx_to_html_with_docling(source_pptx, output_dir=output_folder)
        cleaned_html_path = clean_html_with_llm(
            raw_html_path,
            reference_html_path=reference_html,
            provider=SELECTED_PROVIDER,
            model_name=SELECTED_MODEL,
        )
        convert_html_to_docx(cleaned_html_path, "Report_Output.docx")