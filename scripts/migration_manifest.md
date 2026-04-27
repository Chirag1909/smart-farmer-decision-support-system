# Migration Manifest (Non-Destructive)

This restructure was performed in copy-first mode. Original files remain in place.

## Backend
- Copied `backend/routers/*.py` -> `backend/app/routes/`
- Copied `backend/services/*.py` -> `backend/app/services/`
- Added new entrypoint: `backend/app/main.py`
- Kept legacy entrypoint: `backend/main.py` (now imports `backend.app.main:app`)
- Copied Flask modules `application/{routes,services,models,templates,static}` -> `backend/app/flask_legacy/`
- Added Flask compatibility entrypoint: `backend/app/flask_legacy/main.py`

## Frontend
- Copied `web_app/frontend/public/*` -> `frontend/public/`
- Copied `web_app/frontend/src/*` -> `frontend/src/`
- Copied `web_app/frontend/package.json` -> `frontend/package.json`
- Added `frontend/src/config.js` and `frontend/.env` for env-based API URL

## Data
- Copied datasets from:
  - `processed_data/`
  - `application/processed_data/`
- Destination: `data/` (copy only, originals untouched)

## Compatibility
- Existing folders like `application/`, `web_app/`, `backend/routers`, `backend/services` were preserved.
- No deletions were performed.

## Inventory Snapshot
- `backend/`: 50 files
- `frontend/`: 13 files
- `data/`: 78 files
- `notebooks/`: 7 files
- `scripts/`: 1 file
- Legacy preserved: `application/` (67 files), `web_app/` (36 files)
