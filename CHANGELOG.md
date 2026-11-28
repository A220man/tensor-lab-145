# Changelog

## 1.7.0 — work-in-progress checkpoint

Partial code published for continued development. Known issues: STATUS.md.

## 1.6.0 — work-in-progress checkpoint


## 1.6.1 — CLI generation fix

- Fixed `get_click_option_name()` to properly handle `@click.option` decorators without parentheses
- Added support for extracting option names from `@click.option("--name")` and `@option("--name")` decorators
- Updated `analyze_python_file()` to include click option parameters in generated CLI commands
- All existing tests pass (2/2)

Partial code published for continued development. Known issues: STATUS.md.

## 1.5.0 — work-in-progress checkpoint

Partial code published for continued development. Known issues: STATUS.md.

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
