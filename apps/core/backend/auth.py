import os
from datetime import datetime, timedelta
from typing import Optional, Union

from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, Request, Security, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel, Field
from sqlmodel import select

from db import get_session
from firebase import get_firestore
from models import Profile, User

router = APIRouter()

SECRET_KEY = os.getenv("PLAYFORM_SECRET", "dev-secret-key")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24
N8N_WEBHOOK_URL = os.getenv("N8N_WEBHOOK_URL", "")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
security = HTTPBearer()


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None


class UserIn(BaseModel):
    username: str
    password: str


class ProfileIn(BaseModel):
    name: str
    age: int = Field(ge=18, le=50)
    bio: str


def serialize_profile(profile: Union[Profile, dict]) -> dict:
    data = profile if isinstance(profile, dict) else profile.dict()
    data["matches_count"] = data.get("matches_count", 0)
    return data


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


async def trigger_n8n_webhook(profile_name: str, username: str = "Anonymous"):
    if not N8N_WEBHOOK_URL:
        return

    import httpx

    async with httpx.AsyncClient() as client:
        try:
            await client.post(
                N8N_WEBHOOK_URL,
                json={
                    "event": "profile_created",
                    "name": profile_name,
                    "user": username,
                    "timestamp": datetime.utcnow().isoformat(),
                },
                timeout=5.0,
            )
        except Exception as exc:
            print(f"Failed to trigger n8n: {exc}")


@router.post("/auth/signup", response_model=Token)
def signup(user_in: UserIn, session=Depends(get_session)):
    statement = select(User).where(User.username == user_in.username)
    existing = session.exec(statement).first()
    if existing:
        raise HTTPException(status_code=400, detail="Username already registered")

    user = User(username=user_in.username, hashed_password=get_password_hash(user_in.password))
    session.add(user)
    session.commit()
    session.refresh(user)

    access_token = create_access_token(
        data={"sub": user.username},
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/auth/login", response_model=Token)
def login(user_in: UserIn, session=Depends(get_session)):
    statement = select(User).where(User.username == user_in.username)
    user = session.exec(statement).first()
    if not user or not verify_password(user_in.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )

    access_token = create_access_token(
        data={"sub": user.username},
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
    )
    return {"access_token": access_token, "token_type": "bearer"}


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Security(security),
    session=Depends(get_session),
):
    token = credentials.credentials
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Could not validate credentials")
        token_data = TokenData(username=username)
    except JWTError as exc:
        raise HTTPException(status_code=401, detail="Could not validate credentials") from exc

    statement = select(User).where(User.username == token_data.username)
    user = session.exec(statement).first()
    if user is None:
        raise HTTPException(status_code=401, detail="User not found")
    return user


@router.get("/api/dashboard")
def dashboard(current_user: User = Depends(get_current_user), session=Depends(get_session)):
    fs = get_firestore()
    if fs:
        profiles = []
        for doc in fs.collection("profiles").stream():
            profile = doc.to_dict()
            profile["id"] = profile.get("id", doc.id)
            profiles.append(serialize_profile(profile))
        return {
            "user": current_user.username,
            "total_profiles": len(profiles),
            "profiles": profiles,
        }

    profiles = session.exec(select(Profile)).all()
    return {
        "user": current_user.username,
        "total_profiles": len(profiles),
        "profiles": [serialize_profile(profile) for profile in profiles],
    }


@router.get("/api/users")
def list_users(current_user: User = Depends(get_current_user), session=Depends(get_session)):
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Admin only")

    users = session.exec(select(User).where(User.is_admin == False)).all()
    return [{"id": user.id, "username": user.username} for user in users]


@router.get("/api/profiles")
def list_profiles_public(session=Depends(get_session)):
    fs = get_firestore()
    if fs:
        profiles = []
        for doc in fs.collection("profiles").stream():
            profile = doc.to_dict()
            profile["id"] = profile.get("id", doc.id)
            profiles.append(serialize_profile(profile))
        return profiles

    profiles = session.exec(select(Profile)).all()
    return [serialize_profile(profile) for profile in profiles]


@router.post("/api/profiles")
async def create_profile_public(
    profile_in: ProfileIn,
    background_tasks: BackgroundTasks,
    request: Request,
    session=Depends(get_session),
):
    username = "Anonymous"
    auth_header = request.headers.get("Authorization")
    if auth_header and auth_header.startswith("Bearer "):
        try:
            token = auth_header.split(" ", maxsplit=1)[1]
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            username = payload.get("sub", "Anonymous")
        except Exception:
            pass

    background_tasks.add_task(trigger_n8n_webhook, profile_in.name, username)

    fs = get_firestore()
    if fs:
        result = fs.collection("profiles").add(
            {
                "name": profile_in.name,
                "age": profile_in.age,
                "bio": profile_in.bio,
                "matches_count": 0,
            }
        )
        doc_id = result[1].id if result and len(result) > 1 else None
        return {"created": {"id": doc_id, "name": profile_in.name}}

    profile = Profile(**profile_in.dict(), matches_count=0)
    session.add(profile)
    session.commit()
    session.refresh(profile)
    return {"created": serialize_profile(profile)}


@router.delete("/api/profiles/{profile_id}")
def delete_profile(profile_id: int, session=Depends(get_session)):
    profile = session.get(Profile, profile_id)
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")

    session.delete(profile)
    session.commit()
    return {"deleted": profile_id}
