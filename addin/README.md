# DWP Plugin 2.0 (Python)

The DWP Plugin ribbon for PowerPoint. All buttons run in Python (`dwp_addin.py`); the `.ppam` only holds one
VBA macro (`DWPShim.bas`) that starts `DWP_Addin.exe <button id>`.

Buttons: Title, Keynote, Textbox, Picture, Textbox Full, Picture Full, Remove Identifier, Ignore,
Penyusun View / Add / Remove, AI Tagging, About, and **Convert to Word** (report engine, rules only, no LLM:
writes `<deck>_laporan.docx` next to the deck and opens it in Word).

## Build

1. Exe: `python addin/build.py` → `dist/DWP_Addin/` (about 56 MB, includes Python and all libraries).
2. Add-in:
   - Open the source `.pptm` of DWP_Plugin (or a new empty presentation) and press Alt+F11.
   - Remove Module1–Module11 (no longer used), then File → Import File → `addin/DWPShim.bas`.
   - Save as *PowerPoint Add-in (.ppam)*: `DWP_Plugin.ppam`.
   - Put the ribbon in: `python addin/set_ribbon.py DWP_Plugin.ppam`.

## Install

Put these side by side in one folder:

    DWP_Plugin.ppam
    DWP_Addin\          (copy of dist\DWP_Addin)

Then in PowerPoint: File → Options → Add-ins → Manage: PowerPoint Add-ins → Add New → `DWP_Plugin.ppam`.

The exe is not code-signed; SmartScreen or antivirus may block it until IT allows it.

Logs: `%TEMP%\dwp_addin\addin.log`. Convert to Word work files: `%TEMP%\dwp_addin\<time>\`.

## Adding a button

Add the button to `customUI14.xml` with `onAction="RunAction"`, add its id to `ACTIONS` in `dwp_addin.py`,
then rebuild the exe and run `set_ribbon.py` again. No VBA change is needed.
