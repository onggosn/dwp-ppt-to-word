# dwp-ppt-word

Converts Bank Indonesia RDG board-meeting decks (PowerPoint template "1_Format RDG") into a formatted Word report, with an optional CKEditor HTML version of the same content.

The target format is `docs/test3.docx` (made from `docs/test3.pptx`). The main path is a **report engine**: geometry rules plan every slide, an LLM re-plans only the slides the rules flag as doubtful, and a deterministic writer produces the same format regardless of where the plan came from.

## How it works

```
PPTX ─ extract ─▶ rules plan ─▶ route ─▶ validate ─▶ write
        shapes    layout_engine  rules or   ids exist,   report_writer
        e1, e2…   .analyse()     LLM per    no dupes,    DOCX (+ HTML)
                                 slide      no text lost
```

1. **Extract**: every shape becomes an element with an id (`e1`, `e2`, …) and absolute coordinates; groups are flattened and off-slide elements dropped.
2. **Plan**: `layout_engine.analyse` turns geometry into a list of blocks (heading, text, table, figure, note) that only reference element ids. Each slide gets a type (cover, divider, closing, text, charts, columns, dense, infographic) and flags where the result is doubtful.
3. **Route**: the planner decides who re-plans flagged slides (see [Planners](#planners)). The LLM returns the same id-only JSON and never writes text, so numbers cannot change. Invalid LLM plans fall back to the rules plan; valid ones are cached in `work/plan_cache`.
4. **Write**: `report_writer.py` renders the plan to DOCX, and to CKEditor HTML via `--html`.

Format rules: all figures of a slide go in one image | caption table (wide figures span both columns, caption row below); body text is kept as-is, with PowerPoint bullets and numbering becoming Word lists and bold/italic kept per run. Dense infographic slides become one image, with the title and key-message lines kept as text (this needs a PowerPoint render).

## Setup

Windows with Microsoft PowerPoint installed is needed for slide renders (pictures, charts, infographics). Without it, pass `--no-render` to use the original images from the PPTX.

```
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

LLM features need `GOOGLE_API_KEY` or `GEMINI_API_KEY` in the environment. They are optional: `--planner rules` never calls an LLM.

## Usage

### Command line

```
python report_engine.py docs/test3.pptx -o work/test3_report.docx
python report_engine.py docs/test3.pptx -o work/test3_report.docx --html work/test3_report.html
python report_engine.py docs/test2.pptx -o work/test2_report.docx --planner rules    # no LLM
python report_engine.py docs/test2.pptx -o work/test2_cached.docx --planner cached  # saved LLM plans only
python report_engine.py docs/test3.pptx -o work/test3_llm.docx --planner llm        # every slide to the LLM
```

Useful options: `--slides 5,12,30` (retry only these), `--include-hidden`, `--no-render`, `--no-cache`, `--workers N` (parallel LLM calls), `--provider gemini|ollama`, `--model`.

Besides the DOCX, the engine writes `plans.json` (the plan of every slide) and `review.json` (renders and results for the review page) into the work directory.

### Planners

| Planner | Behaviour |
|---|---|
| `rules` | Rules only, no LLM. |
| `cached` | Reuses LLM plans in `work/plan_cache`; never calls the LLM. Only helps for slides planned before, byte for byte. |
| `auto` (default) | Sends dense or flagged slides to the LLM. |
| `llm` | Sends every content slide to the LLM. |

### Web app

```
python app.py        # http://localhost:5001
```

- `/` and `/dwp` have an engine selector; the report format is the default. Report jobs offer DOCX and CKEditor HTML downloads.
- `/review/<job>` shows each slide's render next to the result, with its type, plan source and flags.
- `/dwp` is the editor flow: upload a PPT, then "Konversi ke CKEditor" asks whether flagged slides are fixed manually (rules only) or automatically with the LLM. The review step lets you edit each flagged slide by hand, re-plan it with an AI prompt prefilled from its flags, mark it OK, or revert it. Fixes live in server memory and are lost on restart.

### PowerPoint add-in

`addin/` holds the DWP Plugin ribbon rewritten in Python, including a **Convert to Word** button (report engine, rules only). See [addin/README.md](addin/README.md) for build, install and project status.

## Evaluation and tests

```
python evaluate.py --gold docs/test3.docx --out work/test3_report.docx   # score vs a hand-made gold docx
python evaluate.py --silver "docs/test - Copy.pptx"                      # rules vs cached LLM plans
python -m unittest discover tests                                        # no pytest needed
```

`evaluate.py` also accepts `--plans plans.json`, `--detail` and `--json`. The tests run with rendering off, and any LLM call fails them.

## Layout

| Path | Purpose |
|---|---|
| `report_engine.py` | Extract, plan, route, validate; CLI entry point |
| `report_writer.py` | DOCX and CKEditor HTML writers (`Tee` feeds both) |
| `layout_engine.py` | Geometry rules (`analyse`, `collect`); older PPTX → DOCX/HTML path with its own CLI |
| `llm_planner.py` | One-slide LLM planner with validation and a single repair retry |
| `evaluate.py` | Scoring against gold or silver (cached LLM) results |
| `app.py`, `templates/` | Flask app; `ckeditor_flow.py` is the `/dwp` backend, `review.py` the review pages |
| `sections.json` | Section tree used to place content in the `/dwp` editor |
| `addin/` | PowerPoint add-in (Python, COM) |
| `converter.py`, `docs/` | Older Docling/LLM pipeline and sample decks (`test2.pptx`: 184 slides, `test - Copy.pptx`: 76) |
| `train/`, `yolo_extract.py`, `prepare_dataset.py` | YOLO layout experiments; dropped from the main path because they did not beat the rules enough |
