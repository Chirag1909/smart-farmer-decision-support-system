# Smart Farmer Decision Support System

Production-oriented repository containing legacy Flask modules, FastAPI backend modules, React frontend, datasets, and notebooks.

## Current Structure

```text
project-root/
├── backend/
│   ├── app/
│   │   ├── routes/
│   │   ├── services/
│   │   ├── models/
│   │   ├── utils/
│   │   └── main.py
│   ├── requirements.txt
│   ├── config.py
│   └── main.py
├── frontend/
│   ├── src/
│   ├── public/
│   ├── package.json
│   └── .env
├── data/
├── notebooks/
├── scripts/
├── application/        # preserved legacy Flask app
├── web_app/            # preserved legacy full-stack app
├── .env
├── .gitignore
└── docker-compose.yml
```

## Backend Run (FastAPI layout)

From `backend/`:

```bash
pip install -r requirements.txt
uvicorn app.main:app --host 0.0.0.0 --port 10000
```

## Frontend Run

From `frontend/`:

```bash
npm install
npm run build
npm start
```

## Environment Variables

Root `.env`:

```env
API_BASE_URL=http://localhost:10000
FRONTEND_API_BASE_URL=http://localhost:10000
DATABASE_URL=sqlite:///users.db
DATA_DIR=./data
```

Frontend `.env`:

```env
REACT_APP_API_BASE_URL=http://localhost:10000
```

## Deployment

- Backend start command: `uvicorn app.main:app --host 0.0.0.0 --port 10000`
- Docker compose included for containerized backend boot.
- Legacy Flask deployment files remain untouched for compatibility.
