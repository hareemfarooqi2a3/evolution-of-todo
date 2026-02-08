import pytest
from phase1_cli.src.models import Todo


def test_todo_creation():
    """Tests that a Todo can be created with valid data."""
    todo = Todo(id=1, title="Test Todo", description="Test description")
    assert todo.id == 1
    assert todo.title == "Test Todo"
    assert todo.description == "Test description"
    assert not todo.completed


def test_todo_completed_defaults_to_false():
    """Tests that a Todo's completed status defaults to False."""
    todo = Todo(id=1, title="Test Todo")
    assert not todo.completed


def test_todo_with_description():
    """Tests that a Todo can be created with a description."""
    todo = Todo(id=1, title="Test Todo", description="Some description")
    assert todo.description == "Some description"


def test_todo_without_description():
    """Tests that a Todo can be created without a description."""
    todo = Todo(id=1, title="Test Todo")
    assert todo.description is None
