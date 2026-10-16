"""Demo web app wrapping the PPTX -> HTML -> LLM cleanup -> DOCX pipeline.

Save your original script next to this file as `converter.py` (unchanged).
Run:  pip install flask  &&  python app.py   ->  http://localhost:5000
"""
import threading
import traceback
import uuid
from pathlib import Path

from flask import Flask, jsonify, render_template, request, send_file

import converter as c  # your original code
import ckeditor_flow  # PPT -> CKEditor (seamless editing)
import layout_engine  # PPTX -> DOCX/HTML dari geometri slide (tanpa LLM)

app = Flask(__name__)
WORK = Path("work")
WORK.mkdir(exist_ok=True)
JOBS: dict[str, dict] = {}
ckeditor_flow.register(app, WORK)  # /api/ck/*


def run_job(job_id, pptx: Path, ref, provider, model, use_llm):
    job = JOBS[job_id]
    try:
        out_dir = WORK / job_id / "output"
        job["status"] = "running"
        step = iter(range(len(job["steps"])))

        # converter.py picks the PPTX or PDF Docling pipeline from the file extension
        job["step"] = next(step)
        raw_html = c.convert_document_to_html_with_docling(str(pptx), output_dir=str(out_dir))

        job["step"] = next(step)
        cleaned = c.clean_html_with_llm(
            raw_html,
            reference_html_path=ref if use_llm else None,
            provider=provider if use_llm else "none",
            model_name=model,
            progress_cb=lambda n: job.__setitem__("llm_chars", n),
        )

        job["step"] = next(step)
        docx_path = WORK / job_id / f"{pptx.stem}.docx"
        c.convert_html_to_docx(cleaned, str(docx_path))

        job["step"] = next(step)
        c.format_docx_tables(str(docx_path))

        job.update(status="done", step=len(job["steps"]), file=str(docx_path), name=docx_path.name)
    except Exception as e:  # surface error in UI
        traceback.print_exc()
        job.update(status="error", error=str(e))


def run_layout_job(job_id, pptx: Path, provider, model, use_llm, include_hidden=False):
    """Layout engine: render (PowerPoint) -> analisa geometri -> [LLM rapikan teks] -> DOCX + HTML."""
    job = JOBS[job_id]
    # batas progress (lihat layout_engine.convert_pptx) -> indeks langkah di UI
    bounds = [0.35, 0.45] + ([0.85] if use_llm else []) + [1.01]

    def on_progress(fraction, _message):
        job["step"] = next(i for i, b in enumerate(bounds) if fraction < b)

    try:
        job["status"] = "running"
        docx_path = WORK / job_id / f"{pptx.stem}.docx"
        html_path = WORK / job_id / f"{pptx.stem}.html"
        stats = layout_engine.convert_pptx(
            pptx, docx_path, html_path,
            use_llm=use_llm, provider=provider, model=model,
            work_dir=WORK / job_id / "build", progress=on_progress, include_hidden=include_hidden,
        )
        job.update(status="done", step=len(job["steps"]), file=str(docx_path), name=docx_path.name,
                   html=str(html_path), stats=stats)
    except Exception as e:
        traceback.print_exc()
        job.update(status="error", error=str(e))


@app.get("/")
def index():
    return render_template("index.html")


@app.get("/dwp")
def index_dwp():
    # tampilan bergaya DWP: konversi PPT/PDF ke Word + editor PPT/CKEditor
    return render_template("index_dwp.html")


@app.post("/api/convert")
def convert():
    f = request.files.get("pptx")
    if not f or not f.filename.lower().endswith((".pptx", ".pdf")):
        return jsonify(error="Please upload a .pptx or .pdf file."), 400

    job_id = uuid.uuid4().hex[:10]
    job_dir = WORK / job_id
    job_dir.mkdir(parents=True)
    pptx = job_dir / Path(f.filename).name
    f.save(pptx)

    is_pdf = f.filename.lower().endswith(".pdf")
    use_llm = request.form.get("use_llm", "true") == "true"
    provider = request.form.get("provider", "gemini")
    model = request.form.get("model") or "gemini-3.8-flash"

    # layout engine hanya untuk PPTX; PDF tetap lewat Docling
    if request.form.get("engine", "layout") == "layout" and not is_pdf:
        steps = ["Render slides with PowerPoint", "Analyse slide layout (no LLM)"]
        if use_llm:
            steps.append("Tidy text with LLM")
        steps.append("Write Word document and CKEditor HTML")
        JOBS[job_id] = dict(id=job_id, status="queued", step=0, source=f.filename, steps=steps,
                            llm_step=-1, llm_chars=0, engine="layout")
        include_hidden = request.form.get("include_hidden", "false") == "true"
        threading.Thread(target=run_layout_job, args=(job_id, pptx, provider, model, use_llm, include_hidden),
                         daemon=True).start()
        return jsonify(id=job_id)

    ref = None
    if use_llm:
        r = request.files.get("reference")
        if not r or not r.filename.lower().endswith((".html", ".htm")):
            return jsonify(error="Please upload a reference .html file."), 400
        ref = str(job_dir / "reference.html")
        r.save(ref)

    steps = []
    steps.append("Read the PDF with Docling" if is_pdf else "Read the PPTX with Docling")
    steps.append("Restructure layout with LLM" if use_llm else "Clean HTML with Python (no LLM)")
    steps.append("Build Word document with Pandoc")
    steps.append("Apply table borders, 50/50 columns and image sizes")

    JOBS[job_id] = dict(
        id=job_id, status="queued", step=0, source=f.filename, steps=steps,
        llm_step=1 if use_llm else -1, llm_chars=0,
    )
    threading.Thread(
        target=run_job, args=(job_id, pptx, ref, provider, model, use_llm), daemon=True
    ).start()
    return jsonify(id=job_id)


@app.get("/api/status/<job_id>")
def status(job_id):
    job = JOBS.get(job_id)
    return (jsonify(job) if job else (jsonify(error="Job not found"), 404))


@app.get("/api/history")
def history():
    return jsonify([j for j in reversed(JOBS.values())])


@app.get("/download/<job_id>")
def download(job_id):
    job = JOBS.get(job_id)
    if not job or job.get("status") != "done":
        return "Not ready", 404
    return send_file(job["file"], as_attachment=True, download_name=job["name"])


@app.get("/download/<job_id>/html")
def download_html(job_id):
    """HTML mandiri (gambar base64) untuk ditempel/dimuat di CKEditor."""
    job = JOBS.get(job_id)
    if not job or job.get("status") != "done" or not job.get("html"):
        return "Not ready", 404
    return send_file(job["html"], as_attachment=True, download_name=Path(job["html"]).name)


if __name__ == "__main__":
    app.run(debug=False, threaded=True, port=5001)