import pytest
from phase1_cli.src.services import TodoService
from phase1_cli.src.models import Todo

@pytest.fixture
def todo_service():
    """Provides a fresh TodoService instance for each test."""
    return TodoService()

def test_create_todo(todo_service: TodoService):
    """Test creating a new todo."""
    todo = todo_service.create_todo("Buy groceries", "Milk, Eggs, Bread")
    assert todo.id == 1
    assert todo.title == "Buy groceries"
    assert todo.description == "Milk, Eggs, Bread"
    assert not todo.completed
    assert len(todo_service.get_all_todos()) == 1

    todo2 = todo_service.create_todo("Walk the dog")
    assert todo2.id == 2
    assert todo2.title == "Walk the dog"
    assert todo2.description is None
    assert not todo2.completed
    assert len(todo_service.get_all_todos()) == 2

def test_create_todo_empty_title(todo_service: TodoService):
    """Test creating a todo with an empty title."""
    with pytest.raises(ValueError, match="Title cannot be empty."):
        todo_service.create_todo("")

def test_get_all_todos(todo_service: TodoService):
    """Test retrieving all todos."""
    assert len(todo_service.get_all_todos()) == 0
    todo_service.create_todo("Task 1")
    todo_service.create_todo("Task 2")
    todos = todo_service.get_all_todos()
    assert len(todos) == 2
    assert todos[0].title == "Task 1"
    assert todos[1].title == "Task 2"

def test_get_todo_by_id(todo_service: TodoService):
    """Test retrieving a todo by its ID."""
    todo1 = todo_service.create_todo("Task A")
    todo2 = todo_service.create_todo("Task B")

    found_todo = todo_service.get_todo_by_id(todo1.id)
    assert found_todo == todo1

    not_found_todo = todo_service.get_todo_by_id(999)
    assert not_found_todo is None

def test_update_todo(todo_service: TodoService):
    """Test updating an existing todo."""
    todo = todo_service.create_todo("Old Title", "Old Description")
    
    # Update title and description
    updated_todo = todo_service.update_todo(todo.id, "New Title", "New Description", True)
    assert updated_todo is not None
    assert updated_todo.title == "New Title"
    assert updated_todo.description == "New Description"
    assert updated_todo.completed

    # Update only title
    updated_todo_title = todo_service.update_todo(todo.id, title="Only Title Change")
    assert updated_todo_title is not None
    assert updated_todo_title.title == "Only Title Change"
    assert updated_todo_title.description == "New Description" # Should remain unchanged
    assert updated_todo_title.completed # Should remain unchanged

    # Update only description
    updated_todo_desc = todo_service.update_todo(todo.id, description="Only Desc Change")
    assert updated_todo_desc is not None
    assert updated_todo_desc.title == "Only Title Change" # Should remain unchanged
    assert updated_todo_desc.description == "Only Desc Change"
    assert updated_todo_desc.completed # Should remain unchanged

    # Update only completed status
    updated_todo_completed = todo_service.update_todo(todo.id, completed=False)
    assert updated_todo_completed is not None
    assert updated_todo_completed.title == "Only Title Change"
    assert updated_todo_completed.description == "Only Desc Change"
    assert not updated_todo_completed.completed

    # Try to update a non-existent todo
    non_existent_update = todo_service.update_todo(999, "Non Existent")
    assert non_existent_update is None

    # Test updating with empty title
    with pytest.raises(ValueError, match="Title cannot be empty."):
        todo_service.update_todo(todo.id, "")

def test_delete_todo(todo_service: TodoService):
    """Test deleting a todo."""
    todo1 = todo_service.create_todo("Task 1")
    todo2 = todo_service.create_todo("Task 2")

    # Delete an existing todo
    assert todo_service.delete_todo(todo1.id)
    assert len(todo_service.get_all_todos()) == 1
    assert todo_service.get_todo_by_id(todo1.id) is None

    # Try to delete a non-existent todo
    assert not todo_service.delete_todo(999)
    assert len(todo_service.get_all_todos()) == 1