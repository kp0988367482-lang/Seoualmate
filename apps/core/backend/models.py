from typing import Optional
from sqlmodel import SQLModel, Field


class Game(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str


class Profile(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    age: int = Field(ge=18, le=50)
    bio: str
    matches_count: int = Field(default=0)
    user_id: Optional[int] = Field(foreign_key="user.id")


class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(index=True)
    hashed_password: str
    is_admin: bool = Field(default=False)
