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

app = Flask(__name__)
WORK = Path("work")
WORK.mkdir(exist_ok=True)
JOBS: dict[str, dict] = {}


def run_job(job_id, pptx: Path, ref, provider, model):
    job = JOBS[job_id]
    try:
        out_dir = WORK / job_id / "output"
        job.update(status="running", step=0)
        raw_html = c.convert_pptx_to_html_with_docling(str(pptx), output_dir=str(out_dir))

        job["step"] = 1
        cleaned = c.clean_html_with_llm(
            raw_html, reference_html_path=ref, provider=provider, model_name=model
        )

        job["step"] = 2
        docx_path = WORK / job_id / f"{pptx.stem}.docx"
        c.convert_html_to_docx(cleaned, str(docx_path))

        job.update(status="done", step=3, file=str(docx_path), name=docx_path.name)
    except Exception as e:  # surface error in UI
        traceback.print_exc()
        job.update(status="error", error=str(e))


@app.get("/")
def index():
    return render_template("index.html")


@app.post("/api/convert")
def convert():
    f = request.files.get("pptx")
    if not f or not f.filename.lower().endswith(".pptx"):
        return jsonify(error="Please upload a .pptx file."), 400

    job_id = uuid.uuid4().hex[:10]
    job_dir = WORK / job_id
    job_dir.mkdir(parents=True)
    pptx = job_dir / Path(f.filename).name
    f.save(pptx)

    r = request.files.get("reference")
    if not r or not r.filename.lower().endswith((".html", ".htm")):
        return jsonify(error="Please upload a reference .html file."), 400
    ref = str(job_dir / "reference.html")
    r.save(ref)

    provider = request.form.get("provider", "gemini")
    model = request.form.get("model") or "gemini-2.5-flash"

    JOBS[job_id] = dict(id=job_id, status="queued", step=0, source=f.filename)
    threading.Thread(target=run_job, args=(job_id, pptx, ref, provider, model), daemon=True).start()
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


if __name__ == "__main__":
    app.run(debug=False, threaded=True, port=5000)