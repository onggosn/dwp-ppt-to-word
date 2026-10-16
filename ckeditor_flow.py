"""PPT -> CKEditor flow (seamless editing), backend for templates/index_dwp.html.

Independent of converter.py (no Docling / LLM needed). It:
  1. reads the slides of the document .pptx (mock OneDrive: work/onedrive, generated from docs/test.pptx)
     with layout_engine (slide geometry -> headings, lists, picture+caption tables, data tables),
     renders the slides with PowerPoint and crops every picture from the render,
  2. maps every slide to a sub-section (leaf of the section tree, like Mapping Section PPT in DWP),
  3. builds CKEditor-ready HTML grouped by section, in one run, with real progress.

Register in app.py:
    import ckeditor_flow
    ckeditor_flow.register(app, WORK)

Section tree: sections.json next to this file (list of {"code": "1.2.1", "title": "..."}).
Slide -> section mapping order:
    1. tag      a shape name / alt text / speaker note containing  SEC:1.2.1  or  [[1.2.1]]
    2. judul    slide title equals a leaf section title (exact, ignoring case/punctuation)
    3. lanjutan same section as the previous slide
    4. default  first leaf section
A tag that points to a parent section is moved to the first leaf under it.
"""
import dataclasses
import html
import json
import os
import re
import shutil
import threading
import time
import uuid
from pathlib import Path

from flask import Blueprint, abort, jsonify, request, send_from_directory
from pptx import Presentation
from pptx.enum.shapes import MSO_SHAPE_TYPE

import layout_engine

HERE = Path(__file__).resolve().parent
MOCK_TEMPLATE = HERE / "docs" / "test.pptx"  # sementara: pengganti PPT template section di OneDrive
MOCK_NAME = "DWP_Buku_3a.pptx"
STEP_DELAY = float(os.environ.get("DWP_CK_STEP_DELAY", "0.08"))  # seconds per slide per phase (visible progress)

DEFAULT_SECTIONS = [
    {"code": "1", "title": "Bab 1 Pendahuluan"},
    {"code": "1.1", "title": "Tujuan"},
    {"code": "1.2", "title": "Latar Belakang"},
    {"code": "1.2.1", "title": "Kondisi Ekonomi"},
    {"code": "1.2.2", "title": "Inflasi"},
    {"code": "2", "title": "Bab 2 Kebijakan"},
    {"code": "2.1", "title": "Bauran Kebijakan"},
    {"code": "2.2", "title": "Rekomendasi"},
    {"code": "3", "title": "Bab 3 Penutup"},
    {"code": "3.1", "title": "Kesimpulan"},
    {"code": "3.2", "title": "Tindak Lanjut"},
]

TAG_RE = re.compile(r"(?:\bSEC[:=_\-\s]*|\[\[)\s*(\d+(?:\.\d+)*)\s*(?:\]\])?", re.IGNORECASE)
STEPS = ["Membaca slide PPT", "Memetakan slide ke section Predefine", "Membuat konten CKEditor"]
WEIGHTS = (0.3, 0.4, 0.3)


# ------------------------------------------------------------------ sections
def load_sections(raw=None):
    """Returns [{code,title,level,leaf}] in tree order. raw: list of {code,title} or None."""
    if raw is None:
        p = HERE / "sections.json"
        raw = json.loads(p.read_text(encoding="utf-8")) if p.exists() else DEFAULT_SECTIONS
    out = []
    codes = [str(n["code"]) for n in raw]
    for n in raw:
        code = str(n["code"])
        out.append({
            "code": code,
            "title": str(n["title"]),
            "level": code.count("."),
            "leaf": not any(c.startswith(code + ".") for c in codes),
        })
    if not any(n["leaf"] for n in out):
        raise ValueError("Struktur section tidak memiliki sub-section.")
    return out


def _norm(s):
    return re.sub(r"[^a-z0-9]+", " ", s.lower()).strip()


def _first_leaf(toc, code):
    for n in toc:
        if n["leaf"] and (n["code"] == code or n["code"].startswith(code + ".")):
            return n["code"]
    return None


def map_slide(slide, toc, prev_code):
    """Returns (code, method)."""
    for text in slide["tags_text"]:
        m = TAG_RE.search(text)
        if m:
            leaf = _first_leaf(toc, m.group(1))
            if leaf:
                return leaf, "tag"
    title = _norm(slide["title"])
    if title:
        leaves = [n for n in toc if n["leaf"]]
        for n in leaves:
            if _norm(n["title"]) == title:
                return n["code"], "judul"
    if prev_code:
        return prev_code, "lanjutan"
    return next(n["code"] for n in toc if n["leaf"]), "default"


# ------------------------------------------------------------------ pptx reading
def _alt_text(shape):
    try:
        return shape._element.xpath(".//p:cNvPr/@descr")[0]
    except Exception:
        return ""


def _walk(shapes):
    for sh in shapes:
        yield sh
        if sh.shape_type == MSO_SHAPE_TYPE.GROUP:
            yield from _walk(sh.shapes)


def _text(runs):
    """Teks polos dengan normalisasi spasi yang sama seperti di HTML/DOCX."""
    return "".join(r[0] for r in layout_engine._strip_runs(runs))


def extract_slides(pptx_path, media_dir):
    """Analisa layout tiap slide (cepat, tanpa render). Gambar baru dibuat oleh render_media();
    sampai saat itu tiap baris gambar menunjuk ke path tujuan dan box-nya disimpan di slide["pending"]."""
    prs = Presentation(str(pptx_path))
    W, H = prs.slide_width, prs.slide_height
    media_dir = Path(media_dir)
    slides = []
    for n, sl in enumerate(prs.slides, 1):
        if layout_engine.is_hidden(sl):
            continue      # slide yang di-hide di PowerPoint tidak masuk dokumen
        tags_text = []
        for sh in _walk(sl.shapes):
            tags_text += [sh.name or "", _alt_text(sh)]
        if sl.has_notes_slide and sl.notes_slide.notes_text_frame is not None:
            tags_text.append(sl.notes_slide.notes_text_frame.text or "")

        info = layout_engine.analyse(sl, W, H)
        pending, counter = {}, {"n": 0}

        def defer(box, _n=n, _pending=pending, _c=counter):
            _c["n"] += 1
            path = media_dir / f"s{_n:02d}_{_c['n']}.png"
            _pending[path] = box
            return path

        blocks = layout_engine.slide_blocks(info, defer)
        title = _text(info["title"].runs) if info["title"] else ""
        if not title:
            first = next((b for b in blocks if b.type in ("heading", "para", "bullet")), None)
            title = _text(first.runs)[:80] if first else f"Slide {n}"
        slides.append({"n": n, "title": title, "blocks": blocks, "tags_text": tags_text, "pending": pending})
    return slides


def render_media(pptx_path, job_dir, slides, on_slide=None):
    """Render slide dengan PowerPoint lalu crop tiap gambar. Tanpa PowerPoint: gambar asli dari PPTX.
    Baris gambar yang gagal disimpan dibuang."""
    job_dir = Path(job_dir)
    rendered = layout_engine.render_slides(Path(pptx_path), job_dir / "slides")
    for s in slides:
        render = layout_engine.load_render(job_dir / "slides" / f"slide{s['n']}.png") if rendered else None
        for b in s["blocks"]:
            if b.type != "figures":
                continue
            rows = []
            for row in b.rows:
                box = s["pending"].get(row["img"])
                saved = layout_engine.save_box_image(box, row["img"], render) if box else None
                if saved:
                    rows.append(dict(row, img=saved))
            b.rows = rows
        s["blocks"] = [b for b in s["blocks"] if b.type != "figures" or b.rows]
        s["pending"] = {}
        if on_slide:
            on_slide(s["n"])
    return rendered


# ------------------------------------------------------------------ CKEditor HTML
def _slide_html(slide, job_id, title_level):
    """Blok layout_engine -> HTML. Judul slide sudah ditulis terpisah (dengan data-slide), jadi heading
    level 1 di awal dilewati dan heading lain digeser ke bawah judul slide."""
    blocks = slide["blocks"]
    if blocks and blocks[0].type == "heading" and blocks[0].level == 1:
        blocks = blocks[1:]
    shifted = [dataclasses.replace(b, level=min(title_level + b.level - 1, 6)) if b.type == "heading" else b
               for b in blocks]
    return layout_engine.blocks_to_html(
        [shifted], img_url=lambda p: f"/api/ck/media/{job_id}/{Path(p).name}")


def build_ck_html(job_id, slides, toc, mapping):
    by_code = {}
    for s in slides:
        by_code.setdefault(mapping[s["n"]]["code"], []).append(s)
    parts = []
    for node in toc:
        h = min(node["level"] + 2, 6)
        parts.append(
            f'<h{h} data-section="{node["code"]}">{html.escape(node["code"])} {html.escape(node["title"])}</h{h}>')
        for s in by_code.get(node["code"], []):
            sh = min(h + 1, 6)
            parts.append(f'<h{sh} data-slide="{s["n"]}">{html.escape(s["title"])}</h{sh}>')
            parts.append(_slide_html(s, job_id, sh))
    return "\n".join(parts)


def _public_slide(s, mapping):
    flat = []
    for b in s["blocks"]:
        if b.type in ("heading", "para", "bullet", "note"):
            text = _text(b.runs)
            if text and not (b.type == "heading" and b.level == 1 and text == s["title"]):
                flat.append(text)
        elif b.type == "figures":
            flat += ["[Gambar]"] * len(b.rows)
        elif b.type == "table":
            flat.append("[Tabel %d baris]" % len(b.rows))
    m = mapping[s["n"]]
    return {"n": s["n"], "title": s["title"], "lines": flat, "section": m["code"], "method": m["method"]}


# ------------------------------------------------------------------ flask wiring
def register(app, work_dir):
    work = Path(work_dir)
    jobs = {}
    bp = Blueprint("ck", __name__, url_prefix="/api/ck")

    def get_job(job_id):
        if not re.fullmatch(r"[0-9a-f]{10}", job_id or ""):
            abort(404)
        j = jobs.get(job_id)
        if not j:
            abort(404)
        return j

    def do_map(j):
        mapping, prev = {}, None
        for s in j["slides"]:
            code, method = map_slide(s, j["toc"], prev)
            mapping[s["n"]] = {"code": code, "method": method}
            prev = code
        return mapping

    @bp.get("/sections")
    def sections():
        return jsonify(load_sections())

    def make_job(src, source, toc):
        """Baca PPTX dari `src` lalu daftarkan sebagai job baru."""
        job_id = uuid.uuid4().hex[:10]
        d = work / ("ck_" + job_id)
        d.mkdir(parents=True)
        slides = extract_slides(src, d / "media")
        if not slides:
            raise ValueError("PPTX tidak memiliki slide.")
        j = dict(id=job_id, source=source, dir=d, src=Path(src), slides=slides, toc=toc, status="uploaded",
                 done=0, total=len(slides), pct=0, phase=0, steps=[{"t": t, "state": "wait"} for t in STEPS],
                 html="", error=None)
        j["mapping"] = do_map(j)
        jobs[job_id] = j
        return j

    def payload(j):
        return dict(exists=True, id=j["id"], source=j["source"], toc=j["toc"],
                    slides=[_public_slide(s, j["mapping"]) for s in j["slides"]])

    # Mockup OneDrive: satu dokumen aktif, disimpan di work/onedrive supaya bertahan antar refresh/restart.
    drive = work / "onedrive"
    drive_file = drive / MOCK_NAME
    current = {"id": None}

    @bp.get("/ppt")
    def ppt_state():
        j = jobs.get(current["id"])
        if not j and drive_file.exists():
            try:
                j = make_job(drive_file, MOCK_NAME, load_sections())
            except Exception as e:
                return jsonify(error=f"PPTX tidak dapat dibaca: {e}"), 500
            current["id"] = j["id"]
        return jsonify(payload(j) if j else {"exists": False})

    @bp.post("/generate")
    def generate():
        """Generate PPT (template section) ke 'OneDrive'. Sementara menyalin docs/test.pptx."""
        if not MOCK_TEMPLATE.exists():
            return jsonify(error=f"Template contoh tidak ditemukan: {MOCK_TEMPLATE.name}"), 500
        if not drive_file.exists():
            drive.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(MOCK_TEMPLATE, drive_file)
        try:
            j = make_job(drive_file, MOCK_NAME, load_sections())
        except Exception as e:
            return jsonify(error=f"PPTX tidak dapat dibaca: {e}"), 400
        current["id"] = j["id"]
        return jsonify(payload(j))

    @bp.post("/convert/<job_id>")
    def convert(job_id):
        j = get_job(job_id)
        if j["status"] == "running":
            return jsonify(id=job_id, status="running")
        j.update(status="running", done=0, pct=0, phase=0, html="", error=None,
                 steps=[{"t": t, "state": "wait"} for t in STEPS])
        threading.Thread(target=_run, args=(j,), daemon=True).start()
        return jsonify(id=job_id, status="running")

    def _run(j):
        try:
            total = len(j["slides"])

            def tick(phase, i):
                j["phase"], j["done"] = phase, i
                base = sum(WEIGHTS[:phase])
                j["pct"] = round((base + WEIGHTS[phase] * i / total) * 100)
                for k, st in enumerate(j["steps"]):
                    st["state"] = "done" if k < phase or (k == phase and i == total) else ("run" if k == phase else "wait")
                if STEP_DELAY:
                    time.sleep(STEP_DELAY)

            # 1. membaca slide: render PowerPoint + crop gambar (progress per slide setelah render)
            tick(0, 0)
            render_media(j["src"], j["dir"], j["slides"], on_slide=lambda n: tick(0, n))
            j["mapping"] = do_map(j)
            for i in range(1, total + 1):          # 2. memetakan ke section
                tick(1, i)
            j["html"] = build_ck_html(j["id"], j["slides"], j["toc"], j["mapping"])
            for i in range(1, total + 1):          # 3. membuat konten CKEditor
                tick(2, i)
            j.update(status="done", pct=100)
            for st in j["steps"]:
                st["state"] = "done"
        except Exception as e:
            j.update(status="error", error=str(e))

    @bp.get("/status/<job_id>")
    def status(job_id):
        j = get_job(job_id)
        return jsonify({k: j[k] for k in ("id", "status", "done", "total", "pct", "phase", "steps", "error")})

    @bp.get("/html/<job_id>")
    def html_out(job_id):
        j = get_job(job_id)
        if j["status"] != "done":
            return jsonify(error="Konversi belum selesai."), 409
        return jsonify(html=j["html"], slides=[_public_slide(s, j["mapping"]) for s in j["slides"]])

    @bp.get("/media/<job_id>/<path:name>")
    def media(job_id, name):
        j = get_job(job_id)
        return send_from_directory(j["dir"] / "media", name)

    app.register_blueprint(bp)
    return jobs
