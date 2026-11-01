"""POC backend untuk halaman "PPT to Word Convert" di frontend new-dwp.

Hanya memakai konversi Full AI: book_engine.convert_book (buku ringkasan, Claude di AWS Bedrock).
AI menyusun bab/bagian dan meringkas tiap slide; angka yang perlu dicek diberi komentar Word dari
"Digital Workplace". Butuh AWS_BEARER_TOKEN_BEDROCK di .env (lihat .env.example).

Jalankan:  .venv/Scripts/python.exe backend/app.py   ->  http://localhost:5003
Frontend new-dwp (mode poc) mem-proxy /poc-api/* ke server ini.

Endpoint (doc_id = id dokumen DWP, mis. "buku-2d"):
  GET  /api/poc/documents/<doc_id>            status dokumen (PPT, konversi Word, PDF final)
  POST /api/poc/documents/<doc_id>/ppt        unggah / ganti PPT (multipart "file"), langsung dikonversi
  GET  /api/poc/documents/<doc_id>/word       unduh DOCX hasil (dengan komentar review)
  POST /api/poc/documents/<doc_id>/final-pdf  unggah PDF final (multipart "file")
  POST /api/poc/documents/<doc_id>/reset      hapus semua (untuk demo ulang)
"""
import json
import os
import re
import shutil
import threading
import time
import traceback
import uuid
from datetime import datetime
from pathlib import Path

from flask import Flask, abort, jsonify, request, send_file
from pptx import Presentation

import slide_reader
import book_engine

HERE = Path(__file__).resolve().parent
WORK = HERE / "work" / "poc"
MAX_PPT_MB = 150
MAX_PDF_MB = 150
SECONDS_PER_SLIDE = 9          # perkiraan awal (mockup: ~18 menit untuk 120 slide)
MODEL = os.environ.get("POC_MODEL") or book_engine.DEFAULT_MODEL

# batas progress book_engine: 0.15 kerangka, 0.25..0.8 isi per slide, 0.8..0.9 cek angka, 0.92 tulis Word
STEPS = [
    ("Reading slides and detecting slide type", 0.15),
    ("AI building the book outline (chapters and sections)", 0.25),
    ("AI processing slide", 0.8),
    ("Checking numbers and adding review comments", 1.01),
]

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = (max(MAX_PPT_MB, MAX_PDF_MB) + 5) * 1024 * 1024
_lock = threading.Lock()
_docs: dict[str, dict] = {}


# ------------------------------------------------------------------ state
def _now():
    return datetime.now().isoformat(timespec="seconds")


def _doc_dir(doc_id):
    if not re.fullmatch(r"[A-Za-z0-9_-]{1,64}", doc_id or ""):
        abort(404)
    return WORK / doc_id


def _empty(doc_id):
    return {"id": doc_id, "ppt": None, "conversion": None, "word": None, "finalPdf": None}


def _load(doc_id):
    with _lock:
        if doc_id not in _docs:
            f = _doc_dir(doc_id) / "state.json"
            doc = json.loads(f.read_text(encoding="utf-8")) if f.exists() else _empty(doc_id)
            conv = doc.get("conversion")
            if conv and conv.get("status") == "converting":
                # server mati di tengah konversi: thread-nya hilang
                conv.update(status="error", error="Konversi terhenti karena server dimulai ulang. Unggah ulang PPT.")
            _docs[doc_id] = doc
        return _docs[doc_id]


def _save(doc):
    d = _doc_dir(doc["id"])
    d.mkdir(parents=True, exist_ok=True)
    tmp = d / "state.json.tmp"
    tmp.write_text(json.dumps(doc, ensure_ascii=False, indent=1), encoding="utf-8")
    tmp.replace(d / "state.json")


def _public(doc):
    """State untuk frontend (tanpa path lokal)."""
    out = {k: v for k, v in doc.items() if k in ("id", "ppt", "conversion", "word", "finalPdf")}
    if out["ppt"]:
        out["ppt"] = {k: v for k, v in out["ppt"].items() if k != "path"}
    if out["word"]:
        out["word"] = {k: v for k, v in out["word"].items() if k != "path"}
    if out["finalPdf"]:
        out["finalPdf"] = {k: v for k, v in out["finalPdf"].items() if k != "path"}
    conv = out["conversion"]
    if conv and conv["status"] == "converting":
        conv = dict(conv)
        elapsed = time.time() - conv["startedTs"]
        frac = conv["progress"]
        if frac > 0.05:
            conv["etaSeconds"] = max(0, round(elapsed / frac - elapsed))
        else:
            conv["etaSeconds"] = max(0, conv["estimateSeconds"] - round(elapsed))
        out["conversion"] = conv
    if doc["finalPdf"]:
        out["status"] = "done"
    elif doc["ppt"]:
        out["status"] = "in_progress"
    else:
        out["status"] = "not_started"
    return out


# ------------------------------------------------------------------ conversion
def _run(doc_id, run_id, pptx: Path, out_dir: Path, total: int):
    doc = _load(doc_id)

    def current():
        return doc["conversion"] and doc["conversion"]["runId"] == run_id

    def progress(fraction, message):
        if not current():
            return
        conv = doc["conversion"]
        step = next(i for i, (_t, end) in enumerate(STEPS) if fraction < end)
        m = re.search(r"AI: slide \d+ selesai \((\d+)/(\d+)\)", message)
        if m:
            conv["ai"] = {"done": int(m.group(1)), "total": int(m.group(2))}
        else:
            m = re.search(r"AI menulis isi (\d+) slide", message)
            if m:
                conv["ai"] = {"done": 0, "total": int(m.group(1))}
        conv["progress"] = round(fraction, 3)
        conv["currentSlide"] = min(total, round(total * fraction))
        conv["message"] = message
        for i, st in enumerate(conv["steps"]):
            st["state"] = "done" if i < step else ("running" if i == step else "waiting")

    try:
        docx = out_dir / (pptx.stem + " - Buku.docx")
        stats = book_engine.convert_book(pptx, docx, model=MODEL, work_dir=out_dir / "build",
                                         progress=progress, comments=True)
        if not current():
            return
        conv = doc["conversion"]
        conv.update(status="complete", progress=1.0, currentSlide=total, finishedAt=_now(),
                    stats={k: stats[k] for k in ("title", "slides", "chapters", "slides_used", "llm_calls",
                                                  "cache_hits", "fallback", "comments", "numbers", "rendered",
                                                  "seconds", "check")})
        for st in conv["steps"]:
            st["state"] = "done"
        doc["word"] = {"name": docx.name, "size": docx.stat().st_size, "comments": stats["comments"],
                       "author": "Digital Workplace", "createdAt": _now(), "path": str(docx)}
    except Exception as e:
        traceback.print_exc()
        if current():
            doc["conversion"].update(status="error", error=str(e) or e.__class__.__name__)
    finally:
        if current():
            with _lock:
                _save(doc)


# ------------------------------------------------------------------ routes
@app.get("/api/poc/documents/<doc_id>")
def get_doc(doc_id):
    return jsonify(_public(_load(doc_id)))


def _too_large(limit_mb):
    return request.content_length and request.content_length > limit_mb * 1024 * 1024


@app.post("/api/poc/documents/<doc_id>/ppt")
def upload_ppt(doc_id):
    doc = _load(doc_id)
    if _too_large(MAX_PPT_MB):
        return jsonify(code="TOO_LARGE", message=f"File lebih dari {MAX_PPT_MB}MB."), 413
    f = request.files.get("file")
    if not f or not f.filename:
        return jsonify(code="NO_FILE", message="Pilih file .pptx."), 400
    if not f.filename.lower().endswith(".pptx"):
        return jsonify(code="INVALID_TYPE", message="Hanya file .pptx yang bisa diunggah."), 400

    run_id = uuid.uuid4().hex[:10]
    run_dir = _doc_dir(doc_id) / run_id
    run_dir.mkdir(parents=True)
    safe = re.sub(r"[^\w\-. ]+", "_", Path(f.filename).name).strip() or "presentation.pptx"
    dest = run_dir / safe
    f.save(dest)
    size = dest.stat().st_size
    if size > MAX_PPT_MB * 1024 * 1024:
        shutil.rmtree(run_dir, ignore_errors=True)
        return jsonify(code="TOO_LARGE", message=f"File lebih dari {MAX_PPT_MB}MB."), 413
    try:
        prs = Presentation(str(dest))
    except Exception as e:
        shutil.rmtree(run_dir, ignore_errors=True)
        return jsonify(code="INVALID_TYPE", message=f"PPTX tidak dapat dibaca: {e}"), 400
    slides = len(prs.slides)
    visible = sum(1 for s in prs.slides if not slide_reader.is_hidden(s))
    if not visible:
        shutil.rmtree(run_dir, ignore_errors=True)
        return jsonify(code="EMPTY", message="PPTX tidak memiliki slide."), 400

    old_runs = [p for p in _doc_dir(doc_id).iterdir() if p.is_dir() and p.name != run_id]
    with _lock:
        doc.update(
            ppt={"name": Path(f.filename).name, "size": size, "slides": slides, "visibleSlides": visible,
                 "uploadedBy": request.form.get("uploadedBy") or "Unknown", "uploadedAt": _now(),
                 "path": str(dest)},
            conversion={"runId": run_id, "status": "converting", "progress": 0.0, "currentSlide": 0,
                        "totalSlides": visible, "message": "", "ai": None, "engine": "book", "model": MODEL,
                        "estimateSeconds": visible * SECONDS_PER_SLIDE, "startedAt": _now(),
                        "startedTs": time.time(), "steps": [{"label": t, "state": "waiting"} for t, _end in STEPS],
                        "error": None},
            word=None, finalPdf=None)
        _save(doc)
    threading.Thread(target=_run, args=(doc_id, run_id, dest, run_dir, visible), daemon=True).start()
    for p in old_runs:                       # PPT lama tidak disimpan (lihat modal Replace PPT)
        shutil.rmtree(p, ignore_errors=True)
    return jsonify(_public(doc))


@app.get("/api/poc/documents/<doc_id>/word")
def download_word(doc_id):
    doc = _load(doc_id)
    if not doc["word"] or not Path(doc["word"]["path"]).exists():
        return jsonify(code="NOT_READY", message="File Word belum tersedia."), 404
    return send_file(doc["word"]["path"], as_attachment=True, download_name=doc["word"]["name"])


@app.post("/api/poc/documents/<doc_id>/final-pdf")
def upload_final_pdf(doc_id):
    doc = _load(doc_id)
    if not doc["word"]:
        return jsonify(code="NOT_READY", message="Konversi Word belum selesai."), 409
    if _too_large(MAX_PDF_MB):
        return jsonify(code="TOO_LARGE", message=f"File lebih dari {MAX_PDF_MB}MB."), 413
    f = request.files.get("file")
    if not f or not f.filename.lower().endswith(".pdf"):
        return jsonify(code="INVALID_TYPE", message="Hanya file .pdf yang bisa diunggah."), 400
    dest = _doc_dir(doc_id) / doc["conversion"]["runId"] / ("final_" + re.sub(r"[^\w\-. ]+", "_", Path(f.filename).name))
    f.save(dest)
    with _lock:
        doc["finalPdf"] = {"name": Path(f.filename).name, "size": dest.stat().st_size,
                           "uploadedBy": request.form.get("uploadedBy") or "Unknown", "uploadedAt": _now(),
                           "path": str(dest)}
        _save(doc)
    return jsonify(_public(doc))


@app.post("/api/poc/documents/<doc_id>/reset")
def reset(doc_id):
    d = _doc_dir(doc_id)
    with _lock:
        _docs[doc_id] = _empty(doc_id)
    shutil.rmtree(d, ignore_errors=True)
    return jsonify(_public(_load(doc_id)))


@app.errorhandler(413)
def too_large(_e):
    return jsonify(code="TOO_LARGE", message=f"File lebih dari {MAX_PPT_MB}MB."), 413


if __name__ == "__main__":
    WORK.mkdir(parents=True, exist_ok=True)
    if not os.environ.get("AWS_BEARER_TOKEN_BEDROCK"):
        print("  [!] AWS_BEARER_TOKEN_BEDROCK belum diisi (.env): konversi akan gagal.")
    print(f"POC API: Full AI book_engine, model={MODEL}  ->  http://localhost:5003")
    app.run(port=5003, threaded=True)
