"""Halaman review hasil layout engine: render slide asli vs hasil konversi, per slide diberi label.

Data dibaca dari disk (work/<job_id>/build/review.json, ditulis layout_engine.convert_pptx), jadi tetap
bisa direview setelah server restart. Label disimpan ke work/<job_id>/review_labels.json dan nantinya
dipakai untuk memprioritaskan aturan / sebagai data training classifier.

Register di app.py:
    import review
    review.register(app, WORK)
"""
import json
import re
from datetime import datetime
from pathlib import Path

from flask import Blueprint, abort, jsonify, render_template, request, send_from_directory

# Kategori kesalahan yang bisa dipilih reviewer (kode -> label)
VERDICTS = {
    "ok": "OK",
    "order": "Urutan salah",
    "text": "Teks hilang / dobel",
    "diagram_should_text": "Diagram, seharusnya teks",
    "text_should_diagram": "Teks tercecer, seharusnya diagram",
    "table": "Tabel / grid salah",
    "caption": "Caption / gambar salah pasang",
    "heading": "Level heading salah",
    "other": "Lainnya",
}


def register(app, work_dir):
    work = Path(work_dir)
    bp = Blueprint("review", __name__)

    def job_dir(job_id):
        if not re.fullmatch(r"[0-9a-f]{10}", job_id or ""):
            abort(404)
        d = work / job_id
        if not (d / "build" / "review.json").exists():
            abort(404)
        return d

    def load_labels(d):
        p = d / "review_labels.json"
        return json.loads(p.read_text(encoding="utf-8")) if p.exists() else {}

    @bp.get("/review")
    def review_index():
        jobs = []
        for p in sorted(work.glob("*/build/review.json"), key=lambda p: p.stat().st_mtime, reverse=True):
            d = p.parent.parent
            data = json.loads(p.read_text(encoding="utf-8"))
            labels = load_labels(d)
            jobs.append(dict(id=d.name, source=data.get("source", ""), slides=len(data["slides"]),
                             labelled=len(labels), wrong=sum(1 for v in labels.values() if v["verdict"] != "ok"),
                             time=datetime.fromtimestamp(p.stat().st_mtime).strftime("%d %b %Y %H:%M")))
        return render_template("review.html", job=None, jobs=jobs, verdicts=VERDICTS)

    @bp.get("/review/<job_id>")
    def review_job(job_id):
        d = job_dir(job_id)
        data = json.loads((d / "build" / "review.json").read_text(encoding="utf-8"))
        return render_template("review.html", job=dict(id=job_id, **data), jobs=None, verdicts=VERDICTS,
                               labels=load_labels(d))

    @bp.get("/review/<job_id>/slides/<path:name>")
    def review_slide(job_id, name):
        return send_from_directory(job_dir(job_id) / "build" / "slides", name)

    @bp.get("/review/<job_id>/media/<path:name>")
    def review_media(job_id, name):
        return send_from_directory(job_dir(job_id) / "build" / "media", name)

    @bp.post("/api/review/<job_id>/label")
    def save_label(job_id):
        d = job_dir(job_id)
        body = request.get_json(force=True, silent=True) or {}
        n, verdict = body.get("n"), body.get("verdict")
        if not isinstance(n, int) or verdict not in VERDICTS:
            return jsonify(error="n (int) dan verdict yang valid wajib diisi."), 400
        labels = load_labels(d)
        labels[str(n)] = {"verdict": verdict, "note": str(body.get("note", ""))[:1000],
                          "at": datetime.now().isoformat(timespec="seconds")}
        (d / "review_labels.json").write_text(json.dumps(labels, ensure_ascii=False, indent=1), encoding="utf-8")
        return jsonify(ok=True, labelled=len(labels))

    @bp.get("/api/review/<job_id>/labels")
    def get_labels(job_id):
        d = job_dir(job_id)
        data = json.loads((d / "build" / "review.json").read_text(encoding="utf-8"))
        return jsonify(source=data.get("source"), labels=load_labels(d))

    app.register_blueprint(bp)
