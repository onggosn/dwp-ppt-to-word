"""Bangun DWP_Addin.exe (PyInstaller, satu folder) di venv terpisah yang ramping: hanya pustaka report engine,
pywin32 dan PyInstaller (venv utama berisi torch/docling yang tidak dibutuhkan add-in).

    python addin/build.py            -> dist/DWP_Addin/DWP_Addin.exe
Salin folder dist/DWP_Addin ke samping DWP_Plugin.ppam.
"""
import subprocess
import sys
import venv
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
VENV = ROOT / ".venv-addin"
PACKAGES = ["python-pptx", "python-docx", "pillow", "lxml", "pywin32", "pyinstaller"]


def main():
    py = VENV / "Scripts" / "python.exe"
    if not py.exists():
        venv.create(VENV, with_pip=True)
    subprocess.run([str(py), "-m", "pip", "install", "-q", *PACKAGES], check=True)
    subprocess.run([
        str(py), "-m", "PyInstaller", "--noconfirm", "--clean", "--onedir", "--windowed",
        "--name", "DWP_Addin", "--paths", str(ROOT),
        "--distpath", str(ROOT / "dist"), "--workpath", str(ROOT / "build" / "pyinstaller"),
        "--specpath", str(ROOT / "build"),
        "--add-data", f"{ROOT / 'docs' / 'report_template.docx'};docs",
        # LLM dan Docling tidak dipakai add-in (planner aturan saja)
        "--exclude-module", "llm_planner", "--exclude-module", "converter",
        str(ROOT / "addin" / "dwp_addin.py"),
    ], check=True, cwd=ROOT)
    print(ROOT / "dist" / "DWP_Addin" / "DWP_Addin.exe")


if __name__ == "__main__":
    sys.exit(main())
