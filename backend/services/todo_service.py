from typing import List, Optional
from sqlmodel import Session, select
from ..models import Todo, TodoCreate, TodoUpdate

class TodoService:
    def __init__(self, session: Session):
        self.session = session

    def get_all(self, user_id: int, search: Optional[str] = None, filter_by_status: Optional[str] = None, filter_by_priority: Optional[str] = None, sort_by: Optional[str] = None) -> List[Todo]:
        query = select(Todo).where(Todo.user_id == user_id)
        if search:
            query = query.where(
                (Todo.title.ilike(f"%{search}%")) |
                (Todo.description.ilike(f"%{search}%"))
            )
        if filter_by_status is not None:
            completed = filter_by_status.lower() == 'completed'
            query = query.where(Todo.completed == completed)
        if filter_by_priority:
            query = query.where(Todo.priority.ilike(filter_by_priority))
        
        todos = self.session.exec(query).all()

        if sort_by:
            if sort_by == 'priority':
                priority_map = {'high': 0, 'medium': 1, 'low': 2}
                todos = sorted(todos, key=lambda x: priority_map.get(x.priority.lower() if x.priority else 'medium', 1))
            elif sort_by == 'title':
                todos = sorted(todos, key=lambda x: x.title if x.title else '')
        return todos

    def get_by_id(self, todo_id: int, user_id: int) -> Optional[Todo]:
        return self.session.exec(select(Todo).where(Todo.id == todo_id, Todo.user_id == user_id)).first()

    def create(self, todo_create: TodoCreate, user_id: int) -> Todo:
        todo = Todo.from_orm(todo_create, update={'user_id': user_id})
        self.session.add(todo)
        self.session.commit()
        self.session.refresh(todo)
        return todo

    def update(self, todo_id: int, todo_update: TodoUpdate, user_id: int) -> Optional[Todo]:
        todo = self.get_by_id(todo_id, user_id)
        if not todo:
            return None

        update_data = todo_update.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(todo, key, value)
        
        self.session.add(todo)
        self.session.commit()
        self.session.refresh(todo)
        return todo

    def delete(self, todo_id: int) -> bool:
        todo = self.get_by_id(todo_id)
        if todo:
            self._todos.remove(todo)
            return True
        return False



