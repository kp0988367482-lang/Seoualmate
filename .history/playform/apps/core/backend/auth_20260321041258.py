ㄧimport os
from datetime import datetime, timedelta
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Security, status, BackgroundTasks, Request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel
from sqlmodel import select

from db import get_session
from models import User, Game, Profile
from firebase import get_firestore

router = APIRouter()

# secret should be set via env in production
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


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def trigger_n8n_webhook(game_name: str, username: str = "Anonymous"):
    """Internal helper to trigger n8n workflow asynchronously."""
    if not N8N_WEBHOOK_URL:
        return
    import httpx
    async with httpx.AsyncClient() as client:
        try:
            await client.post(N8N_WEBHOOK_URL, json={
                "event": "game_created",
                "name": game_name,
                "user": username,
                "timestamp": datetime.utcnow().isoformat()
            }, timeout=5.0)
        except Exception as e:
            print(f"Failed to trigger n8n: {e}")


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
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/auth/login", response_model=Token)
def login(user_in: UserIn, session=Depends(get_session)):
    statement = select(User).where(User.username == user_in.username)
    user = session.exec(statement).first()
    if not user or not verify_password(user_in.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password"
        )
    access_token = create_access_token(
        data={"sub": user.username},
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    return {"access_token": access_token, "token_type": "bearer"}


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Security(security),
    session=Depends(get_session)
):
    token = credentials.credentials
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Could not validate credentials")
        token_data = TokenData(username=username)
    except JWTError:
        raise HTTPException(status_code=401, detail="Could not validate credentials")
    statement = select(User).where(User.username == token_data.username)
    user = session.exec(statement).first()
    if user is None:
        raise HTTPException(status_code=401, detail="User not found")
    return user


@router.get("/api/dashboard")
def dashboard(current_user: User = Depends(get_current_user), session=Depends(get_session)):
    """Protected dashboard — returns game stats for the logged-in user."""
    fs = get_firestore()
    if fs:
        games_col = fs.collection("games")
        games_docs = games_col.stream()
        games = []
        for doc in games_docs:
            d = doc.to_dict()
            d["id"] = d.get("id", doc.id)
            games.append(d)
        total_games = len(games)
        return {"user": current_user.username, "total_games": total_games, "games": games}

    # Fallback to SQLite
    profiles = session.exec(select(Profile)).all()
    total_profiles = len(profiles)
    return {
        "user": current_user.username,
        "total_profiles": total_profiles,
        "profiles": [p.dict() for p in profiles],
    }


# ── Public Games API ──────────────────────────────────────────────────────────


def list_profiles_public(session=Depends(get_session)):
    """Return all profiles (public, no auth required)."""
    fs = get_firestore()
    if fs:
        profiles_col = fs.collection("profiles")
        profiles = []
        for doc in profiles_col.stream():
            d = doc.to_dict()
            d["id"] = d.get("id", doc.id)
            profiles.append(d)
        return profiles

    profiles = session.exec(select(Profile)).all()
    return [p.dict() for p in profiles]

@router.post("/api/profiles")
async def create_profile_public(
    profile_in: ProfileIn,
    background_tasks: BackgroundTasks,
    request: Request,
    session=Depends(get_session)
):
    """Create a new dating profile and trigger n8n workflow."""
    # Attempt to get username from token if present (optional)
    username = "Anonymous"
    auth_header = request.headers.get("Authorization")
    if auth_header and auth_header.startswith("Bearer "):
        try:
            token = auth_header.split(" ")[1]
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            username = payload.get("sub", "Anonymous")
        except Exception:
            pass

    background_tasks.add_task(trigger_n8n_webhook, profile_in.name, username)

    fs = get_firestore()
    if fs:
        doc_ref = fs.collection("profiles").add({
            "name": profile_in.name,
            "age": profile_in.age,
            "bio": profile_in.bio,
            "matches_count": 0
        })
        try:
            doc_id = doc_ref[1].id if doc_ref and len(doc_ref) > 1 else None
        except Exception:
            doc_id = None
        return {"created": {"id": doc_id, "name": profile_in.name}}

    profile = Profile(**profile_in.dict(), matches_count=0)
    session.add(profile)
    session.commit()
    session.refresh(profile)
    return {"created": profile.dict()}


@router.delete("/api/profiles/{profile_id}")
def delete_profile(profile_id: int, session=Depends(get_session)):
    """Delete a profile by ID."""
    profile = session.get(Profile, profile_id)
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    session.delete(profile)
    session.commit()
    return {"deleted": profile_id}
