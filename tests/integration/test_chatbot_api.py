import pytest
from fastapi.testclient import TestClient
from sqlmodel import create_engine, Session, SQLModel
from unittest.mock import MagicMock
import os
from openai import OpenAI
import json

# Set dummy environment variables before importing the app
os.environ["DATABASE_URL"] = "sqlite:///./dummy_for_import.db"
os.environ["OPENAI_API_KEY"] = "dummy_key"

from chatbot_backend.main import app
from chatbot_backend.database import engine as main_engine
from chatbot_backend.agent import assistant_id, client as openai_client_instance


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


@pytest.fixture(name="mock_client")
def mock_openai(mocker):
    # Create a mock for the entire OpenAI client instance
    mock_client = MagicMock()

    # Patch the OpenAI class constructor itself to return our mock_client
    mocker.patch('openai.OpenAI', return_value=mock_client)
    # Mock the client in agent.py directly as it's a global instance
    mocker.patch('chatbot_backend.agent.client', new=mock_client)

    # Mock the specific beta.threads methods on mock_client
    mock_client.beta.threads.create = MagicMock()
    mock_client.beta.threads.retrieve = MagicMock()
    mock_client.beta.threads.messages.create = MagicMock()

    # Mock the specific beta.threads.runs methods on mock_client
    mock_client.beta.threads.runs.create = MagicMock()
    mock_client.beta.threads.runs.retrieve = MagicMock()
    mock_client.beta.threads.runs.submit_tool_outputs = MagicMock()

    # Mock the specific beta.threads.messages methods on mock_client
    mock_client.beta.threads.messages.list = MagicMock()

    # --- Setup return values and side effects for mocked methods ---

    # Mock the Assistant object that get_agent would return
    mock_assistant = MagicMock()
    mock_assistant.id = "asst_mockid"
    mocker.patch('chatbot_backend.agent.create_or_retrieve_assistant', return_value=mock_assistant)

    # Mock the thread object
    mock_thread = MagicMock()
    mock_thread.id = "thread_mockid"
    mock_client.beta.threads.create.return_value = mock_thread
    mock_client.beta.threads.retrieve.return_value = mock_thread

    # Mock messages.create
    mock_client.beta.threads.messages.create.return_value = MagicMock()

    # Mock runs.create
    mock_run_initial = MagicMock()
    mock_run_initial.id = "run_mockid"
    mock_run_initial.status = "queued" # Initial status
    mock_client.beta.threads.runs.create.return_value = mock_run_initial

    # Mock the tool call for add_task
    mock_tool_call = MagicMock()
    mock_tool_call.id = "call_mockid"
    mock_tool_call.function.name = "add_task"
    mock_tool_call.function.arguments = json.dumps({"user_id": "testuser", "title": "write integration test"})

    mock_submit_tool_outputs = MagicMock()
    mock_submit_tool_outputs.tool_calls = [mock_tool_call]

    # Mock runs.retrieve to simulate the run lifecycle
    mock_run_requires_action = MagicMock()
    mock_run_requires_action.id = "run_mockid"
    mock_run_requires_action.status = "requires_action"
    mock_run_requires_action.required_action.type = "submit_tool_outputs"
    mock_run_requires_action.required_action.submit_tool_outputs = mock_submit_tool_outputs

    mock_run_completed = MagicMock()
    mock_run_completed.id = "run_mockid"
    mock_run_completed.status = "completed"

    # Configure the side_effect for runs.retrieve to return different statuses
    mock_client.beta.threads.runs.retrieve.side_effect = [
        mock_run_initial, # First check (queued)
        mock_run_requires_action, # Second check (requires_action)
        mock_run_completed # Third check (completed after tool submission)
    ]

    # Mock runs.submit_tool_outputs
    mock_client.beta.threads.runs.submit_tool_outputs.return_value = MagicMock()

    # Mock messages.list for the final assistant response
    mock_message_text = MagicMock()
    mock_message_text.type = "text"
    mock_message_text.text.value = "I have added the task: write integration test."

    mock_assistant_message = MagicMock()
    mock_assistant_message.role = "assistant"
    mock_assistant_message.content = [mock_message_text]
    
    mock_messages_list = MagicMock()
    mock_messages_list.data = [mock_assistant_message]
    mock_client.beta.threads.messages.list.return_value = mock_messages_list

    # Ensure get_agent returns the mocked client and assistant for the dependency
    mocker.patch('chatbot_backend.main.get_agent', return_value=(mock_client, mock_assistant))

    # Mock the actual tool functions to ensure they are called and return expected results
    mocker.patch('chatbot_backend.tools.task_tools.add_task', return_value={"task_id": 1, "status": "created", "title": "write integration test"})
    mocker.patch('chatbot_backend.tools.task_tools.list_tasks') # We can expand this for other tests
    return mock_client


def test_chat_add_task(client: TestClient, session: Session, mock_client):
    """
    Tests the /api/{user_id}/chat endpoint for adding a task with mocked OpenAI API calls.
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
    assert "thread_id" in data
    assert "I have added the task" in data["response"]
    
    # 3. Verify the database state
    from chatbot_backend.models import Task, Conversation, Message
    
    # Verify a Task was created (by the actual tool function)
    tasks = session.query(Task).all()
    assert len(tasks) == 1
    task = tasks[0]
    assert task.user_id == user_id
    assert task.title == "write integration test"
    
    # Verify a Conversation was created/updated
    conversations = session.query(Conversation).all()
    assert len(conversations) == 1
    assert conversations[0].user_id == user_id
    assert conversations[0].thread_id == "thread_mockid" # Ensure thread_id is saved
    
    # Verify two Messages were created (user and assistant)
    messages = session.query(Message).all()
    assert len(messages) == 2
    user_msg = next((m for m in messages if m.role == 'user'), None)
    assistant_msg = next((m for m in messages if m.role == 'assistant'), None)
    
    assert user_msg is not None
    assert user_msg.content == message
    
    assert assistant_msg is not None
    assert "I have added the task" in assistant_msg.content

    # Verify OpenAI client methods were called as expected
    mock_client.beta.threads.create.assert_called_once()
    mock_client.beta.threads.messages.create.assert_called_once_with(
        thread_id="thread_mockid", role="user", content=message
    )
    mock_client.beta.threads.runs.create.assert_called_once_with(
        thread_id="thread_mockid", assistant_id="asst_mockid"
    )
    # retrieve is called multiple times due to polling
    assert mock_client.beta.threads.runs.retrieve.call_count >= 3
    mock_client.beta.threads.runs.submit_tool_outputs.assert_called_once()
    mock_client.beta.threads.messages.list.assert_called_once_with(
        thread_id="thread_mockid", order="desc", limit=1
    )
