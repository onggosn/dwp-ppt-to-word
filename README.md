# dwp-ppt-word

Proof of concept: **PPT to Word Convert** for Digital Workplace (DWP).

A Bank Indonesia RDG deck (PowerPoint) is turned into a condensed Word **book** by AI (Claude on Amazon Bedrock). The Word file has review comments by "Digital Workplace" on the parts a person should check. The page for it lives inside the real DWP frontend (a copy of `new-dwp`), following the Sprint 18 design.

```
frontend/  (DWP, Vue 3 + Vuetify)          backend/  (Flask, Python)
/app/v2/ppt-to-word  ── /poc-api/* ──────▶  app.py ─▶ book_engine ─▶ Word (.docx)
                        (dev proxy)                    Claude on Bedrock
```

## Layout

| Path | Purpose |
|---|---|
| `backend/app.py` | POC API: upload / replace PPT, conversion progress, Word download, final PDF |
| `backend/book_engine.py` | Full AI conversion: outline, per-slide writing, number check; CLI |
| `backend/book_writer.py` | Book format for Word and HTML |
| `backend/slide_reader.py` | Reads slide elements with coordinates; renders slides (PowerPoint or LibreOffice) |
| `backend/llm.py`, `backend/bedrock_llm.py` | LLM calls (Bedrock; Ollama optional) |
| `backend/docx_common.py` | Shared Word helpers: template, styles, review comments |
| `backend/templates/` | Word template |
| `backend/tests/` | Tests (no real LLM calls) |
| `frontend/` | Copy of the DWP frontend (`new-dwp`) with the POC page and POC mode |
| `samples/` | Sample decks and the example books the format follows |

## Setup

Backend (Python 3.13; only once, on a fresh checkout):

```
py -3.13 -m venv .venv
.venv\Scripts\pip install -r backend\requirements.txt
copy backend\.env.example backend\.env      # then fill in AWS_BEARER_TOKEN_BEDROCK
```

Do not run `python -m venv .venv` over an existing `.venv` with another Python version: the installed packages are built for 3.13 and stop loading (`cannot import name 'etree' from 'lxml'`). To rebuild it, use `py -3.13 -m venv --clear .venv` and install the requirements again.

Frontend (Node 18+). It also needs `frontend/.env.development` from the DWP team (not in git); `.env.poc` only overrides a few values.

```
cd frontend
npm install
```

Slide renders use Microsoft PowerPoint on Windows, or LibreOffice (`soffice`) plus PyMuPDF elsewhere. Without either, the original images in the PPTX are used.

## Run

```
python backend/app.py                                  # API on http://localhost:5003
npm --prefix frontend run serve-poc -- --port 8090    # http://localhost:8090/app/v2/ppt-to-word
```

Both are also in `.claude/launch.json` (`backend`, `frontend`). POC mode skips DWP's SSO, answers DWP middleware calls with mock data, and proxies `/poc-api/*` to the backend. See [frontend/src/v2/poc/README.md](frontend/src/v2/poc/README.md).

## Flow

### Page and API

What happens from the page to the Word file (`frontend/src/v2/views/poc/PptToWordView.vue` and `backend/app.py`).

```mermaid
flowchart TD
    start([User opens the PPT to Word page]) --> load["Frontend: GET /documents/:id"]
    load --> hasPpt{PPT uploaded?}
    hasPpt -- no --> pick[User drops or browses a .pptx]
    pick --> fcheck{"Frontend check: access, .pptx, max 150MB"}
    fcheck -- fail --> modal[Error modal] --> pick
    fcheck -- ok --> upload["POST /documents/:id/ppt"]
    upload --> bcheck{"Backend check: .pptx, max 150MB, readable, has slides"}
    bcheck -- fail --> modal
    bcheck -- ok --> save["Save PPT, delete the previous run, status = converting"]
    save --> thread["Background thread: book_engine.convert_book"]
    save --> poll
    hasPpt -- yes --> poll{Conversion status?}
    thread -. "progress callback updates state.json" .-> poll
    poll -- converting --> progress["Show steps, slide counter, ETA; poll again after 2 s"] --> poll
    poll -- error --> failed[Show the error] --> replace
    poll -- complete --> ready["Notification: Word File is Ready"]
    ready --> download["GET /documents/:id/word: Word with review comments"]
    download --> revise[User checks the comments and revises in Word, exports PDF]
    revise --> pdf["POST /documents/:id/final-pdf"] --> done([Status: Completed])
    ready -. Replace PPT .-> replace["Replace dialog and confirm; warns if the Word file was downloaded"]
    replace --> upload
```

### Conversion engine

`book_engine.convert_book`, which runs in the background thread above.

```mermaid
flowchart TD
    s([convert_book]) --> pp{PowerPoint available?}
    pp -- "yes (Windows)" --> rpp[Render slides with PowerPoint] --> read
    pp -- no --> lo{"LibreOffice and PyMuPDF available?"}
    lo -- "yes (macOS / Linux)" --> rlo["LibreOffice: PPTX to PDF, PyMuPDF: PDF page to PNG"] --> same{"PDF pages = slides?"}
    same -- yes --> read
    same -- no --> orig
    lo -- no --> orig[Use the original images inside the PPTX] --> read
    read["Read slide elements: text, tables, pictures, with coordinates"] --> outline["AI: book outline from the whole deck, text only"]
    outline --> ok1{Valid answer?}
    ok1 -- "no, also after 1 fix attempt" --> fail([Conversion error])
    ok1 -- yes --> items["Per slide, 4 in parallel: AI writes a topic box or text, with the slide image"]
    items --> ok2{Valid answer?}
    ok2 -- yes --> nums
    ok2 -- "no, also after 1 fix attempt" --> fb["Fallback: slide title and whole slide image, plus a warning"] --> nums
    nums{"Numbers in the AI text that are not in the slide text?"}
    nums -- no --> write
    nums -- yes --> verify[AI checks those numbers against the slide image] --> verdict{Verdict}
    verdict -- sure --> write
    verdict -- "unsure / absent" --> flag[Mark the number for a comment] --> write
    write["Write Word: chapters, sections, topic boxes, charts cropped from the render"] --> comments["Add Word comments by Digital Workplace: flagged numbers and warnings"]
    comments --> e([Word file ready])
```

Every AI call (outline, per slide, number check) looks in `backend/work/book_cache` first. The answer is validated (JSON shape, slide numbers and element ids that exist on the slide, required fields, figure and caption limits), and an invalid answer gets one fix attempt with the errors sent back to the AI.

## How the conversion works

`book_engine.convert_book` (also a CLI):

1. **Render**: every slide is rendered to PNG, with PowerPoint on Windows or LibreOffice + PyMuPDF on macOS / Linux. With neither, the original images in the PPTX are used.
2. **Outline**: one text-only AI call over the whole deck picks the book title, chapters and sections, and which slides go where. Each slide becomes a `topic` box (key message, chart cropped from the render, bullets) or near-verbatim `text`. Cover, agenda, dividers and appendix are left out.
3. **Per slide**: one AI call with the slide render and its elements. The AI only names which elements form the chart area; images are cropped from the render, so charts are never redrawn.
4. **Number check**: numbers in the AI text that are not in the slide text are checked against the slide image. Uncertain numbers get a Word comment by "Digital Workplace".

```
python backend/book_engine.py "samples/rdgb-maret-2026/DKEM RDGB Maret 2026_06_Materi Hari Kedua_afterRDG.pptx" -o backend/work/buku.docx
```

AI answers are cached in `backend/work/book_cache`, so re-runs only call the AI for changed slides. The model is `BEDROCK_MODEL` in `backend/.env`.

## API

- `GET /api/poc/documents/<id>`: PPT, conversion progress (steps, slide counter, AI slide counter, ETA), Word and final PDF.
- `POST /api/poc/documents/<id>/ppt` (multipart `file`): upload or replace the PPT (`.pptx`, max 150MB) and start converting. A replaced PPT and its Word file are deleted.
- `GET /api/poc/documents/<id>/word`: the Word file with review comments.
- `POST /api/poc/documents/<id>/final-pdf` (multipart `file`): the final PDF, after the Word file exists.
- `POST /api/poc/documents/<id>/reset`: clear everything (demo).

State is kept in `backend/work/poc/<id>/state.json`, so it survives a restart. A conversion that was running when the server stopped is marked failed.

## Tests

```
python -m unittest discover backend/tests
```

The older experiments (rules-based report engine, `/dwp` editor, PowerPoint add-in, YOLO layout models) were removed from this branch; they remain in git history.
