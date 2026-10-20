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

## Project status (2026-10-20)

### Built

**Report engine** (`report_engine.py`, `report_writer.py`): PPTX → Word in the report format of
`docs/test3.docx`.

- Rules plan per slide from `layout_engine.analyse`; slide types cover, divider, closing, text, charts,
  columns, dense and infographic.
- Planners:

  | Planner | What it does |
  |---|---|
  | `rules` | No LLM. The default to use, since the LLM budget is 0. |
  | `cached` | Reuses LLM plans saved in `work/plan_cache`; never calls the LLM. Only helps for slides already planned before, byte for byte. |
  | `auto` | Sends dense or flagged slides to the LLM. |
  | `llm` | Sends every content slide to the LLM. |

- Format: all figures of a slide in one image | caption table; wide figures span both columns with the caption
  below; bullets and numbering become Word lists; bold and italic are kept per word.
- Captions: all-caps labels, and bold mixed-case titles on coloured bars (e.g. "Perkembangan Loan Agreement
  Revolving"). A bar with other titles under it is a section heading, not a caption. Collage screenshots and
  stacked panel charts join their captioned figure.
- Infographics: a dense slide that the rules would split into many short labels and loose tables becomes the
  title, the key-message lines under it as text, and one full-width image. This needs a PowerPoint render.
- Output: `.docx`, optional CKEditor HTML (`--html`) with the same content, plus `plans.json` and
  `review.json`.

**Web app** (`app.py`):

- `/` and `/dwp` have an engine selector, with the report format as the default.
- Report jobs offer DOCX and CKEditor HTML downloads.
- `/review/<job>` shows each slide's render next to the result, with its slide type, plan source and flags.
- `/dwp` editor tab (`ckeditor_flow.py`): "Generate PPT" is an upload for the prototype, and the PPT tab
  always asks for it (a new upload replaces the document and its CKEditor content). "Konversi ke CKEditor"
  first asks how flagged slides are fixed: Manual (report engine rules only) or Otomatis dengan LLM
  (planner `auto`), reusing the background render; the result is mapped to the section tree and put into
  CKEditor (content max 820 px wide). The review step lists the flagged slides; each can be fixed by
  hand (edit the result in place), re-planned by the LLM with a prompt prefilled from its flags, marked OK,
  or reverted. Fixes stay in server memory; the DOCX download is the automatic result without them.

**Measurement**:

- `evaluate.py --gold G --out O` scores a result against a hand-made gold docx.
- `evaluate.py --silver DECK` scores the rules against cached LLM plans, about 30 slides of
  `docs/test - Copy.pptx`. The rules score 68.0%, up from 66.1% before the caption rule.
- `python -m unittest discover tests` (10 tests, about 1 s): test3 rules-only scores 100% against gold, the
  HTML matches the DOCX, LLM answers parse, the infographic rule and the add-in notes logic work, and any LLM
  call fails the tests.

**PowerPoint add-in** (this folder): all 13 DWP Plugin buttons in Python plus **Convert to Word**. Every button
was tested live against PowerPoint with the built exe. Convert to Word on test3 scores 100% against gold.

### Pending

- **Add-in:** build the `.ppam` (import `DWPShim.bas`, save as `.ppam`, run `set_ribbon.py`) and test it inside
  PowerPoint. The shim and the ribbon have not been run in a real add-in yet. Also confirm that the
  `FileSaveAsWordDocx` icon shows, and get the unsigned exe allowed by IT.
- **Infographic near misses:** some slides of the DWP design deck (14, 54, 83) are still partly fragmented.
  Lowering the threshold would catch them; first check that it does not catch RDG chart slides such as
  test2 slide 156.
- **More gold docx files:** only test3 (5 slides) has a hand-made gold. Gold files for dense slides, or labels
  on the review page, are needed to measure further rule changes on new decks.
- **Smaller items:**
  - "DSta"-style corner tags are written as body text.
  - Small legend labels can appear as stray text (test2 slide 96).
  - Some chart crops show a thin strip of the title bar.
  - The CKEditor HTML embeds images, so it is 63 MB for test2.
  - `/dwp` review fixes are lost on server restart and are not written back into the DOCX.
  - "Perbaiki dengan AI" on `/dwp` has only been tested without an API key (error path), not with a real LLM.
