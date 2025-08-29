# FloNote Ready (FastAPI + Vite React)

This package serves your SPA at `/` and your API at `/api/*`. It prevents the `{"detail":"Not Found"}` white screen by ensuring the frontend build is mounted and a SPA fallback is provided.

## Quickstart with Docker (recommended)
```bash
docker build -t flonote-ready .
docker run -p 8000:8000 -e OPENAI_API_KEY=sk-... flonote-ready
# Open http://localhost:8000
# API docs: http://localhost:8000/docs
```
If your platform requires a `PORT` env var, it's already honored.

## Without Docker
```bash
# 1) Build frontend
cd frontend
npm ci
npm run build

# 2) Copy build to backend/app/public
mkdir -p ../backend/app/public
cp -r dist/* ../backend/app/public/

# 3) Run the API
cd ../backend
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --host 0.0.0.0 --port 8000

# Visit http://localhost:8000/
```

## Structure
```
backend/
  app/
    main.py           # FastAPI app; mounts SPA + /api routes
    public/           # (filled by Vite build)
  requirements.txt

frontend/
  index.html
  src/
    main.jsx
    App.jsx
  package.json
  vite.config.js
```

## Notes
- Client code calls `/api/health` to verify connectivity.
- SPA fallback serves `index.html` for unknown paths (client-side routing).
- If `/` returns `Frontend not built yet`, you skipped the build/copy step.
