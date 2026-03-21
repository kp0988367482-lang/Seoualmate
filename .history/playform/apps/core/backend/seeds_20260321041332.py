ㄧfrom sqlmodel import Session, select
from db import engine
from models import Profile

SAMPLE_PROFILES = [
    {"name": "小美", "age": 25, "bio": "AI工程師，喜歡咖啡和旅行"},
    {"name": "阿俊", "age": 28, "bio": "健身教練，熱愛戶外活動"},
    {"name": "小芳", "age": 23, "bio": "設計師，愛畫畫和看電影"},
    {"name": "大衛", "age": 30, "bio": "產品經理，喜歡閱讀和烹飪"},
    {"name": "小玲", "age": 26, "bio": "行銷專員，熱衷音樂和美食"},
]


def seed_profiles(firestore_client=None):
    """Seed initial dating profiles into Firestore if provided, otherwise into SQLite."""
    if firestore_client:
        col = firestore_client.collection("profiles")
        docs = list(col.get())
        if len(docs) == 0:
            for p in SAMPLE_PROFILES:
                col.add(p)
            return True
        return False

    # SQLite path
    with Session(engine) as session:
        existing = session.exec(select(Profile)).first()
        if existing:
            return False
        for p in SAMPLE_PROFILES:
            profile = Profile(
                name=p["name"],
                age=p["age"], 
                bio=p["bio"],
                matches_count=0
            )
            session.add(profile)
        session.commit()
    return True
