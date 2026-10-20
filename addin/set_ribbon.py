"""Pasang ribbon addin/customUI14.xml ke sebuah .ppam / .pptm (isi lain, termasuk VBA, tidak diubah).

    python addin/set_ribbon.py DWP_Plugin.ppam              # ditimpa di tempat
    python addin/set_ribbon.py DWP_Plugin.pptm -o out.pptm
"""
import argparse
import shutil
import tempfile
import zipfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
PART = "customUI/customUI14.xml"
REL_TYPE = "http://schemas.microsoft.com/office/2007/relationships/ui/extensibility"


def set_ribbon(src: Path, out: Path, ribbon: Path = HERE / "customUI14.xml") -> Path:
    with zipfile.ZipFile(src) as z:
        items = {i.filename: z.read(i.filename) for i in z.infolist()}
    items[PART] = ribbon.read_bytes()
    rels = items["_rels/.rels"].decode("utf-8")
    if REL_TYPE not in rels:     # file tanpa ribbon: tambahkan relasi ke customUI
        rels = rels.replace("</Relationships>",
                            f'<Relationship Id="RDwpRibbon" Type="{REL_TYPE}" Target="{PART}"/></Relationships>')
        items["_rels/.rels"] = rels.encode("utf-8")
    with tempfile.NamedTemporaryFile(delete=False, suffix=src.suffix) as tmp:
        with zipfile.ZipFile(tmp, "w", zipfile.ZIP_DEFLATED) as z:
            for name, data in items.items():
                z.writestr(name, data)
    shutil.move(tmp.name, out)
    return out


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="Pasang ribbon DWP Plugin ke .ppam/.pptm")
    ap.add_argument("file")
    ap.add_argument("-o", "--output", help="default: timpa file asal")
    a = ap.parse_args()
    print(set_ribbon(Path(a.file), Path(a.output or a.file)))
