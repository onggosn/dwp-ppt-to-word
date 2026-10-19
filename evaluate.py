"""Skor hasil konversi (DOCX) terhadap DOCX acuan yang benar (gold), per slide dan per tipe slide.

Kedua dokumen dibaca jadi urutan item: h1 (judul slide), h2, label (paragraf tebal / Heading 3+),
p (paragraf isi) dan fig (gambar + keterangannya); lalu dipotong per slide di setiap h1.
Per slide (dipasangkan lewat judul):
  text_f1     paragraf yang sama (teks dinormalisasi, toleransi typo kecil) -> precision/recall/F1
  role        dari paragraf yang cocok, berapa yang perannya sama (h2 / label / p)
  order       urutan paragraf yang cocok (longest increasing subsequence / jumlah cocok)
  fig_f1      gambar dengan keterangan yang sama -> F1 (jumlah gambar ikut dihitung)
  fig_order   urutan gambar yang cocok
  score       rata-rata metrik yang berlaku; slide acuan yang tidak ada di hasil = 0
Bisa dipakai untuk hasil engine mana pun (layout_engine, report_engine, Docling+LLM), asal judul slide
ditulis sebagai Heading 1.

CLI:
    python evaluate.py --gold docs/test3.docx --out work/test3_report.docx [--plans work/..._build/plans.json] [--detail]
"""
from __future__ import annotations

import argparse
import json
import re
import unicodedata
from difflib import SequenceMatcher
from pathlib import Path

from docx import Document
from docx.oxml.ns import qn
from docx.table import Table
from docx.text.paragraph import Paragraph

FUZZY = 0.9                      # kemiripan minimal dua paragraf dianggap sama
TITLE_FUZZY = 0.8                # kemiripan minimal judul slide untuk memasangkan slide
SKIP_TEXTS = {"gambar dan keterangan"}
_QUOTES = str.maketrans({"’": "'", "‘": "'", "“": '"', "”": '"', "–": "-", "—": "-", "\xa0": " "})


def norm(t: str) -> str:
    t = unicodedata.normalize("NFKC", t).translate(_QUOTES).replace("…", "...")
    t = re.sub(r"\s+", " ", t).strip().lower()
    return re.sub(r" +([,.;:)%])", r"\1", t)


def _style_id(p: Paragraph) -> str:
    ppr = p._p.pPr
    st = ppr.find(qn("w:pStyle")) if ppr is not None else None
    return (st.get(qn("w:val")) if st is not None else "") or ""


def _role(p: Paragraph) -> str:
    sid = _style_id(p).lower().replace(" ", "")
    m = re.match(r"heading(\d)", sid)
    if m:
        return {"1": "h1", "2": "h2"}.get(m.group(1), "label")
    runs = [r for r in p.runs if r.text.strip()]
    if runs and all(r.bold for r in runs) and len(p.text.strip()) <= 80:
        return "label"
    return "p"


def _has_drawing(el) -> bool:
    return bool(el.findall(".//" + qn("w:drawing")) or el.findall(".//" + qn("w:pict")))


def read_items(path: Path) -> list:
    """[(role, teks ternormalisasi)] dalam urutan dokumen."""
    doc = Document(str(path))
    items = []
    for el in doc.element.body.iterchildren():
        tag = el.tag.split("}")[1]
        if tag == "p":
            p = Paragraph(el, doc)
            text = norm(p.text)
            if _has_drawing(el):
                items.append(("fig", ""))
            elif text and text not in SKIP_TEXTS:
                items.append((_role(p), text))
        elif tag == "tbl":
            for row in Table(el, doc).rows:
                cells, prev = [], None
                for c in row.cells:            # sel gabungan muncul berulang -> ambil sekali
                    if c._tc is not prev:
                        cells.append(c)
                    prev = c._tc
                if any(_has_drawing(c._tc) for c in cells):
                    items.append(("fig", norm(" ".join(c.text for c in cells))))
                elif items and items[-1][0] == "fig" and not items[-1][1]:
                    # tabel gambar 1 kolom: keterangan di baris bawah gambar
                    items[-1] = ("fig", norm(" ".join(c.text for c in cells)))
                else:
                    text = norm(" | ".join(c.text for c in cells))
                    if text.strip(" |"):
                        items.append(("table", text))
    return items


def split_slides(items: list) -> list:
    """[(judul, [item])]; item sebelum h1 pertama (judul dokumen) dibuang."""
    slides = []
    for role, text in items:
        if role == "h1":
            slides.append((text, []))
        elif slides:
            slides[-1][1].append((role, text))
    return slides


def _match(gold: list, out: list) -> list:
    """Pasangan (i_gold, j_out): sama persis dulu, lalu yang mirip >= FUZZY."""
    pairs, used = [], set()
    for exact in (True, False):
        for i, g in enumerate(gold):
            if any(pi == i for pi, _ in pairs):
                continue
            for j, o in enumerate(out):
                if j in used:
                    continue
                if (g == o) if exact else SequenceMatcher(None, g, o, autojunk=False).ratio() >= FUZZY:
                    pairs.append((i, j))
                    used.add(j)
                    break
    return sorted(pairs)


def _lis(seq: list) -> int:
    tails = []
    for x in seq:
        k = next((i for i, t in enumerate(tails) if t >= x), len(tails))
        if k == len(tails):
            tails.append(x)
        else:
            tails[k] = x
    return len(tails)


def _f1(n_match: int, n_gold: int, n_out: int) -> float:
    if n_gold == 0 and n_out == 0:
        return 1.0
    p = n_match / n_out if n_out else 0.0
    r = n_match / n_gold if n_gold else 0.0
    return 2 * p * r / (p + r) if p + r else 0.0


def score_slide(gold: list, out: list) -> dict:
    g_txt = [(r, t) for r, t in gold if r not in ("fig",)]
    o_txt = [(r, t) for r, t in out if r not in ("fig",)]
    pairs = _match([t for _, t in g_txt], [t for _, t in o_txt])
    m = {
        "text_f1": _f1(len(pairs), len(g_txt), len(o_txt)),
        "role": sum(g_txt[i][0] == o_txt[j][0] for i, j in pairs) / len(pairs) if pairs else (1.0 if not g_txt else 0.0),
        "order": _lis([j for _, j in pairs]) / len(pairs) if pairs else (1.0 if not g_txt else 0.0),
    }
    g_fig = [t for r, t in gold if r == "fig"]
    o_fig = [t for r, t in out if r == "fig"]
    if g_fig or o_fig:
        fp = _match(g_fig, o_fig)
        m["fig_f1"] = _f1(len(fp), len(g_fig), len(o_fig))
        m["fig_order"] = _lis([j for _, j in fp]) / len(fp) if fp else 0.0
    m["score"] = sum(m.values()) / len(m)
    m["missing"] = [g_txt[i][1] for i in range(len(g_txt)) if i not in {a for a, _ in pairs}] + \
        [f"[fig] {t}" for i, t in enumerate(g_fig) if i not in {a for a, _ in _match(g_fig, o_fig)}]
    m["extra"] = [o_txt[j][1] for j in range(len(o_txt)) if j not in {b for _, b in pairs}] + \
        [f"[fig] {t}" for j, t in enumerate(o_fig) if j not in {b for _, b in _match(g_fig, o_fig)}]
    m["roles_wrong"] = [f"{g_txt[i][0]}->{o_txt[j][0]}: {g_txt[i][1][:60]}" for i, j in pairs
                        if g_txt[i][0] != o_txt[j][0]]
    return m


def evaluate(gold_path: Path, out_path: Path, plans_path: Path | None = None) -> dict:
    gold, out = split_slides(read_items(gold_path)), split_slides(read_items(out_path))
    kinds = {}
    if plans_path and Path(plans_path).exists():
        for s in json.loads(Path(plans_path).read_text(encoding="utf-8")):
            kinds[norm(s["title"])] = (s["kind"], s["source"])
    results, taken = [], set()
    for title, items in gold:
        best, best_r = None, TITLE_FUZZY
        for j, (t2, _) in enumerate(out):
            r = SequenceMatcher(None, title, t2, autojunk=False).ratio()
            if j not in taken and r >= best_r:
                best, best_r = j, r
        kind, source = next((v for k, v in kinds.items()
                             if SequenceMatcher(None, title, k, autojunk=False).ratio() >= TITLE_FUZZY), ("?", "?"))
        if best is None:
            results.append({"title": title, "kind": kind, "source": source, "score": 0.0, "found": False})
            continue
        taken.add(best)
        results.append({"title": title, "kind": kind, "source": source, "found": True,
                        **score_slide(items, out[best][1])})
    by_kind = {}
    for r in results:
        by_kind.setdefault(r["kind"], []).append(r["score"])
    return {"slides": results,
            "overall": sum(r["score"] for r in results) / len(results) if results else 0.0,
            "by_kind": {k: sum(v) / len(v) for k, v in by_kind.items()},
            "extra_slides": [t for j, (t, _) in enumerate(out) if j not in taken]}


def print_report(res: dict, detail: bool):
    cols = ("text_f1", "role", "order", "fig_f1", "fig_order", "score")
    print(f"{'slide':52} {'tipe':8} {'sumber':6} " + " ".join(f"{c:>9}" for c in cols))
    for r in res["slides"]:
        vals = " ".join(f"{r[c]:9.1%}" if c in r else f"{'-':>9}" for c in cols)
        print(f"{r['title'][:52]:52} {r['kind'][:8]:8} {r['source'][:6]:6} {vals}"
              + ("" if r["found"] else "   (slide tidak ditemukan)"))
        if detail and r["found"]:
            for key in ("missing", "extra", "roles_wrong"):
                for t in r[key]:
                    print(f"      {key}: {t[:110]}")
    print(f"\nskor total: {res['overall']:.1%}")
    for k, v in sorted(res["by_kind"].items()):
        print(f"  {k:10} {v:.1%}")
    if res["extra_slides"]:
        print(f"slide di hasil yang tidak ada di acuan: {len(res['extra_slides'])}")


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="Skor DOCX hasil konversi terhadap DOCX acuan")
    ap.add_argument("--gold", required=True, help="DOCX acuan yang benar (mis. docs/test3.docx)")
    ap.add_argument("--out", required=True, help="DOCX hasil konversi")
    ap.add_argument("--plans", default=None, help="plans.json dari report_engine (tipe & sumber per slide)")
    ap.add_argument("--detail", action="store_true", help="tampilkan paragraf yang hilang/lebih/salah peran")
    ap.add_argument("--json", action="store_true", help="keluaran JSON")
    a = ap.parse_args()
    result = evaluate(Path(a.gold), Path(a.out), Path(a.plans) if a.plans else None)
    if a.json:
        print(json.dumps(result, ensure_ascii=False, indent=1))
    else:
        print_report(result, a.detail)
