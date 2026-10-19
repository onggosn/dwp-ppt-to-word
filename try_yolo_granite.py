"""Eksperimen: hasil out-of-the-box DocLayout-YOLO dan Granite-Docling untuk PPTX (tanpa aturan layout).

    python try_yolo_granite.py docs/test.pptx

Alur:
  1. PPTX -> PDF + PNG per slide lewat PowerPoint (kedua model bekerja di atas gambar halaman).
  2. DocLayout-YOLO (DocStructBench): deteksi kotak layout per slide -> gambar beranotasi + JSON.
  3. Granite-Docling (granite-docling-258M, VlmPipeline Docling): PDF -> DoclingDocument -> HTML -> DOCX (Pandoc).

Hasil: work/experiments/<nama file>/{slides, yolo, granite}
"""
import json
import shutil
import subprocess
import sys
import time
from pathlib import Path

PS_EXPORT = r"""
$ErrorActionPreference = 'Stop'
$app = New-Object -ComObject PowerPoint.Application
$pres = $app.Presentations.Open('{src}', $true, $false, $false)
try {
  $pres.SaveAs('{pdf}', 32)   # 32 = ppSaveAsPDF
  foreach ($s in $pres.Slides) { $s.Export(('{png}\slide' + $s.SlideIndex + '.png'), 'PNG', 2000, 1125) }
} finally { $pres.Close(); if ($app.Presentations.Count -eq 0) { $app.Quit() } }
"""


def export_with_powerpoint(pptx: Path, out: Path) -> Path:
    """PPTX -> out/<nama>.pdf dan out/slides/slideN.png."""
    pdf, png_dir = out / f"{pptx.stem}.pdf", out / "slides"
    png_dir.mkdir(parents=True, exist_ok=True)
    q = lambda p: str(p.resolve()).replace("'", "''")
    script = PS_EXPORT.replace("{src}", q(pptx)).replace("{pdf}", q(pdf)).replace("{png}", q(png_dir))
    subprocess.run(["powershell", "-NoProfile", "-NonInteractive", "-Command", script],
                   check=True, capture_output=True, timeout=900)
    return pdf


def run_yolo(png_dir: Path, out: Path) -> None:
    """DocLayout-YOLO out of the box: kotak + label kelas + skor per slide."""
    from ultralytics import YOLO
    from huggingface_hub import hf_hub_download

    # weights = hf_hub_download("juliozhao/DocLayout-YOLO-DocStructBench", "doclayout_yolo_docstructbench_imgsz1024.pt")
    weights = str('runs/detect/train-2/weights/best.pt')
    model = YOLO(weights)
    out.mkdir(parents=True, exist_ok=True)
    summary = {}
    for img in sorted(png_dir.glob("slide*.png"), key=lambda p: int(p.stem[5:])):
        res = model.predict(str(img), imgsz=1024, conf=0.2, device="cuda:0" if _cuda() else "cpu", verbose=False)[0]
        res.save(str(out / f"{img.stem}_yolo.jpg"))           # gambar beranotasi bawaan library
        boxes = [{"label": res.names[int(c)], "conf": round(float(s), 3),
                  "xyxy": [round(float(v), 1) for v in xyxy]}
                 for xyxy, c, s in zip(res.boxes.xyxy, res.boxes.cls, res.boxes.conf)]
        summary[img.stem] = boxes
        print(f"  YOLO {img.stem}: {len(boxes)} kotak")
    (out / "boxes.json").write_text(json.dumps(summary, indent=1), encoding="utf-8")


def run_granite(pdf: Path, out: Path) -> None:
    """Granite-Docling out of the box: PDF -> DoclingDocument -> HTML (gambar disematkan) -> DOCX."""
    import pypandoc
    from docling.datamodel import vlm_model_specs
    from docling.datamodel.base_models import InputFormat
    from docling.datamodel.pipeline_options import VlmPipelineOptions
    from docling.document_converter import DocumentConverter, PdfFormatOption
    from docling.pipeline.vlm_pipeline import VlmPipeline
    from docling_core.types.doc.document import ImageRefMode

    opts = VlmPipelineOptions(vlm_options=vlm_model_specs.GRANITEDOCLING_TRANSFORMERS,
                              generate_page_images=True, generate_picture_images=True)
    converter = DocumentConverter(format_options={
        InputFormat.PDF: PdfFormatOption(pipeline_cls=VlmPipeline, pipeline_options=opts)})
    out.mkdir(parents=True, exist_ok=True)
    doc = converter.convert(str(pdf)).document
    html = out / f"{pdf.stem}.html"
    doc.save_as_html(html, image_mode=ImageRefMode.EMBEDDED)
    pypandoc.convert_file(str(html), "docx", outputfile=str(out / f"{pdf.stem}.docx"))
    print(f"  Granite: {html.name} + {pdf.stem}.docx")


def _cuda() -> bool:
    import torch
    return torch.cuda.is_available()


if __name__ == "__main__":
    pptx = Path(sys.argv[1] if len(sys.argv) > 1 else "docs/test.pptx")
    out = Path("work/experiments") / pptx.stem
    shutil.rmtree(out, ignore_errors=True)
    t = time.time()
    pdf = export_with_powerpoint(pptx, out)
    print(f"[1/3] PowerPoint -> PDF + PNG: {time.time() - t:.0f}s")
    t = time.time()
    run_yolo(out / "slides", out / "yolo")
    print(f"[2/3] DocLayout-YOLO: {time.time() - t:.0f}s")
    # t = time.time()
    # run_granite(pdf, out / "granite")
    # print(f"[3/3] Granite-Docling: {time.time() - t:.0f}s")
    # print(f"Hasil: {out}")
