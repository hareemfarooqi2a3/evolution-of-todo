from src.services.todo_service import TodoService

def test_add_todo():
    """
    Tests that a todo can be added to the service.
    """
    service = TodoService()
    todo = service.add_todo(title="Test Todo", description="Test description")
    assert todo.id == 1
    assert todo.title == "Test Todo"
    assert todo.description == "Test description"
    assert not todo.completed
    assert len(service.list_todos()) == 1

def test_list_todos():
    """
    Tests that all todos can be listed.
    """
    service = TodoService()
    service.add_todo(title="Todo 1")
    service.add_todo(title="Todo 2")
    todos = service.list_todos()
    assert len(todos) == 2
    assert todos[0].title == "Todo 1"
    assert todos[1].title == "Todo 2"

def test_add_todo_increments_id():
    """
    Tests that the todo ID is auto-incremented.
    """
    service = TodoService()
    todo1 = service.add_todo(title="Todo 1")
    todo2 = service.add_todo(title="Todo 2")
    assert todo1.id == 1
    assert todo2.id == 2

def test_get_todo_by_id():
    """
    Tests that a todo can be retrieved by its ID.
    """
    service = TodoService()
    todo1 = service.add_todo(title="Todo 1")
    retrieved_todo = service.get_todo_by_id(todo1.id)
    assert retrieved_todo == todo1
    assert service.get_todo_by_id(999) is None

def test_complete_todo():
    """
    Tests that a todo can be marked as complete.
    """
    service = TodoService()
    todo = service.add_todo(title="Test Todo")
    assert not todo.completed
    updated_todo = service.complete_todo(todo.id)
    assert updated_todo.completed
    assert service.complete_todo(999) is None

def test_uncomplete_todo():
    """
    Tests that a todo can be marked as incomplete.
    """
    service = TodoService()
    todo = service.add_todo(title="Test Todo")
    updated_todo = service.complete_todo(todo.id)
    assert updated_todo.completed
    updated_todo = service.uncomplete_todo(todo.id)
    assert not updated_todo.completed
    assert service.uncomplete_todo(999) is None

def test_update_todo():
    """
    Tests that a todo can be updated.
    """
    service = TodoService()
    todo = service.add_todo(title="Test Todo", description="Test description")
    updated_todo = service.update_todo(todo.id, title="Updated Title", description="Updated description")
    assert updated_todo.title == "Updated Title"
    assert updated_todo.description == "Updated description"
    assert service.update_todo(999, title="Not found") is None

def test_delete_todo():
    """
    Tests that a todo can be deleted.
    """
    service = TodoService()
    todo = service.add_todo(title="Test Todo")
    assert len(service.list_todos()) == 1
    deleted = service.delete_todo(todo.id)
    assert deleted
    assert len(service.list_todos()) == 0
    assert not service.delete_todo(999)
