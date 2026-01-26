from typing import Optional, List
from datetime import datetime
from sqlmodel import Field, SQLModel, JSON
from sqlalchemy import Column


class UserBase(SQLModel):
    username: str = Field(unique=True, index=True)
    hashed_password: str

class User(UserBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

class UserCreate(UserBase):
    password: str

class UserRead(UserBase):
    id: int

class UserUpdate(SQLModel):
    username: Optional[str] = None
    hashed_password: Optional[str] = None

class Token(SQLModel):
    access_token: str
    token_type: str

class TokenData(SQLModel):
    username: Optional[str] = None

class TodoBase(SQLModel):
    title: str
    description: Optional[str] = None
    completed: bool = False
    priority: Optional[str] = None
    tags: Optional[List[str]] = Field(default=None, sa_column=Column(JSON))
    due_date: Optional[datetime] = None
    recurring_interval: Optional[str] = None
    user_id: Optional[int] = Field(default=None, foreign_key="user.id")


class Todo(TodoBase, table=True):
    id: int = Field(default=None, primary_key=True)


class TodoCreate(TodoBase):
    due_date: Optional[datetime] = None
    recurring_interval: Optional[str] = None


class TodoUpdate(SQLModel):
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None
    priority: Optional[str] = None
    tags: Optional[List[str]] = None
    due_date: Optional[datetime] = None
    recurring_interval: Optional[str] = None