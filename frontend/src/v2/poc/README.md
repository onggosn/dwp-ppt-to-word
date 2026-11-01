# POC: PPT to Word Convert

Proof of concept for the Sprint 18 "PPT to Word Convert" design (Figma: Sprint Active DWP > Sprint 18 >
DWP P7 Web), running inside the real DWP shell. This folder is a copy of `new-dwp`; the conversion
backend is `backend/` in the same repo (see the root README).

## Run

From the repo root:

```
python backend/app.py                                  # http://localhost:5003 (needs backend/.env)
npm --prefix frontend run serve-poc -- --port 8090    # http://localhost:8090/app/v2/ppt-to-word
```

POC mode needs `frontend/.env.development` (from the DWP team, not in git); `.env.poc` only overrides a few values.

## What POC mode changes

- `pocMock.ts`: seeds a user (Deflin Anggita), and answers every DWP middleware call with a canned success.
  `App.vue` skips SSO, Firebase and CKEditor tokens. `CryptoHelper.js` skips request/response encryption.
- Only when `VUE_APP_POC_MOCK=true` (set by `.env.poc`). Normal modes are unchanged.
- `vue.config.js` proxies `/poc-api/*` to the backend (`POC_API_TARGET`, default `http://localhost:5003`).

## Page

`views/poc/PptToWordView.vue` with `components/poc/*`:

- PowerPoint → Word → Final PDF stepper, upload with checks (.pptx only, max 150MB).
- Conversion progress from the backend: steps, slide counter, AI slide counter, ETA; polled every 2 seconds.
- "Word File is Ready" notification, Download Word (comments by Digital Workplace).
- Replace PPT with a confirmation, which warns when the Word file was already downloaded.
- Final PDF upload.
- `?access=none` shows the "no access" case. "Reset POC demo" clears the document on the backend.
- The Content panel on the right is static (`PocContentPanel.vue`).
