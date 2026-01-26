import pytest
from fastapi.testclient import TestClient
from sqlmodel import create_engine, Session, SQLModel
import os

# Set dummy environment variables before importing the app
os.environ["DATABASE_URL"] = "sqlite:///./dummy_for_import.db"
os.environ["OPENAI_API_KEY"] = "dummy_key"

from chatbot_backend.main import app
from chatbot_backend.database import engine as main_engine


# Use an in-memory SQLite database for testing
DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

# Dependency override for the database engine
def override_get_engine():
    return engine

# This is a bit of a hack to replace the engine. 
# In a real app, the dependency injection would be more explicit.
# For now, we are directly overriding the engine in the modules that use it.
from chatbot_backend import database, main, tools

database.engine = engine
main.engine = engine
tools.task_tools.engine = engine

@pytest.fixture(name="session")
def session_fixture():
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session
    SQLModel.metadata.drop_all(engine)

@pytest.fixture(name="client")
def client_fixture(session: Session):
    # The app is imported from main, and its dependencies should be patched.
    client = TestClient(app)
    yield client


def test_chat_add_task(client: TestClient, session: Session):
    """
    Tests the /api/{user_id}/chat endpoint for adding a task.
    This test currently validates the MOCKED logic in main.py.
    """
    user_id = "testuser"
    message = "add task write integration test"
    
    # 1. Send the chat message to the API
    response = client.post(
        f"/api/{user_id}/chat",
        json={"message": message}
    )
    
    # 2. Check the API response
    assert response.status_code == 200
    data = response.json()
    assert "conversation_id" in data
    assert "I've added the task" in data["response"]
    assert "write integration test" in data["response"]
    assert len(data["tool_calls"]) == 1
    assert data["tool_calls"][0]["name"] == "add_task"
    
    # 3. Verify the database state
    from chatbot_backend.models import Task, Conversation, Message
    
    # Verify a Task was created
    tasks = session.query(Task).all()
    assert len(tasks) == 1
    task = tasks[0]
    assert task.user_id == user_id
    assert task.title == "write integration test"
    
    # Verify a Conversation was created
    conversations = session.query(Conversation).all()
    assert len(conversations) == 1
    assert conversations[0].user_id == user_id
    
    # Verify two Messages were created (user and assistant)
    messages = session.query(Message).all()
    assert len(messages) == 2
    user_msg = next((m for m in messages if m.role == 'user'), None)
    assistant_msg = next((m for m in messages if m.role == 'assistant'), None)
    
    assert user_msg is not None
    assert user_msg.content == message
    
    assert assistant_msg is not None
    assert "I've added the task" in assistant_msg.content
