from sqlmodel import Session, select

from db import engine
from models import Profile

SAMPLE_PROFILES = [
    {"name": "小美", "age": 25, "bio": "AI 工程師，喜歡咖啡、旅行與慢跑。"},
    {"name": "阿俊", "age": 28, "bio": "健身教練，熱愛戶外活動與自煮生活。"},
    {"name": "小芳", "age": 23, "bio": "平面設計師，愛畫畫、看電影和逛展。"},
    {"name": "大衛", "age": 30, "bio": "產品經理，喜歡閱讀、烹飪與城市散步。"},
    {"name": "小玲", "age": 26, "bio": "行銷專員，熱衷音樂、美食和週末小旅行。"},
]


def seed_profiles(firestore_client=None):
    if firestore_client:
        collection = firestore_client.collection("profiles")
        docs = list(collection.get())
        if docs:
            return False

        for profile in SAMPLE_PROFILES:
            collection.add({**profile, "matches_count": 0})
        return True

    with Session(engine) as session:
        existing = session.exec(select(Profile)).first()
        if existing:
            return False

        for profile in SAMPLE_PROFILES:
            session.add(
                Profile(
                    name=profile["name"],
                    age=profile["age"],
                    bio=profile["bio"],
                    matches_count=0,
                )
            )
        session.commit()

    return True
