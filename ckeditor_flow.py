"""PPT -> CKEditor flow (seamless editing), backend for templates/index_dwp.html.

Independent of converter.py (no Docling needed). It:
  1. takes the document .pptx (prototype: "Generate PPT" = the user uploads a deck, kept in the mock
     OneDrive folder work/onedrive), reads the slides for the PPT tab (titles, lines, section mapping) and
     renders them with PowerPoint in the background,
  2. converts the deck with report_engine, rules only (no LLM), reusing that render,
  3. maps every slide to a sub-section (leaf of the section tree, like Mapping Section PPT in DWP) and
     builds CKEditor-ready HTML grouped by section, with real progress,
  4. review: slides the report engine flagged can be fixed by hand (edited HTML), re-planned by the LLM
     with a reviewer prompt (prefilled with a recommendation from the flags), marked OK, or reverted.

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
import html
import json
import os
import re
import threading
import time
import uuid
from pathlib import Path

from flask import Blueprint, abort, jsonify, request, send_from_directory
from PIL import Image
from pptx import Presentation
from pptx.enum.shapes import MSO_SHAPE_TYPE

import layout_engine
import report_engine

HERE = Path(__file__).resolve().parent
MOCK_NAME = "DWP_Buku_3a.pptx"   # nama file PPT dokumen di "OneDrive" (prototipe: isinya PPT yang diunggah)
STEP_DELAY = float(os.environ.get("DWP_CK_STEP_DELAY", "0.02"))  # seconds per slide per phase (visible progress)

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
STEPS = ["Merender slide PPT", "Menyusun layout dengan report engine (tanpa LLM)",
         "Memetakan slide ke section Predefine", "Membuat konten CKEditor"]
STEP_LLM = "Menyusun layout: aturan + LLM untuk slide bertanda"   # langkah 2 pada mode perbaikan otomatis
WEIGHTS = (0.2, 0.55, 0.1, 0.15)
CONVERT_MODES = ("manual", "llm")   # manual: aturan saja, slide bertanda diperbaiki di review; llm: planner auto

# tanda report engine (rules_flags) -> (kenapa perlu dicek, prompt AI yang disarankan)
FLAG_INFO = report_engine.FLAG_INFO


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
        slides.append({"n": n, "title": title, "blocks": blocks, "tags_text": tags_text, "pending": pending,
                       "flags": layout_engine.slide_flags(info, blocks)})
    return slides


def render_previews(pptx_path, job_dir, numbers):
    """Render semua slide dengan PowerPoint (sekali per job) + pratinjau JPEG untuk halaman /dwp:
    slides/preview{n}.jpg (besar) dan slides/thumb{n}.jpg (thumbnail). False kalau PowerPoint tidak ada."""
    slides_dir = Path(job_dir) / "slides"
    if not (slides_dir / "slide1.png").exists():
        if not layout_engine.render_slides(Path(pptx_path), slides_dir):
            return False
    for n in numbers:
        src = slides_dir / f"slide{n}.png"
        if src.exists() and not (slides_dir / f"thumb{n}.jpg").exists():
            im = Image.open(src).convert("RGB")
            big = im.copy()
            big.thumbnail((1400, 1400))
            big.save(slides_dir / f"preview{n}.jpg", quality=82)
            im.thumbnail((360, 360))
            im.save(slides_dir / f"thumb{n}.jpg", quality=80)
    return True


# ------------------------------------------------------------------ report engine -> CKEditor HTML
def report_fragments(job_id, out_dir, rel):
    """review.json dari report_engine -> {nomor slide: hasil}. Gambar di fragmen dirujuk "media/<nama>",
    diganti ke URL file job (rel = folder hasil relatif terhadap folder job)."""
    review = json.loads((Path(out_dir) / "review.json").read_text(encoding="utf-8"))
    plans = json.loads((Path(out_dir) / "plans.json").read_text(encoding="utf-8"))
    titles = {p["n"]: p["title"] for p in plans}
    prefix = f'src="/api/ck/file/{job_id}/{rel}/media/'
    out = {}
    for s in review["slides"]:
        frag = s["html"].replace('src="media/', prefix)
        out[s["n"]] = {"auto": frag, "html": frag, "kind": s["kind"], "flags": s["flags"],
                       "title": titles.get(s["n"], ""),
                       "fix": "ai" if s.get("source") in ("llm", "cache") else None}   # diperbaiki LLM saat konversi
    return out


def flag_list(codes):
    return [{"code": c, "msg": FLAG_INFO.get(c, (c, ""))[0]} for c in codes]


def recommended_prompt(codes):
    """Prompt AI yang disarankan untuk slide bertanda: gabungan saran per tanda."""
    lines = [FLAG_INFO[c][1] for c in codes if c in FLAG_INFO and FLAG_INFO[c][1]]
    return "\n".join(lines) or "Perbaiki susunan slide ini supaya urutan dan pengelompokan isinya sesuai slide asli."


def build_ck_html(slides, toc, mapping, results):
    """Section (pohon Predefine) -> hasil report engine per slide. Slide tanpa hasil (cover, penutup) dilewati."""
    by_code = {}
    for s in slides:
        if s["n"] in results:
            by_code.setdefault(mapping[s["n"]]["code"], []).append(s)
    parts = []
    for node in toc:
        h = min(node["level"] + 2, 6)
        parts.append(
            f'<h{h} data-section="{node["code"]}">{html.escape(node["code"])} {html.escape(node["title"])}</h{h}>')
        for s in by_code.get(node["code"], []):
            parts.append(f'<div class="ck-slide" data-slide="{s["n"]}">{results[s["n"]]["html"]}</div>')
    return "\n".join(parts)


def _public_slide(s, mapping, results=None):
    """Data slide untuk halaman. Setelah konversi: tanda report engine, saran prompt AI dan status perbaikan."""
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
    out = {"n": s["n"], "title": s["title"], "lines": flat, "section": m["code"], "method": m["method"],
           "flags": []}
    r = (results or {}).get(s["n"])
    if r:
        out.update(flags=flag_list(r["flags"]), kind=r["kind"], fix=r["fix"], edited=r["html"] != r["auto"])
        if r["flags"]:
            out.update(html=r["html"], prompt=recommended_prompt(r["flags"]))
    return out


# ------------------------------------------------------------------ flask wiring
def register(app, work_dir):
    work = Path(work_dir).resolve()   # absolut: send_from_directory menafsirkan path relatif terhadap folder app
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
                 html="", error=None, render="running", render_done=threading.Event(), results={}, ai={},
                 lock=threading.Lock(), mode="manual", llm_failed=[])
        j["mapping"] = do_map(j)
        jobs[job_id] = j
        threading.Thread(target=_render_bg, args=(j,), daemon=True).start()
        return j

    def _render_bg(j):
        """Render slide di latar belakang saat PPT dimuat: pratinjau gambar asli di tab PPT, dan render
        yang sama dipakai lagi saat konversi (tidak render dua kali)."""
        try:
            ok = render_previews(j["src"], j["dir"], [s["n"] for s in j["slides"]])
            j["render"] = "done" if ok else "unavailable"
        except Exception as e:
            j["render"] = "unavailable"
            print(f"  [!] Render pratinjau gagal: {e}")
        finally:
            j["render_done"].set()

    def payload(j):
        return dict(exists=True, id=j["id"], source=j["source"], toc=j["toc"], render=j["render"],
                    status=j["status"], slides=[_public_slide(s, j["mapping"]) for s in j["slides"]])

    # Mockup OneDrive: work/onedrive. Prototipe: "Generate PPT" = pengguna mengunggah PPT.
    drive = work / "onedrive"
    current = {"id": None}

    @bp.get("/ppt")
    def ppt_state():
        """Dokumen aktif sesi server ini (untuk kembali ke posisi terakhir setelah refresh). PPT lama di
        'OneDrive' tidak dibuka otomatis: tab PPT selalu meminta generate (unggah) PPT."""
        j = jobs.get(current["id"])
        return jsonify(payload(j) if j else {"exists": False})

    @bp.post("/upload")
    def upload():
        """Generate PPT (prototipe): PPT yang diunggah menjadi PPT dokumen di 'OneDrive'."""
        f = request.files.get("pptx")
        if not f or not f.filename.lower().endswith(".pptx"):
            return jsonify(error="Pilih file .pptx."), 400
        drive.mkdir(parents=True, exist_ok=True)
        # nama unik: PPT sebelumnya bisa masih dibuka render latar belakang job lama
        dest = drive / f"{uuid.uuid4().hex[:8]}_{MOCK_NAME}"
        f.save(dest)
        try:
            Presentation(str(dest))          # file rusak / bukan PPTX -> ditolak, dokumen aktif tidak berubah
        except Exception as e:
            dest.unlink(missing_ok=True)
            return jsonify(error=f"PPTX tidak dapat dibaca: {e}"), 400
        for old in drive.glob(f"*_{MOCK_NAME}"):
            if old != dest:
                try:
                    old.unlink()
                except OSError:
                    pass                     # masih dipakai render; terhapus pada unggahan berikutnya
        try:
            j = make_job(dest, Path(f.filename).name, load_sections())
        except Exception as e:
            return jsonify(error=f"PPTX tidak dapat dibaca: {e}"), 400
        current["id"] = j["id"]
        return jsonify(payload(j))

    @bp.post("/convert/<job_id>")
    def convert(job_id):
        """mode: manual (aturan saja, tanpa LLM; slide bertanda diperbaiki di review) | llm (LLM menyusun ulang
        slide bertanda saat konversi, memakai kuota LLM)."""
        j = get_job(job_id)
        if j["status"] == "running":
            return jsonify(id=job_id, status="running")
        mode = (request.get_json(force=True, silent=True) or {}).get("mode", "manual")
        if mode not in CONVERT_MODES:
            return jsonify(error="mode tidak dikenal."), 400
        steps = [STEP_LLM if mode == "llm" and i == 1 else t for i, t in enumerate(STEPS)]
        j.update(status="running", done=0, pct=0, phase=0, html="", error=None, mode=mode, llm_failed=[],
                 steps=[{"t": t, "state": "wait"} for t in steps])
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

            # 1. render: tunggu render latar belakang (dimulai saat PPT dimuat)
            tick(0, 0)
            j["render_done"].wait(timeout=900)
            tick(0, total)

            # 2. report engine memakai render yang sama: aturan saja, atau + LLM untuk slide bertanda
            def on_progress(fraction, _message):
                tick(1, min(total, max(0, round((fraction - 0.3) / 0.7 * total))))

            rendered = j["render"] == "done"
            out = j["dir"] / "report"
            stats = report_engine.convert_report(
                j["src"], out / (Path(j["source"]).stem + ".docx"),
                planner="auto" if j["mode"] == "llm" else "rules", render=rendered,
                work_dir=out, slides_dir=j["dir"] / "slides" if rendered else None, progress=on_progress,
                comments=True)
            j["results"], j["ai"] = report_fragments(j["id"], out, "report"), {}
            j["llm_failed"] = stats["llm_failed"]
            tick(1, total)

            j["mapping"] = do_map(j)
            for i in range(1, total + 1):          # 3. memetakan ke section
                tick(2, i)
            j["html"] = build_ck_html(j["slides"], j["toc"], j["mapping"], j["results"])
            for i in range(1, total + 1):          # 4. membuat konten CKEditor
                tick(3, i)
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
        slides = [_public_slide(s, j["mapping"], j["results"]) for s in j["slides"]]
        return jsonify(html=j["html"], slides=slides, render=j["render"], mode=j["mode"], llm_failed=j["llm_failed"],
                       docx=(j["dir"] / "report" / (Path(j["source"]).stem + ".docx")).exists())

    # ---- review: perbaiki slide bertanda (manual / AI / tandai OK / kembalikan hasil otomatis)
    def get_result(j, n):
        if j["status"] != "done" or n not in j["results"]:
            abort(404)
        return j["results"][n]

    def slide_reply(j, n):
        with j["lock"]:
            j["html"] = build_ck_html(j["slides"], j["toc"], j["mapping"], j["results"])
        s = next(s for s in j["slides"] if s["n"] == n)
        pub = _public_slide(s, j["mapping"], j["results"])
        pub["html"] = j["results"][n]["html"]
        return jsonify(slide=pub, html=j["html"])

    @bp.post("/fix/<job_id>/<int:n>")
    def fix(job_id, n):
        """action: manual (html hasil edit) | ok (hasil otomatis sudah benar) | revert (kembali ke hasil otomatis)."""
        j = get_job(job_id)
        r = get_result(j, n)
        body = request.get_json(force=True, silent=True) or {}
        action = body.get("action")
        if action == "manual":
            text = str(body.get("html", ""))
            if re.search(r"<\s*(script|iframe|object|embed)\b|\son\w+\s*=", text, re.I):
                return jsonify(error="HTML berisi script atau atribut event."), 400
            r.update(html=text, fix="manual")
        elif action == "ok":
            r["fix"] = "ok"
        elif action == "revert":
            r.update(html=r["auto"], fix=None)
        else:
            return jsonify(error="action tidak dikenal."), 400
        return slide_reply(j, n)

    @bp.post("/ai/<job_id>/<int:n>")
    def ai_fix(job_id, n):
        """Perbaiki dengan AI: LLM menyusun ulang rencana slide ini dengan prompt reviewer (memakai kuota LLM)."""
        j = get_job(job_id)
        get_result(j, n)
        body = request.get_json(force=True, silent=True) or {}
        prompt = str(body.get("prompt", "")).strip()[:2000]
        if not prompt:
            return jsonify(error="Prompt AI kosong."), 400
        if j["ai"].get(n, {}).get("status") == "running":
            return jsonify(status="running")
        j["ai"][n] = {"status": "running", "error": None}
        provider = body.get("provider") or "gemini"
        model = body.get("model") or report_engine.DEFAULT_MODEL
        threading.Thread(target=_run_ai, args=(j, n, prompt, provider, model), daemon=True).start()
        return jsonify(status="running")

    def _run_ai(j, n, prompt, provider, model):
        state = j["ai"][n]
        try:
            k = len(list((j["dir"] / "ai").glob(f"s{n}_*"))) + 1 if (j["dir"] / "ai").exists() else 1
            rel = f"ai/s{n}_{k}"
            out = j["dir"] / rel
            rendered = j["render"] == "done"
            stats = report_engine.convert_report(
                j["src"], out / "slide.docx", planner="llm", provider=provider, model=model, only={n},
                instruction=prompt, render=rendered, work_dir=out,
                slides_dir=j["dir"] / "slides" if rendered else None)
            if n in stats["llm_failed"] or not stats["llm_slides"] + stats["cache_hits"]:
                plans = json.loads((out / "plans.json").read_text(encoding="utf-8"))
                errors = next((p["errors"] for p in plans if p["n"] == n), [])
                raise RuntimeError("; ".join(errors[-2:]) or "LLM tidak menghasilkan rencana yang sah.")
            res = report_fragments(j["id"], out, rel).get(n)
            if not res:
                raise RuntimeError("Slide ini tidak menghasilkan isi dokumen.")
            j["results"][n].update(html=res["html"], fix="ai")
            state["status"] = "done"
        except Exception as e:
            state.update(status="error", error=str(e))

    @bp.get("/ai/<job_id>/<int:n>")
    def ai_state(job_id, n):
        j = get_job(job_id)
        state = j["ai"].get(n)
        if not state:
            abort(404)
        if state["status"] == "done":
            reply = slide_reply(j, n).get_json()
            return jsonify(status="done", **reply)
        return jsonify(state)

    @bp.get("/docx/<job_id>")
    def docx(job_id):
        """DOCX hasil otomatis report engine (belum termasuk perbaikan di halaman review)."""
        j = get_job(job_id)
        name = Path(j["source"]).stem + ".docx"
        if j["status"] != "done" or not (j["dir"] / "report" / name).exists():
            abort(404)
        return send_from_directory(j["dir"] / "report", name, as_attachment=True)

    @bp.get("/render/<job_id>")
    def render_state(job_id):
        return jsonify(render=get_job(job_id)["render"])

    @bp.get("/slide/<job_id>/<path:name>")
    def slide_image(job_id, name):
        """Pratinjau slide: preview{n}.jpg / thumb{n}.jpg."""
        j = get_job(job_id)
        if not re.fullmatch(r"(preview|thumb)\d+\.jpg", name):
            abort(404)
        return send_from_directory(j["dir"] / "slides", name)

    @bp.get("/file/<job_id>/<path:name>")
    def job_file(job_id, name):
        """Gambar hasil report engine: report/media/... dan ai/s<n>_<k>/media/..."""
        j = get_job(job_id)
        if not re.fullmatch(r"(report|ai/s\d+_\d+)/media/[\w.\-]+", name):
            abort(404)
        return send_from_directory(j["dir"], name)

    app.register_blueprint(bp)
    return jobs
