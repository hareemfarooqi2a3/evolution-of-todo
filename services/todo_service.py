from typing import List, Optional
from models.todo import Todo

class TodoService:
    """
    Manages the collection of todos in memory.
    """
    def __init__(self):
        self._todos: List[Todo] = []
        self._next_id: int = 1

    def add_todo(self, title: str, description: Optional[str] = None) -> Todo:
        """
        Adds a new todo to the collection.

        Args:
            title: The title of the todo.
            description: The description of the todo.

        Returns:
            The newly created todo.
        """
        todo = Todo(id=self._next_id, title=title, description=description)
        self._todos.append(todo)
        self._next_id += 1
        return todo

    def list_todos(self) -> List[Todo]:
        """
        Returns the list of all todos.

        Returns:
            A list of all todos.
        """
        return self._todos

    def get_todo_by_id(self, todo_id: int) -> Optional[Todo]:
        """
        Gets a todo by its ID.

        Args:
            todo_id: The ID of the todo to get.

        Returns:
            The todo with the specified ID, or None if not found.
        """
        for todo in self._todos:
            if todo.id == todo_id:
                return todo
        return None

    def complete_todo(self, todo_id: int) -> Optional[Todo]:
        """
        Marks a todo as complete.

        Args:
            todo_id: The ID of the todo to mark as complete.

        Returns:
            The updated todo, or None if not found.
        """
        todo = self.get_todo_by_id(todo_id)
        if todo:
            todo.completed = True
        return todo

    def uncomplete_todo(self, todo_id: int) -> Optional[Todo]:
        """
        Marks a todo as incomplete.

        Args:
            todo_id: The ID of the todo to mark as incomplete.

        Returns:
            The updated todo, or None if not found.
        """
        todo = self.get_todo_by_id(todo_id)
        if todo:
            todo.completed = False
        return todo

    def update_todo(self, todo_id: int, title: Optional[str] = None, description: Optional[str] = None) -> Optional[Todo]:
        """
        Updates a todo.

        Args:
            todo_id: The ID of the todo to update.
            title: The new title of the todo.
            description: The new description of the todo.

        Returns:
            The updated todo, or None if not found.
        """
        todo = self.get_todo_by_id(todo_id)
        if todo:
            if title is not None:
                todo.title = title
            if description is not None:
                todo.description = description
        return todo

    def delete_todo(self, todo_id: int) -> bool:
        """
        Deletes a todo.

        Args:
            todo_id: The ID of the todo to delete.

        Returns:
            True if the todo was deleted, False otherwise.
        """
        todo = self.get_todo_by_id(todo_id)
        if todo:
            self._todos.remove(todo)
            return True
        return False
