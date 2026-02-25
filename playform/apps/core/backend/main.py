import os
from pathlib import Path
from dotenv import load_dotenv
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware

from db import init_db
import models
from auth import router as auth_router
from firebase import get_firestore
from seeds import seed_games

# Load environment variables from .env file
env_path = Path(__file__).parent / '.env'
load_dotenv(dotenv_path=env_path)

app = FastAPI(title="Playform API")

# Allow requests from the Vite dev server (default port 5173)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(auth_router)


@app.on_event("startup")
def on_startup():
    init_db()
    # try to seed initial games (Firestore preferred when configured)
    try:
        fs = get_firestore()
        seeded = seed_games(fs)
    except Exception:
        seeded = False


@app.get("/health")
def health():
    return {"status": "ok"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
