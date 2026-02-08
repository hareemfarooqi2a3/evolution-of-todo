from typing import List, Optional
import json
import os
from .models import Todo

# File path for persistent storage
DATA_FILE = os.path.join(os.path.dirname(__file__), '..', 'todos.json')

class TodoService:
    """Manages the collection of Todo items with file-based persistence."""
    def __init__(self):
        self._todos: List[Todo] = []
        self._next_id = 1
        self._load_from_file()

    def _load_from_file(self):
        """Load todos from JSON file if it exists."""
        if os.path.exists(DATA_FILE):
            try:
                with open(DATA_FILE, 'r') as f:
                    data = json.load(f)
                    self._todos = [Todo(**item) for item in data.get('todos', [])]
                    self._next_id = data.get('next_id', 1)
            except (json.JSONDecodeError, IOError):
                self._todos = []
                self._next_id = 1

    def _save_to_file(self):
        """Save todos to JSON file."""
        data = {
            'todos': [{'id': t.id, 'title': t.title, 'description': t.description, 'completed': t.completed} for t in self._todos],
            'next_id': self._next_id
        }
        with open(DATA_FILE, 'w') as f:
            json.dump(data, f, indent=2)

    def create_todo(self, title: str, description: Optional[str] = None) -> Todo:
        """Creates a new Todo item and adds it to the list."""
        if not title:
            raise ValueError("Title cannot be empty.")
        
        todo = Todo(
            id=self._next_id,
            title=title,
            description=description
        )
        self._todos.append(todo)
        self._next_id += 1
        self._save_to_file()
        return todo

    def get_all_todos(self) -> List[Todo]:
        """Returns the list of all Todo items."""
        return self._todos

    def get_todo_by_id(self, todo_id: int) -> Optional[Todo]:
        """Finds a Todo item by its ID."""
        for todo in self._todos:
            if todo.id == todo_id:
                return todo
        return None

    def update_todo(
        self,
        todo_id: int,
        title: Optional[str] = None,
        description: Optional[str] = None,
        completed: Optional[bool] = None,
    ) -> Optional[Todo]:
        """Updates the fields of an existing Todo item."""
        todo = self.get_todo_by_id(todo_id)
        if not todo:
            return None

        if title is not None:
            if not title:
                raise ValueError("Title cannot be empty.")
            todo.title = title
        
        if description is not None:
            todo.description = description
            
        if completed is not None:
            todo.completed = completed

        self._save_to_file()
        return todo

    def delete_todo(self, todo_id: int) -> bool:
        """Deletes a Todo item by its ID."""
        todo = self.get_todo_by_id(todo_id)
        if not todo:
            return False
        
        self._todos.remove(todo)
        self._save_to_file()
        return True
