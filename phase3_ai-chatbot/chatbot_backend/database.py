import os
from sqlmodel import create_engine, SQLModel
from dotenv import load_dotenv

load_dotenv()

# Use SQLite as default for local development
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./chatbot.db")

# Handle SQLite connection args
connect_args = {}
if DATABASE_URL.startswith("sqlite"):
    connect_args = {"check_same_thread": False}

engine_kwargs = {}
if not DATABASE_URL.startswith("sqlite"):
    # For PostgreSQL (Neon serverless): recycle stale connections and enable pre-ping
    # to handle dropped SSL connections after idle periods
    engine_kwargs = {
        "pool_recycle": 300,
        "pool_pre_ping": True,
        "pool_size": 5,
        "max_overflow": 10,
    }

engine = create_engine(DATABASE_URL, connect_args=connect_args, **engine_kwargs)

def init_db():
    """Initialize database tables"""
    # Import models to register them with SQLModel metadata
    try:
        from chatbot_backend.models import Task, Conversation, Message
    except ImportError:
        from models import Task, Conversation, Message
    SQLModel.metadata.create_all(engine)

def get_engine():
    return engine
