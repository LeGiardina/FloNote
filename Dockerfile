# ---------- build frontend ----------
FROM node:20-alpine AS webbuild
WORKDIR /web
COPY frontend/package.json frontend/package-lock.json* ./
RUN npm ci --no-audit --no-fund
COPY frontend ./
RUN npm run build

# ---------- backend ----------
FROM python:3.11-slim AS api
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app
COPY backend/requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# copy backend source
COPY backend ./

# copy built frontend into backend/app/public
COPY --from=webbuild /web/dist ./app/public

# health port; some PaaS provide PORT
ENV PORT=8000
EXPOSE 8000
CMD ["sh", "-lc", "uvicorn app.main:app --host 0.0.0.0 --port ${PORT}"]
