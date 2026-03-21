# Playform - GitHub + Antigravity AI Automation System

🤖 **자동화된 AI SaaS 생성 및 배포 시스템**

This workspace contains a complete AI automation system with:
- `backend/` - FastAPI backend
- `frontend/` - Vite + React frontend  
- `agents/` - YouTube, SaaS, Marketing AI agents
- `main_antigravity.py` - Master orchestrator for all agents

---

## 🚀 Quick Start (5분 안에 시작하기)

Backend:

```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

Frontend:

```powershell
cd frontend
npm install
npm run dev
```

Notes:

- Backend runs on `http://127.0.0.1:8000` by default.
- Frontend Vite dev server runs on `http://localhost:5173` by default.
- The backend enables CORS for the Vite dev origin so the frontend can fetch the API during development.

Auth & DB

- Signup: `POST /auth/signup` with JSON `{ "username": "u", "password": "p" }` returns `{ access_token }`.
- Login: `POST /auth/login` with same payload returns `{ access_token }`.
- Protected dashboard: `GET /api/dashboard` requires `Authorization: Bearer <token>`.
- Database: SQLite database `playform.db` is created automatically in the backend folder on startup.

Optional: Firebase Firestore (data collection / dashboard)

- You can switch dashboard and analytics to use Firebase Firestore. The backend will prefer Firestore when credentials are provided.
- Provide credentials using one of these env vars before starting the backend:
	- `FIREBASE_SA` — filesystem path to the service account JSON file, or
	- `FIREBASE_SA_JSON` — the service account JSON as a string.

Example (PowerShell):

```powershell
$env:FIREBASE_SA = "C:\path\to\serviceAccount.json"
uvicorn main:app --reload --port 8000
```

If Firestore is available, the `/api/dashboard` endpoint will read from the `games` collection and return Firestore-stored game documents.

MCP Inspector (optional)

You can run a local MCP server to expose Playform actions to MCP Inspector (VS Code).

1. Install dependencies in the backend env:

```powershell
cd backend
\.venv\Scripts\activate
pip install -r requirements.txt
```

2. Run the MCP server (from workspace root):

```powershell
python mcp_server.py
```

3. In MCP Inspector set:
- Transport: `STDIO`
- Server Script Path: full path to `mcp_server.py`

By default the MCP tools call the local API at `http://127.0.0.1:8000` (set `PLAYFORM_API` env to override).

Install backend deps:

```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
python -c "from db import init_db; init_db()"
uvicorn main:app --reload --port 8000
```

Frontend:

```powershell
cd frontend
npm install
npm run dev
```
