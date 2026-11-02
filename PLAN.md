# Product development plan

Each round completes one feature or repair. Future items are planned, not implemented claims.

## Current round

project-init

## Roadmap

### project-init — Project initialization with FastAPI + React skeleton

Status: done

Acceptance:
- FastAPI backend runs on port 8000
- React frontend runs on port 3000
- Health endpoint returns 200
- Frontend can call backend API

Implementation: `backend/main.py`, `backend/requirements.txt`, `frontend/package.json`, `frontend/vite.config.js`, `frontend/index.html`, `frontend/src/main.jsx`, `frontend/src/App.jsx`

Tests: `backend/test_health.py`

### cli-generation — CLI generation from source code analysis

Status: planned

Acceptance:
- Parse target application source code
- Generate CLI commands for discovered functions
- Validate generated CLI executes correctly

### code-analysis — Source code analysis engine

Status: planned

Acceptance:
- Extract function signatures and types
- Identify entry points and commands
- Generate command metadata

