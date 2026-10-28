"""DWP Plugin dalam Python: semua tombol ribbon DWP_Plugin.ppam + "Convert to Word" (report engine).

.ppam hanya berisi satu makro (addin/DWPShim.bas) yang menjalankan  DWP_Addin.exe <id tombol>  tanpa menunggu.
Program ini menyambung ke PowerPoint yang sedang terbuka (COM) dan bekerja pada presentasi / slide / seleksi
aktif, persis seperti makro VBA versi 1.1.

CLI (juga untuk uji tanpa klik):
    python addin/dwp_addin.py btnTitle
    python addin/dwp_addin.py btnKeynote --answer 2 --quiet     # jawaban InputBox dari argumen, pesan ke stdout
"""
from __future__ import annotations

import argparse
import os
import sys
import tempfile
import threading
import time
import traceback
from pathlib import Path

if not getattr(sys, "frozen", False):
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))   # report_engine dkk. di root repo

TITLE = "DWP Plugin"
VERSION = "2.0"
LOG_DIR = Path(tempfile.gettempdir()) / "dwp_addin"

# konstanta PowerPoint / Office
SEL_SHAPES, SEL_TEXT = 2, 3
MSO_GROUP, MSO_PICTURE = 6, 13
PASTE_ENHANCED_METAFILE = 2
SAVE_AS_PPTX = 24


# --------------------------------------------------------------------------- dialog
class UI:
    """MsgBox / InputBox. quiet: pesan ke stdout dan jawaban dari --answer (untuk uji otomatis)."""

    def __init__(self, quiet: bool = False, answer: str | None = None):
        self.quiet, self.answer, self._root = quiet, answer, None

    def root(self):
        if self._root is None:
            import tkinter as tk
            self._root = tk.Tk()
            self._root.withdraw()
            self._root.attributes("-topmost", True)
        return self._root

    def info(self, msg: str):
        self._show("info", msg)

    def warn(self, msg: str):
        self._show("warning", msg)

    def error(self, msg: str):
        self._show("error", msg)

    def _show(self, kind: str, msg: str):
        if self.quiet:
            print(f"[{kind}] {msg}")
            return
        from tkinter import messagebox
        getattr(messagebox, {"info": "showinfo", "warning": "showwarning", "error": "showerror"}[kind])(
            TITLE, msg, parent=self.root())

    def ask(self, prompt: str, title: str = TITLE) -> str:
        """"" = dibatalkan (seperti InputBox)."""
        if self.quiet:
            print(f"[ask] {prompt} -> {self.answer!r}")
            return (self.answer or "").strip()
        from tkinter import simpledialog
        return (simpledialog.askstring(title, prompt, parent=self.root()) or "").strip()


# --------------------------------------------------------------------------- PowerPoint
def powerpoint():
    import win32com.client
    try:
        return win32com.client.GetActiveObject("PowerPoint.Application")
    except Exception:
        raise UserError("PowerPoint tidak sedang terbuka.")


class UserError(Exception):
    """Pesan untuk pengguna (bukan bug): ditampilkan sebagai peringatan, tanpa traceback."""


def _selection(app):
    try:
        return app.ActiveWindow.Selection
    except Exception:
        raise UserError("Buka presentasi terlebih dahulu.")


def selected_text_shape(app):
    """Shape teks yang dipilih / tempat kursor berada (aturan sama dengan makro VBA)."""
    sel = _selection(app)
    if sel.Type == SEL_TEXT:
        shp = sel.TextRange.Parent.Parent
    elif sel.Type == SEL_SHAPES:
        shp = sel.ShapeRange(1)
    else:
        raise UserError("Please place the cursor inside a text box or select one.")
    if not shp.HasTextFrame:
        raise UserError("The selected shape is not a text box.")
    if not shp.TextFrame.HasText:
        raise UserError("The selected shape has no text.")
    return shp


def current_slide(app):
    try:
        return app.ActiveWindow.View.Slide
    except Exception:
        raise UserError("Pilih slide terlebih dahulu.")


def notes_shape(slide):
    return slide.NotesPage.Shapes.Placeholders(2)


def notes_text(slide) -> str:
    tf = notes_shape(slide).TextFrame
    return tf.TextRange.Text if tf.HasText else ""


def set_notes(slide, text: str):
    notes_shape(slide).TextFrame.TextRange.Text = text


# --------------------------------------------------------------------------- catatan slide (logika murni, diuji)
IGNORE, PENYUSUN = "::ignore::", "::penyusun::"


def add_ignore(notes: str) -> tuple:
    """(catatan baru atau None bila sudah ada, pesan)."""
    if IGNORE in notes:
        return None, f"{IGNORE} sudah ada pada slide ini."
    return (notes + "\r" + IGNORE if notes else IGNORE), f"Berhasil menambahkan {IGNORE}"


def penyusun(notes: str) -> str:
    i = notes.find(PENYUSUN)
    return notes[i + len(PENYUSUN):].strip() if i >= 0 else ""


def add_nip(notes: str, nip: str) -> tuple:
    """Catatan lain di slide tetap ada (makro VBA 1.1 menghapusnya bila belum ada ::penyusun::)."""
    if PENYUSUN not in notes:
        return (notes + "\r" if notes else "") + PENYUSUN + "\r" + nip, "NIP berhasil ditambahkan."
    if nip in notes:
        return None, "NIP sudah ada."
    return notes + "\r" + nip, "NIP berhasil ditambahkan."


def remove_nip(notes: str, nip: str) -> tuple:
    lines = notes.split("\r")
    kept = [ln for ln in lines if ln.strip() == PENYUSUN or ln.strip() != nip]
    if len(kept) == len(lines):
        return None, "NIP tidak ditemukan."
    return "\r".join(kept).strip(), "NIP berhasil dihapus."


# --------------------------------------------------------------------------- aksi tombol
def rename_text(app, ui, prefix: str, prompt: str | None = None, title: str = TITLE):
    shp = selected_text_shape(app)
    name = prefix
    if prompt:
        order = ui.ask(prompt, title)
        if not order:
            return
        name = prefix + order
    shp.Name = name
    ui.info(f"Text box renamed to '{name}'.")


def identify_title(app, ui):
    rename_text(app, ui, "#title")


def identify_keynotes(app, ui):
    rename_text(app, ui, "#keynotes", "Enter the order number for this keynote:", "Keynote Order Number")


def identify_textbox(app, ui):
    rename_text(app, ui, "#textbox", "Enter the order number for this textbox:", "Textbox Order Number")


def identify_textbox_full(app, ui):
    rename_text(app, ui, "#textboxfull", "Enter the order number for this textbox:", "Textbox Order Number")


def _paste_picture(slide, retries: int = 5):
    for i in range(retries):          # clipboard dari proses lain kadang belum siap
        try:
            return slide.Shapes.PasteSpecial(PASTE_ENHANCED_METAFILE)(1)
        except Exception:
            if i == retries - 1:
                raise
            time.sleep(0.3)


def identify_picture(app, ui, full: bool = False):
    sel = _selection(app)
    if sel.Type != SEL_SHAPES and (full or sel.Type != SEL_TEXT):
        raise UserError("Please select one or more objects first." if full
                        else "Please place the cursor inside a text box or select one.")
    shapes = sel.ShapeRange
    slide = current_slide(app)
    if all(shapes(i).Type == MSO_PICTURE for i in range(1, shapes.Count + 1)):
        picture = shapes(1)
    else:
        # bukan gambar: (grup lalu) salin dan tempel sebagai gambar
        (shapes(1) if shapes.Count == 1 else shapes.Group()).Copy()
        picture = _paste_picture(slide)
    order = ui.ask("Enter the order number for this object:", "Order Number")
    if not order:
        return
    name = ("#picturefull" if full else "#picture") + order
    picture.Name = name
    app.ActivePresentation.Save()
    ui.info(f"Object processed and renamed to '{name}'. Presentation saved.")


def identify_picture_full(app, ui):
    identify_picture(app, ui, full=True)


def remove_identifier(app, ui):
    sel = _selection(app)
    if sel.Type != SEL_SHAPES:
        raise UserError("Please select an object first.")
    shp = sel.ShapeRange(1)
    old = shp.Name
    shp.Name = old.replace("#", "")
    ui.info(f"Object name changed from '{old}' to '{shp.Name}'.")


def ignore_slide(app, ui):
    slide = current_slide(app)
    new, msg = add_ignore(notes_text(slide))
    if new is not None:
        set_notes(slide, new)
    ui.info(msg)


def view_nips(app, ui):
    names = penyusun(notes_text(current_slide(app)))
    ui.info("Penyusun:\n" + names if names else "Tidak terdapat penyusun pada slide ini.")


def add_nip_action(app, ui):
    slide = current_slide(app)
    nip = ui.ask("Enter NIP to add:")
    if not nip:
        return
    new, msg = add_nip(notes_text(slide), nip)
    if new is not None:
        set_notes(slide, new)
    ui.info(msg)


def remove_nip_action(app, ui):
    slide = current_slide(app)
    nip = ui.ask("Enter full NIP to remove:")
    if not nip:
        return
    new, msg = remove_nip(notes_text(slide), nip)
    if new is not None:
        set_notes(slide, new)
    ui.info(msg)


def collect_shapes(shapes) -> list:
    out = []
    for i in range(1, shapes.Count + 1):
        shp = shapes(i)
        out.append(shp)
        if shp.Type == MSO_GROUP:
            out += collect_shapes(shp.GroupItems)
    return out


def auto_tagging(app, ui):
    """Tagging seluruh presentasi (port "AI Tagging" VBA): gambar -> #picture{n}, teks tepat di atasnya ->
    #textbox{n}, judul -> #title, teks lain -> #keynote{n}."""
    output_ratio = 0.15
    for s in range(1, app.ActivePresentation.Slides.Count + 1):
        sld = app.ActivePresentation.Slides(s)
        if sld.Shapes.HasTitle:
            sld.Shapes.Title.Name = "#title"
        shapes = collect_shapes(sld.Shapes)
        texts = [c for c in shapes if c.HasTextFrame and c.TextFrame.HasText and c.Type != MSO_PICTURE]
        pic_index = 1
        for pic in (c for c in shapes if c.Type == MSO_PICTURE):
            top, bottom = pic.Top, pic.Top + pic.Height
            center, offset = pic.Left + pic.Width / 2, pic.Height * output_ratio
            pic.Name = f"#picture{pic_index}"
            above, max_y = None, -1.0
            for c in texts:
                c_bottom = c.Top + c.Height
                if (c_bottom >= top - offset and bottom > c_bottom
                        and abs(c.Left + c.Width / 2 - center) < pic.Width / 2 and c_bottom > max_y):
                    above, max_y = c, c_bottom
            if above is not None:
                above.Name = f"#textbox{pic_index}"
            pic_index += 1
        key_index = 1
        for c in texts:
            if not c.Name.startswith(("#title", "#textbox", "#picture")):
                c.Name = f"#keynote{key_index}"
                key_index += 1
    ui.info("Automate Tagging slide ini berhasil! Mohon dapat check kembali")


def about(app, ui):
    ui.info("Copyright © Muhammad Firza Gustama, Bank Indonesia\n\n"
            f"Current Version: {VERSION}\n"
            "- Semua fitur dipindahkan ke Python (DWP_Addin.exe)\n"
            "- Convert to Word: presentasi -> dokumen Word format laporan (tanpa LLM)\n"
            "- Add Penyusun tidak lagi menghapus catatan slide\n\n"
            "Version: 1.1\n- Fix remove notes when add Penyusun\n- Add experimental AI Tagging\n\n"
            "Version: 1.0\nAutomate Object Identifier:\n- #title\n- #keynote\n- #textbox\n- #picture\n"
            "- ::ignore::\n- ::penyusun::")


# --------------------------------------------------------------------------- Convert to Word
def report_path(pptx: Path) -> Path:
    """<deck>_laporan.docx di folder deck; nama berstempel waktu bila file lama sedang dibuka (terkunci)."""
    out = pptx.with_name(pptx.stem + "_laporan.docx")
    try:
        if out.exists():
            with open(out, "a+b"):
                pass
        return out
    except OSError:
        return pptx.with_name(f"{pptx.stem}_laporan_{time.strftime('%Y%m%d_%H%M%S')}.docx")


def convert_to_word(app, ui):
    pres = app.ActivePresentation
    if not pres.Path:
        raise UserError("Simpan presentasi terlebih dahulu, lalu klik Convert to Word lagi.")
    deck = Path(pres.FullName)
    work = LOG_DIR / time.strftime("%Y%m%d_%H%M%S")
    work.mkdir(parents=True, exist_ok=True)
    copy = work / (deck.stem + ".pptx")
    pres.SaveCopyAs(str(copy), SAVE_AS_PPTX)       # keadaan terkini, termasuk perubahan yang belum disimpan
    out = report_path(deck)
    stats = run_with_progress(ui, lambda progress: _convert(copy, out, work, progress))
    if stats is None:
        return
    if ui.quiet:
        ui.info(f"Selesai: {out} ({stats['slides']} slide)")
    else:
        os.startfile(out)


def _convert(copy: Path, out: Path, work: Path, progress) -> dict:
    import report_engine
    return report_engine.convert_report(copy, out, planner="rules", work_dir=work / "build", progress=progress,
                                        comments=True)


def run_with_progress(ui, job):
    """Jalankan job(progress) di thread dengan jendela progres kecil; hasil job, atau None bila gagal."""
    result, error = {}, []

    def target(progress):
        try:
            result["value"] = job(progress)
        except Exception as e:
            error.append(e)
            log_exception()

    if ui.quiet:
        target(lambda f, m: print(f"[{f:4.0%}] {m}"))
    else:
        import tkinter as tk
        from tkinter import ttk
        win = tk.Toplevel(ui.root())
        win.title(TITLE)
        win.attributes("-topmost", True)
        win.resizable(False, False)
        win.protocol("WM_DELETE_WINDOW", lambda: None)       # tidak bisa ditutup saat konversi berjalan
        label = tk.Label(win, text="Menyiapkan konversi...", width=52, anchor="w")
        label.pack(padx=16, pady=(14, 6))
        bar = ttk.Progressbar(win, length=360, maximum=100)
        bar.pack(padx=16, pady=(0, 16))
        state = {"f": 0.0, "m": ""}

        def poll():
            label.config(text=state["m"] or label.cget("text"))
            bar["value"] = state["f"] * 100
            if worker.is_alive():
                win.after(200, poll)
            else:
                win.destroy()
                ui.root().quit()

        def progress(f, m):
            state["f"], state["m"] = f, m

        worker = threading.Thread(target=target, args=(progress,), daemon=True)
        worker.start()
        poll()
        ui.root().mainloop()
    if error:
        ui.error(f"Konversi gagal: {error[0]}\n\nDetail: {LOG_DIR / 'addin.log'}")
        return None
    return result.get("value")


# --------------------------------------------------------------------------- main
ACTIONS = {
    "btnTitle": identify_title,
    "btnKeynote": identify_keynotes,
    "btnTextbox": identify_textbox,
    "btnPicture": identify_picture,
    "btnTextboxFull": identify_textbox_full,
    "btnPictureFull": identify_picture_full,
    "btnRemoveIdentifier": remove_identifier,
    "btnIgnore": ignore_slide,
    "btnViewPenyusun": view_nips,
    "btnAddPenyusun": add_nip_action,
    "btnRemovePenyusun": remove_nip_action,
    "btnAITagging": auto_tagging,
    "btnAbout": about,
    "btnConvertWord": convert_to_word,
}


def log_exception():
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    with open(LOG_DIR / "addin.log", "a", encoding="utf-8") as f:
        f.write(f"--- {time.strftime('%Y-%m-%d %H:%M:%S')}\n{traceback.format_exc()}\n")


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="DWP Plugin (Python)")
    ap.add_argument("action", choices=sorted(ACTIONS), help="id tombol ribbon")
    ap.add_argument("--answer", help="jawaban untuk InputBox (uji otomatis)")
    ap.add_argument("--quiet", action="store_true", help="pesan ke stdout, tanpa dialog")
    a = ap.parse_args(argv)
    ui = UI(a.quiet, a.answer)
    try:
        app = None if a.action == "btnAbout" else powerpoint()
        ACTIONS[a.action](app, ui)
        return 0
    except UserError as e:
        ui.warn(str(e))
        return 1
    except Exception as e:
        log_exception()
        ui.error(f"Terjadi kesalahan: {e}\n\nDetail: {LOG_DIR / 'addin.log'}")
        return 2


if __name__ == "__main__":
    sys.exit(main())
