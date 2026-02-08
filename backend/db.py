import os
from sqlmodel import create_engine, Session, SQLModel

# Use SQLite as default for local development
DATABASE_URL = os.environ.get("DATABASE_URL", "sqlite:///./todo.db")

# Handle SQLite connection args
connect_args = {}
if DATABASE_URL.startswith("sqlite"):
    connect_args = {"check_same_thread": False}

engine = create_engine(DATABASE_URL, connect_args=connect_args)

def init_db():
    """Initialize database tables"""
    # Import models to register them with SQLModel metadata
    try:
        from .models import User, Todo
    except ImportError:
        from models import User, Todo
    SQLModel.metadata.create_all(engine)

def get_db_session():
    with Session(engine) as session:
        yield session
