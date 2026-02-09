from typing import Optional
from sqlmodel import Field, SQLModel, create_engine

class Task(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str
    title: str
    description: Optional[str] = None
    completed: bool = False
    created_at: str # Using str for simplicity, can be datetime
    updated_at: str # Using str for simplicity, can be datetime

class Conversation(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str
    thread_id: Optional[str] = None # Added for OpenAI Assistant API
    created_at: str
    updated_at: str

class Message(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    conversation_id: int = Field(foreign_key="conversation.id")
    user_id: str
    role: str  # "user" or "assistant"
    content: str
    created_at: str
