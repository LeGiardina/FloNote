from fastapi import FastAPI, APIRouter
from fastapi.staticfiles import StaticFiles
from starlette.responses import FileResponse, JSONResponse
from pathlib import Path
import os

app = FastAPI(title="FloNote API", docs_url="/docs", redoc_url="/redoc")

api = APIRouter(prefix="/api")

@api.get("/health")
async def health():
    return {"ok": True, "service": "FloNote", "version": "1.0.0"}

# Example endpoint to show structure is working
@api.get("/templates")
async def templates():
    return [{"id": 1, "name": "SOAP Note"}, {"id": 2, "name": "Assessment/Plan"}]

app.include_router(api)

# --- Static SPA mounting ---
# Expect frontend build to be copied to /app/public during deploy (Dockerfile does this).
PUBLIC_DIR = Path(__file__).resolve().parent / "public"
if PUBLIC_DIR.exists():
    # Serve static assets and index.html for client-side routing
    app.mount("/assets", StaticFiles(directory=PUBLIC_DIR / "assets"), name="assets")

    @app.get("/")
    async def index():
        return FileResponse(PUBLIC_DIR / "index.html")

    @app.get("/{full_path:path}")
    async def spa_fallback(full_path: str):
        index_file = PUBLIC_DIR / "index.html"
        if index_file.exists():
            return FileResponse(index_file)
        return JSONResponse({"detail": "Not Found"}, status_code=404)
else:
    @app.get("/")
    async def not_built():
        return JSONResponse({"detail": "Frontend not built yet. Build Vite and copy to backend/app/public."}, status_code=503)
