# tensor-lab-145 — Ryan Vo

> Work in progress. This checkpoint may be incomplete or fail tests. See PLAN.md and STATUS.md before use.

## Quick Start

### Backend
```bash
cd backend
python3 -m venv venv
./venv/bin/pip install -r requirements.txt
./venv/bin/python main.py
# Runs on http://localhost:8000
```

### Frontend
```bash
cd frontend
npm install
npm run dev
# Runs on http://localhost:3000, proxies /api and /health to backend
```

### Test Backend
```bash
cd backend
./venv/bin/python -m pytest test_health.py -v
```

## API Endpoints

- `GET /health` — Health check, returns `{"status":"ok","service":"tensor-lab-145"}`
- `POST /api/analyze` — Source code analysis (stub, returns empty arrays)

## Roadmap

See PLAN.md for current and planned features.

Maintainer: Ryan Vo <ryandtvo@gmail.com>
