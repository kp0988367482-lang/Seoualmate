from sqlmodel import Session, select
from db import engine
from models import Game

SAMPLE_GAMES = [
    {"name": "Chess"},
    {"name": "Tetris"},
    {"name": "Example Game"},
]


def seed_games(firestore_client=None):
    """Seed initial games into Firestore if provided, otherwise into SQLite."""
    if firestore_client:
        col = firestore_client.collection("games")
        docs = list(col.get())
        if len(docs) == 0:
            for g in SAMPLE_GAMES:
                col.add(g)
            return True
        return False

    # SQLite path
    with Session(engine) as session:
        existing = session.exec(select(Game)).first()
        if existing:
            return False
        for g in SAMPLE_GAMES:
            session.add(Game(name=g["name"]))
        session.commit()
    return True
