import pytest
from pydantic import ValidationError
from src.models.todo import Todo

def test_todo_creation():
    """
    Tests that a Todo can be created with valid data.
    """
    todo = Todo(id=1, title="Test Todo", description="Test description")
    assert todo.id == 1
    assert todo.title == "Test Todo"
    assert todo.description == "Test description"
    assert not todo.completed

def test_todo_title_must_not_be_empty():
    """
    Tests that a Todo cannot be created with an empty title.
    """
    with pytest.raises(ValidationError) as excinfo:
        Todo(id=1, title="", description="Test description")
    assert "Title must not be empty" in str(excinfo.value)

    with pytest.raises(ValidationError) as excinfo:
        Todo(id=1, title="   ", description="Test description")
    assert "Title must not be empty" in str(excinfo.value)

def test_todo_completed_defaults_to_false():
    """
    Tests that a Todo's completed status defaults to False.
    """
    todo = Todo(id=1, title="Test Todo")
    assert not todo.completed
