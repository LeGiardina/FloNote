# FloNote V2 — Clinical Autofill (Full‑Stack)

Light, professional, and EMR‑ready clinical note assistant. Dictate → transcribe → structure → export (FHIR/CCDA).

## Features
- 🎤 **Mic capture** with browser MediaRecorder
- 🧠 **LLM extraction** (ChatGPT) → SOAP/H&P/Progress sections
- 🧩 **Condition‑aware templates** (COPD, DM2, CHF, Asthma)
- 📦 **Export**: FHIR Bundle (JSON) & CCDA (XML)
- 🖥️ **Sleek UI**: light theme, responsive, drag‑and‑drop reorder
- 🔐 Ready for SSO & role‑based auth (hooks in code)

## Quick Start (Local)
```bash
python -m venv .venv && source .venv/bin/activate   # (Windows: .venv\Scripts\activate)
pip install -r requirements.txt

# set OpenAI key
export OPENAI_API_KEY=sk-...                         # (Windows PowerShell: $env:OPENAI_API_KEY="...")

# run api
uvicorn backend.app:app --reload
```

Open `public/index.html` in your browser for the landing/UX. API defaults to `http://localhost:8000`.

## Deploy to Render
- **Build command:** `pip install -r requirements.txt`
- **Start command:** `uvicorn backend.app:app --host 0.0.0.0 --port $PORT`
- **Env:** `OPENAI_API_KEY` (required for live extraction)

## Endpoints
- `POST /api/extract` → `{ transcript, demographics?, problems? }` → structured note
- `POST /api/export/fhir` → FHIR Bundle (JSON)
- `POST /api/export/ccda` → CCDA (XML)
- `GET /api/templates` / `POST /api/templates` → manage templates

## Notes
- This sample uses OpenAI's `Responses` API format when available, and falls back to a rule‑based parser if no key is present (for demos).
- Replace stub auth with your SSO/IDP (Okta/Auth0) when going live.