# CLAUDE.md

POC "PPT to Word Convert" for DWP. Setup, run, flow and API are in [README.md](README.md); this file only lists the rules and pitfalls that are not visible from the code.

## Secrets

- Never commit `backend/.env` (Bedrock key) or `frontend/.env.development` (DWP config). Both are git-ignored; keep it that way.
- Never print the value of `AWS_BEARER_TOKEN_BEDROCK`. `backend/.env.example` stays an empty template.

## Repos

- Push only to this repo (`mfirzagustama/dwp-ppt-to-word`). Never push to `new-dwp`: that is the live DWP frontend.
- `frontend/` is a copy of `new-dwp`. Change only the POC files (`src/v2/views/poc`, `src/v2/components/poc`, `src/v2/poc`) and the existing POC-mode hooks (`App.vue`, `main.ts`, `CryptoHelper.js`, `Router.ts`, `vue.config.js`, `.env.poc`). Leave the rest of the DWP code as it is.
- `npm install` in `frontend/` can add `lefthook.yml` at the repo root and `.git/hooks/prepare-commit-msg`. Delete both; do not commit them.

## Backend

- Python 3.13 only: `py -3.13 -m venv .venv`. Never run `python -m venv .venv` over the existing venv with another version (breaks lxml: `cannot import name 'etree'`). Rebuild with `py -3.13 -m venv --clear .venv` and reinstall `backend/requirements.txt`.
- Keep `extra_body={"anthropic_version": BEDROCK_API_VERSION}` in `bedrock_llm.py`. Without it, anthropic SDK 2.x sends a newer API version that Bedrock rejects for Opus 4.5 / 4.6.
- Model: `BEDROCK_MODEL` in `backend/.env` (now `global.anthropic.claude-opus-4-5-20251101-v1:0`, region `ap-southeast-3`). Sonnet 4.6 also works; Opus 4.7 and newer return 403 for this account.
- Only the Full AI path (`book_engine.convert_book`) is kept. The rules-based report engine and older experiments were removed on purpose; do not bring them back.
- Slide renders: PowerPoint on Windows, LibreOffice + PyMuPDF on macOS / Linux. The LibreOffice path has not been tested on a Mac yet.

## Before committing

```
python -m unittest discover backend/tests                                  # no real LLM calls
cd frontend && npx eslint --fix --ext .ts,.vue src/v2/poc src/v2/views/poc src/v2/components/poc
```

Source files in `frontend/` use CRLF line endings; keep them.
