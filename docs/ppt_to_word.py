import os
import re
import torch
import pypandoc
import ollama
import google.generativeai as genai
from pathlib import Path
from bs4 import BeautifulSoup

from docling.document_converter import DocumentConverter, PowerpointFormatOption
from docling.datamodel.base_models import InputFormat
from docling.datamodel.pipeline_options import PaginatedPipelineOptions
from docling.datamodel.accelerator_options import AcceleratorOptions, AcceleratorDevice
from docling_core.types.doc.document import ImageRefMode

# =================================================================
# MASUKKAN GOOGLE AI STUDIO API KEY ANDA DI SINI (Jika pakai Gemini)
# =================================================================
GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY", "YOUR_API_KEY_HERE")
if GOOGLE_API_KEY != "YOUR_API_KEY_HERE":
    genai.configure(api_key=GOOGLE_API_KEY)
# =================================================================

def check_cuda_availability():
    print("Memeriksa status perangkat keras (CUDA)...")
    if torch.cuda.is_available():
        gpu_name = torch.cuda.get_device_name(0)
        print(f"  [✔] CUDA Aktif! Menggunakan GPU: {gpu_name}")
    else:
        print("  [!] Peringatan: CUDA tidak terdeteksi. Docling berjalan menggunakan CPU.")

def convert_pptx_to_html_with_docling(pptx_path, output_dir="./output"):
    print(f"Memproses {pptx_path} menggunakan Docling PPTX Reader...")
    output_path = Path(output_dir)
    artifacts_dir = output_path / "figures"
    output_path.mkdir(parents=True, exist_ok=True)
    artifacts_dir.mkdir(parents=True, exist_ok=True)
    
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
    
    base_name = os.path.splitext(os.path.basename(pptx_path))[0]
    html_file_path = output_path / f"{base_name}.html"
    
    html_content = doc.export_to_html(
        image_mode=ImageRefMode.REFERENCED,
        image_dir=artifacts_dir
    )
    
    with open(html_file_path, "w", encoding="utf-8") as f:
        f.write(html_content)
        
    print(f"  [+] Berkas HTML & Gambar berhasil dibuat di: {output_dir}")
    return str(html_file_path)

def remove_off_slide_elements(doc):
    """
    Scans the Docling document tree and removes any elements 
    whose bounding box coordinates are entirely outside the slide canvas.
    """
    def filter_node(node):
        if hasattr(node, 'children') and node.children:
            valid_children = []
            
            for child_ref in node.children:
                item = child_ref.resolve(doc) if hasattr(child_ref, "resolve") else child_ref
                is_inside_canvas = True
                
                if hasattr(item, 'prov') and item.prov and len(item.prov) > 0:
                    bbox = item.prov[0].bbox
                    page_no = getattr(bbox, 'page_no', 1)
                    page_info = doc.pages.get(page_no)
                    
                    if page_info and hasattr(page_info, 'size'):
                        slide_w = page_info.size.width
                        slide_h = page_info.size.height
                        
                        x_left = getattr(bbox, 'l', getattr(bbox, 'left', 0))
                        x_right = getattr(bbox, 'r', getattr(bbox, 'right', 0))
                        y_top = getattr(bbox, 't', getattr(bbox, 'top', 0))
                        y_bottom = getattr(bbox, 'b', getattr(bbox, 'bottom', 0))
                        
                        if (x_right <= 0 or x_left >= slide_w or y_bottom <= 0 or y_top >= slide_h):
                            is_inside_canvas = False
                            
                if is_inside_canvas:
                    filter_node(item)
                    valid_children.append(child_ref)
                    
            node.children = valid_children

    if hasattr(doc, 'body'):
        filter_node(doc.body)
        print("  [✔] Off-slide objects have been successfully removed.")

def sanitize_html_for_llm(html_str):
    """Membersihkan tag head, style, dan metadata untuk mempercepat output LLM."""
    html_str = re.sub(r'<style.*?>.*?</style>', '', html_str, flags=re.DOTALL)
    html_str = re.sub(r'<head.*?>.*?</head>', '', html_str, flags=re.DOTALL)
    return html_str.strip()

def apply_deterministic_html_styles(html_str):
    """
    Fungsi Python determinitis untuk memaksa aturan:
    1. Seluruh <img> memiliki style="width: 100%; height: auto;"
    2. Seluruh <table>, <th>, dan <td> memiliki border eksplisit
    """
    soup = BeautifulSoup(html_str, 'html.parser')

    # 1. Paksa seluruh gambar menyesuaikan lebar kolom
    for img in soup.find_all('img'):
        img['style'] = "width: 100%; height: auto;"

    # 2. Paksa seluruh tabel & cell memiliki garis batas (borders)
    for table in soup.find_all('table'):
        table['border'] = "1"
        table['style'] = "border-collapse: collapse; width: 100%; border: 1px solid #000000;"
        
        for cell in table.find_all(['td', 'th']):
            existing_style = cell.get('style', '')
            cell['style'] = f"border: 1px solid #000000; padding: 6px; {existing_style}".strip()

    return str(soup)

def clean_html_with_llm(html_path, reference_html_path=None, provider="gemini", model_name="gemini-2.5-flash"):
    """
    Merapikan tata letak HTML menggunakan LLM.
    Tugas LLM difokuskan penuh pada penataan kolom/layout, perbaikan teks, dan penyelarasan style.
    """
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
            ref_html_text = ref_f.read()
        light_ref_html = sanitize_html_for_llm(ref_html_text)
        reference_instruction = "Analyze the structural style, heading levels, and list formatting of the REFERENCE HTML and apply those styling standards to the TARGET HTML."
        reference_content = f"\n--- REFERENCE HTML STYLE ---\n{light_ref_html}\n----------------------------\n"

    # =================================================================
    # PROMPT TERFOKUS PADA LAYOUT & TEKS (STYLE CSS DITANGANI PYTHON)
    # =================================================================
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

    cleaned_html = ""

    try:
        if provider.lower() == "gemini":
            if GOOGLE_API_KEY == "YOUR_API_KEY_HERE":
                print("  [!] Google API Key belum diisi. Melewati proses perapian LLM.")
                cleaned_html = raw_html
            else:
                model = genai.GenerativeModel(
                    model_name=model_name,
                    generation_config={"temperature": 0.1}
                )
                response = model.generate_content(prompt)
                cleaned_html = response.text
            
        elif provider.lower() == "ollama":
            response = ollama.chat(
                model=model_name, 
                messages=[{'role': 'user', 'content': prompt}],
                options={"temperature": 0.1}
            )
            cleaned_html = response['message']['content']
            
        else:
            print(f"  [!] Provider LLM '{provider}' tidak dikenal. Menggunakan HTML asli.")
            cleaned_html = raw_html

        # Bersihkan sisa fence block markdown jika LLM menyertakannya
        cleaned_html = re.sub(r'^```html\s*', '', cleaned_html.strip())
        cleaned_html = re.sub(r'^```\s*', '', cleaned_html)
        cleaned_html = re.sub(r'\s*```$', '', cleaned_html)
        cleaned_html = cleaned_html.strip()
        
    except Exception as e:
        print(f"  [!] Gagal memanggil {provider.upper()} API: {e}")
        print("  [!] Melanjutkan menggunakan HTML asli.")
        cleaned_html = raw_html

    # =================================================================
    # DITERAPKAN SECARA DETERMINISTIK LEWAT PYTHON (BS4)
    # =================================================================
    print("  [i] Mengaplikasikan aturan border tabel dan ukuran gambar secara otomatis (Python DOM)...")
    final_html = apply_deterministic_html_styles(cleaned_html)

    clean_html_path = html_path.replace(".html", "_cleaned.html")
    with open(clean_html_path, "w", encoding="utf-8") as f:
        f.write(final_html)
        
    print(f"  [✔] HTML berhasil dirapikan dan disesuaikan nilainya.")
    return clean_html_path

def convert_html_to_docx(html_file_path, output_docx="Report_Output.docx"):
    if not html_file_path or not os.path.exists(html_file_path):
        print(f"Error: Berkas HTML tidak ditemukan di {html_file_path}")
        return

    print(f"Mengonversi HTML ke Word (.docx) menggunakan Pandoc: {output_docx}...")
    
    pypandoc.convert_file(
        html_file_path,
        'docx',
        outputfile=output_docx
    )
    
    print(f"Selesai! Dokumen Word berhasil disimpan ke: {output_docx}")

if __name__ == "__main__":
    check_cuda_availability()
    
    source_pptx = "test.pptx"
    output_folder = "./output"
    
    # Path ke file referensi style HTML (jika ada)
    reference_html = "example.html" 
    
    # =================================================================
    # KONFIGURASI LLM CLEANUP
    # =================================================================
    SELECTED_PROVIDER = "gemini"       # Opsi: "ollama" atau "gemini"
    SELECTED_MODEL = "gemini-4-argon" # Opsi: "qwen2.5-coder:7b" atau "gemini-2.5-flash"
    # =================================================================
    
    if not os.path.exists(source_pptx):
        print(f"Error: Berkas {source_pptx} tidak ditemukan.")
    else:
        # Step 1: Langsung PPTX -> HTML & Gambar (Docling)
        raw_html_path = convert_pptx_to_html_with_docling(source_pptx, output_dir=output_folder)
        
        if raw_html_path:
            # Step 2: Restrukturisasi via LLM + Post-process atribut via Python
            cleaned_html_path = clean_html_with_llm(
                raw_html_path, 
                reference_html_path=reference_html,
                provider=SELECTED_PROVIDER, 
                model_name=SELECTED_MODEL
            )
            
            # Step 3: Konversi HTML yang sudah bersih ke DOCX via Pandoc
            convert_html_to_docx(cleaned_html_path, "Report_Output.docx")