import json
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
from pptx import Presentation

# Mengimpor fungsionalitas dari layout_engine milikmu
from layout_engine import render_slides, analyse, Box

def flatten_boxes(info: dict) -> list:
    """
    Mengurai dictionary hasil analyse() menjadi satu list Box yang datar.
    """
    boxes = []
    
    if info.get("title"):
        boxes.append(info["title"])
        
    for b in info.get("subheads", []):
        boxes.append(b)
        
    for head, col in info.get("columns", []):
        if head: boxes.append(head)
        if col: boxes.append(col)
        
    for head, items in info.get("panels", []):
        if head: boxes.append(head)
        boxes.extend(items)
        
    for b in info.get("bodies", []):
        boxes.append(b)
        
    for pic, cap in info.get("figures", []):
        if pic: boxes.append(pic)
        if cap: boxes.append(cap)
        
    for b in info.get("tables", []):
        boxes.append(b)
        
    for b in info.get("notes", []):
        boxes.append(b)
        
    # Menghapus duplikat objek (karena referensi id() yang sama mungkin muncul lebih dari sekali)
    valid_boxes = []
    seen = set()
    for b in boxes:
        if b and id(b) not in seen:
            valid_boxes.append(b)
            seen.add(id(b))
            
    return valid_boxes

def prepare_dataset(pptx_path: str, output_dir: str):
    pptx_path = Path(pptx_path)
    out_dir = Path(output_dir)
    img_dir = out_dir / "images"
    annotated_dir = out_dir / "annotated"
    
    # Buat direktori jika belum ada
    annotated_dir.mkdir(parents=True, exist_ok=True)
    img_dir.mkdir(parents=True, exist_ok=True)

    print("1. Merender slides ke PNG menggunakan PowerPoint COM...")
    # Menggunakan PowerShell export asli dari layout_engine
    render_slides(pptx_path, img_dir)

    print("2. Mengekstrak Layout dan Menggambar Bounding Box...")
    prs = Presentation(pptx_path)
    W, H = prs.slide_width, prs.slide_height

    dataset_mapping = {}

    # Siapkan Font tebal untuk angka (gunakan arial.ttf jika ada, atau default)
    try:
        font = ImageFont.truetype("arial.ttf", 36)
    except IOError:
        font = ImageFont.load_default()

    for n, slide in enumerate(prs.slides, 1):
        img_path = img_dir / f"slide{n}.png"
        if not img_path.exists():
            continue
        
        # Panggil analitik dari layout_engine.py
        info = analyse(slide, W, H)
        boxes = flatten_boxes(info)

        # Buka gambar hasil render PowerShell
        img = Image.open(img_path).convert("RGB")
        draw = ImageDraw.Draw(img)
        img_w, img_h = img.size

        slide_data = {"boxes": {}}

        for idx, b in enumerate(boxes, 1):
            # Proyeksikan kordinat fraksi (0.0 - 1.0) ke pixel absolut gambar PNG
            x0, y0 = int(b.x * img_w), int(b.y * img_h)
            x1, y1 = int(b.r * img_w), int(b.b * img_h)
            
            # Gambar kotak merah yang tebal
            draw.rectangle([x0, y0, x1, y1], outline="red", width=5)
            
            # Gambar lencana kotak angka
            label = f"[{idx}]"
            
            # Menghitung ukuran teks untuk background nomor
            try:
                text_bbox = draw.textbbox((x0, y0), label, font=font)
                draw.rectangle(text_bbox, fill="red")
            except AttributeError: # Fallback untuk Pillow versi lama
                draw.rectangle([x0, y0, x0+40, y0+30], fill="red")
                
            draw.text((x0, y0), label, fill="white", font=font)

            # Simpan metadata (format YOLO: x_center, y_center, width, height dalam persentase)
            slide_data["boxes"][str(idx)] = {
                "yolo_box": [
                    round(b.x + (b.w / 2), 5), # x_center
                    round(b.y + (b.h / 2), 5), # y_center
                    round(b.w, 5),             # width
                    round(b.h, 5)              # height
                ]
            }

        # Simpan gambar yang sudah ditandai merah
        annotated_img_path = annotated_dir / f"slide{n}_annotated.jpg"
        img.save(annotated_img_path, quality=90)
        
        dataset_mapping[f"slide{n}"] = slide_data
        print(f"  -> Slide {n} diproses ({len(boxes)} kotak terdeteksi).")

    # Simpan file pemetaan ke JSON
    with open(out_dir / "boxes_mapping.json", "w", encoding="utf-8") as f:
        json.dump(dataset_mapping, f, indent=2)
    
    print(f"\nSelesai! Silakan cek folder '{output_dir}'.")
    print("Gunakan gambar di sub-folder 'annotated' untuk di-prompt ke Gemini AI.")

if __name__ == "__main__":
    # Ganti 'docs/test.pptx' dengan path file presentasimu
    prepare_dataset("docs/test - Copy.pptx", "work/dataset_prep2")