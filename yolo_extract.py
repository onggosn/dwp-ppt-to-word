"""PPTX -> DOCX + HTML dengan custom YOLO model (pengganti analyse() berbasis aturan di layout_engine.py).

Alur:
  1. render_slides()  slide dirender PowerPoint (COM) ke PNG, sama seperti layout_engine / prepare_dataset.
  2. YOLO             tiap PNG dideteksi: Title | Subtitle | Plain Text | Picture | Caption Picture.
  3. collect()        shape python-pptx dibaca (teks, format, gambar, tabel) dalam koordinat fraksi slide.
  4. cocokkan         tiap shape teks diberi peran dari deteksi yang paling menutupinya (overlap),
                      Picture = crop dari render, Caption dipasangkan ke Picture terdekat.
  5. slide_blocks()   hasilnya diubah ke info dict yang sama dengan analyse(), jadi DocxWriter dan HTML
                      writer dari layout_engine dipakai apa adanya.

Tabel tidak ada di 5 kelas model, jadi tetap diambil langsung dari shape tabel PPTX.
Shape yang tidak tertangkap model (teks / gambar) tidak dibuang: dipakai sebagai fallback dan dihitung di stats.

CLI:
    python yolo_extract.py docs/test2.pptx -o work/test2_yolo.docx
    python yolo_extract.py docs/test2.pptx --weights runs/detect/train/weights/best.pt --conf 0.25
"""
from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

from PIL import Image, ImageDraw
from pptx import Presentation

import layout_engine as le
from layout_engine import Box

HERE = Path(__file__).resolve().parent
DEFAULT_WEIGHTS = HERE / "runs" / "detect" / "train" / "weights" / "best.pt"
CLASSES = ["Title", "Subtitle", "Plain Text", "Picture", "Caption Picture"]  # urutan = train/data.yaml
TEXT_CLASSES = ("Title", "Subtitle", "Plain Text", "Caption Picture")

CONF = 0.25            # ambang skor deteksi
IMGSZ = 1024           # harus sama dengan imgsz saat training
ASSIGN_MIN = 0.5       # minimal bagian shape teks yang harus tertutup deteksi
CAPTION_MAX_GAP = 0.10  # jarak vertikal maksimal caption <-> gambar (fraksi tinggi slide)

COLORS = {"Title": "red", "Subtitle": "orange", "Plain Text": "blue",
          "Picture": "green", "Caption Picture": "purple"}


# --------------------------------------------------------------------------- 1. deteksi
@dataclass
class Det:
    label: str
    conf: float
    box: Box                  # koordinat fraksi slide (kind="det")

    @property
    def area(self) -> float:
        return self.box.w * self.box.h


def load_model(weights=DEFAULT_WEIGHTS):
    from ultralytics import YOLO
    weights = Path(weights)
    if not weights.exists():
        raise FileNotFoundError(f"Weights tidak ditemukan: {weights}")
    return YOLO(str(weights))


def _default_device() -> str:
    try:
        import torch
        return "0" if torch.cuda.is_available() else "cpu"
    except Exception:
        return "cpu"


def detect(model, png: Path, conf: float = CONF, device: Optional[str] = None) -> list:
    """Jalankan model pada satu gambar slide. Mengembalikan [Det] dengan koordinat fraksi (0..1)."""
    res = model.predict(str(png), imgsz=IMGSZ, conf=conf, device=device or _default_device(), verbose=False)[0]
    dets = []
    for (x0, y0, x1, y1), c, s in zip(res.boxes.xyxyn.tolist(), res.boxes.cls.tolist(), res.boxes.conf.tolist()):
        label = res.names[int(c)]
        dets.append(Det(label, float(s), Box("det", x0, y0, x1 - x0, y1 - y0, name=label)))
    return dets


# --------------------------------------------------------------------------- 2. cocokkan deteksi <-> shape
def _frac_covered(b: Box, d: Det) -> float:
    """Bagian luas shape b yang tertutup deteksi d (0..1)."""
    area = max(b.w * b.h, 1e-9)
    return le._inter(b, d.box) / area


def _center_in(b: Box, d: Det) -> bool:
    cx, cy = b.x + b.w / 2, b.y + b.h / 2
    return d.box.x <= cx <= d.box.r and d.box.y <= cy <= d.box.b


def best_det(t: Box, dets: list) -> Optional[Det]:
    """Deteksi terbaik untuk shape teks t. Kelas teks diutamakan; Picture hanya dipakai kalau tidak ada
    kelas teks yang cocok (artinya teks itu bagian dari gambar/grafik dan ikut ter-crop)."""
    cands = [(d, _frac_covered(t, d)) for d in dets]
    cands = [(d, f) for d, f in cands if f >= ASSIGN_MIN]
    for group in (TEXT_CLASSES, ("Picture",)):
        pool = [(d, f) for d, f in cands if d.label in group]
        if pool:
            # skor tertinggi; kalau sama, pilih deteksi yang lebih kecil (lebih spesifik)
            return max(pool, key=lambda x: (round(x[1] * x[0].conf, 2), -x[0].area))[0]
    return None


def _pair_captions(caps: list, pics: list) -> tuple:
    """Pasangkan tiap caption ke satu gambar terdekat (atas / bawah). Mengembalikan (dict id(pic)->cap, sisa)."""
    pairs, left = {}, []
    for c in sorted(caps, key=lambda b: (b.y, b.x)):
        best, best_gap = None, None
        for p in pics:
            if id(p) in pairs or le._h_overlap(c, p) < 0.3:
                continue
            gap = p.y - c.b if c.b <= p.y + 0.02 else (c.y - p.b if c.y >= p.b - 0.02 else None)
            if gap is None or not (-0.03 <= gap <= CAPTION_MAX_GAP):
                continue
            if best_gap is None or abs(gap) < best_gap:
                best, best_gap = p, abs(gap)
        if best is not None:
            pairs[id(best)] = c
        else:
            left.append(c)
    return pairs, left


def build_info(boxes: list, dets: list, stats: Optional[dict] = None) -> dict:
    """Susun info dict yang kompatibel dengan layout_engine.slide_blocks() dari deteksi model."""
    stats = stats if stats is not None else {}
    pic_dets = [d for d in dets if d.label == "Picture"]

    # --- gambar: kotak dari model, gambar aslinya (cadangan tanpa render) dari shape di dalamnya
    pics = []
    for d in pic_dets:
        unit = Box("picture", d.box.x, d.box.y, d.box.w, d.box.h, name="yolo-picture")
        for b in boxes:
            if b.kind == "picture" and _center_in(b, d):
                unit.images += b.images
        pics.append(unit)
    # gambar/grafik di PPTX yang luput dari model -> tetap ikut (jangan ada konten hilang)
    for b in boxes:
        if b.kind == "picture" and b.w >= le.ICON_MAX_W and not any(_center_in(b, d) for d in pic_dets):
            pics.append(Box("picture", b.x, b.y, b.w, b.h, name=b.name, images=b.images))
            stats["pictures_fallback"] = stats.get("pictures_fallback", 0) + 1

    # --- tabel: bukan kelas model; ambil dari shape tabel. Yang terlalu lebar dijadikan gambar.
    tables = []
    for b in boxes:
        if b.kind != "table":
            continue
        if max((len(r) for r in b.rows), default=0) > le.TABLE_MAX_COLS:
            pics.append(Box("picture", b.x, b.y, b.w, b.h, name=b.name, rows=b.rows))
        else:
            tables.append(b)
    tables.sort(key=lambda b: (b.y, b.x))

    # --- teks: peran dari deteksi
    groups = {c: [] for c in TEXT_CLASSES}
    fallback = []
    for t in boxes:
        if t.kind != "text" or len(t.text.strip()) <= 2:
            continue
        d = best_det(t, dets)
        if d is None:
            if not any(le._inside(t, p) or le._inter(t, p) > 0.5 * t.w * t.h for p in pics):
                fallback.append(t)
        elif d.label in groups:
            groups[d.label].append(t)
        # d.label == "Picture": teks bagian gambar, sudah ikut ter-crop
    if fallback:
        stats["text_fallback"] = stats.get("text_fallback", 0) + len(fallback)
        groups["Plain Text"] += fallback

    # judul: placeholder judul diutamakan, lalu yang paling atas; sisanya turun jadi sub-judul
    titles = sorted(groups["Title"], key=lambda b: (not b.is_title, b.y, b.x))
    if not titles:
        ph = [t for t in groups["Plain Text"] if t.is_title]
        if ph:
            titles = ph[:1]
            groups["Plain Text"] = [t for t in groups["Plain Text"] if t is not ph[0]]
    title = titles[0] if titles else None
    if title:
        title.is_title = True
    subheads = titles[1:] + groups["Subtitle"]

    # caption <-> gambar
    pics.sort(key=lambda p: (p.y, p.x))
    pairs, orphan_caps = _pair_captions(groups["Caption Picture"], pics)
    figures = [(p, pairs.get(id(p))) for p in pics]
    figures.sort(key=lambda f: (f[0].w >= le.WIDE_MIN_W, round(f[0].x, 1), f[0].y))

    # isi: catatan kaki, kolom, badan
    rest = groups["Plain Text"] + orphan_caps
    notes = sorted([t for t in rest if t.y >= le.NOTE_MIN_Y], key=lambda b: (b.y, b.x))
    bodies = [t for t in rest if t.y < le.NOTE_MIN_Y]
    columns = []
    tall = sorted([b for b in bodies if b.h > 0.4], key=lambda b: b.x)
    if len(tall) >= 2 and all(tall[i].r <= tall[i + 1].x + 0.03 for i in range(len(tall) - 1)):
        columns = [(None, c) for c in tall]
        bodies = [b for b in bodies if b not in tall]

    return dict(title=title,
                subheads=sorted(subheads, key=lambda b: (b.y, b.x)),
                columns=columns, panels=[],
                bodies=sorted(bodies, key=lambda b: (round(b.y, 2), b.x)),
                figures=figures, tables=tables, notes=notes)


# --------------------------------------------------------------------------- 3. debug
def draw_detections(png: Path, dets: list, out: Path) -> None:
    """Simpan gambar slide dengan kotak prediksi model (untuk dicek mata)."""
    img = Image.open(png).convert("RGB")
    dr = ImageDraw.Draw(img)
    W, H = img.size
    lw = max(2, W // 400)
    for d in dets:
        x0, y0, x1, y1 = d.box.x * W, d.box.y * H, d.box.r * W, d.box.b * H
        color = COLORS.get(d.label, "black")
        dr.rectangle([x0, y0, x1, y1], outline=color, width=lw)
        dr.text((x0 + 3, y0 + 3), f"{d.label} {d.conf:.2f}", fill=color)
    out.parent.mkdir(parents=True, exist_ok=True)
    img.thumbnail((1600, 1600))
    img.save(out, quality=85)


# --------------------------------------------------------------------------- 4. konversi
def convert_pptx_yolo(
    pptx_path,
    docx_path,
    html_path=None,
    weights=DEFAULT_WEIGHTS,
    template=le.DEFAULT_TEMPLATE,
    work_dir=None,
    conf: float = CONF,
    device: Optional[str] = None,
    include_hidden: bool = False,
    debug: bool = True,
) -> dict:
    pptx_path, docx_path = Path(pptx_path), Path(docx_path)
    work = Path(work_dir) if work_dir else docx_path.parent / (docx_path.stem + "_build")
    render_dir, media_dir, dbg_dir = work / "slides", work / "media", work / "yolo"
    work.mkdir(parents=True, exist_ok=True)

    print("1/4 Merender slide dengan PowerPoint ...")
    if not le.render_slides(pptx_path, render_dir):
        raise RuntimeError("Render slide gagal (butuh PowerPoint di Windows). Model YOLO bekerja di atas gambar slide.")

    print(f"2/4 Memuat model: {weights}")
    model = load_model(weights)

    print("3/4 Deteksi + ekstraksi per slide ...")
    prs = Presentation(str(pptx_path))
    W, H = prs.slide_width, prs.slide_height
    slides, per_slide, skipped, stats = [], {}, [], {"pictures_fallback": 0, "text_fallback": 0}
    for n, slide in enumerate(prs.slides, 1):
        if le.is_hidden(slide) and not include_hidden:
            skipped.append(n)
            continue
        png = render_dir / f"slide{n}.png"
        dets = detect(model, png, conf=conf, device=device)
        boxes = [b for b in le.collect(slide.shapes, W, H) if le._on_slide(b)]
        info = build_info(boxes, dets, stats)
        blocks = le.slide_blocks(info, le.make_cropper(png, media_dir, n))
        slides.append(blocks)
        per_slide[f"slide{n}"] = [{"label": d.label, "conf": round(d.conf, 3),
                                   "xywhn": [round(v, 4) for v in (d.box.x, d.box.y, d.box.w, d.box.h)]}
                                  for d in dets]
        if debug:
            draw_detections(png, dets, dbg_dir / f"slide{n}_yolo.jpg")
        print(f"  slide {n}: {len(dets)} deteksi, {len(blocks)} blok")
    (work / "yolo_detections.json").write_text(json.dumps(per_slide, indent=1), encoding="utf-8")

    print("4/4 Menulis dokumen ...")
    w = le.DocxWriter(Path(template))
    for blocks in slides:
        w.write(blocks)
    w.save(docx_path)
    out = {"slides": len(slides), "hidden_skipped": skipped, "docx": str(docx_path), **stats}
    if html_path:
        Path(html_path).write_text(le.html_document(le.blocks_to_html(slides), pptx_path.stem), encoding="utf-8")
        out["html"] = str(html_path)
    print(f"Selesai: {out}")
    return out


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="PPTX -> DOCX/HTML memakai custom YOLO model")
    ap.add_argument("pptx")
    ap.add_argument("-o", "--out", help="path .docx (default: work/<nama>_yolo.docx)")
    ap.add_argument("--html", help="path .html opsional (untuk CKEditor)")
    ap.add_argument("--weights", default=str(DEFAULT_WEIGHTS))
    ap.add_argument("--conf", type=float, default=CONF)
    ap.add_argument("--device", default=None, help="mis. 0 atau cpu (default: otomatis)")
    ap.add_argument("--include-hidden", action="store_true")
    ap.add_argument("--no-debug", action="store_true", help="jangan simpan gambar kotak prediksi")
    a = ap.parse_args()
    src = Path(a.pptx)
    convert_pptx_yolo(src, a.out or HERE / "work" / f"{src.stem}_yolo.docx", html_path=a.html,
                      weights=a.weights, conf=a.conf, device=a.device,
                      include_hidden=a.include_hidden, debug=not a.no_debug)
