# Changelog

## 1.4.0 — work-in-progress checkpoint

Partial code published for continued development. Known issues: STATUS.md.

## 1.3.0 — work-in-progress checkpoint

Partial code published for continued development. Known issues: STATUS.md.

## 1.2.0 — work-in-progress checkpoint

Partial code published for continued development. Known issues: STATUS.md.

## 1.1.0 — work-in-progress checkpoint

Partial code published for continued development. Known issues: STATUS.md.

## 1.0.0 — work-in-progress checkpoint

Partial code published for continued development. Known issues: STATUS.md.

### Completed

- **project-init**: FastAPI + React skeleton with health endpoint and API proxy
  - Backend runs on port 8000 (FastAPI + Uvicorn)
  - Frontend runs on port 3000 (React + Vite)
  - `/health` endpoint returns 200 with service status
  - Frontend proxies `/health` and `/api/*` to backend
  - Basic test coverage for health and analyze endpoints
