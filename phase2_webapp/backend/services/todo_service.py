from typing import List, Optional, Any
from sqlmodel import Session, select
import json
import os

# Make Dapr optional for local development
try:
    from dapr.clients import DaprClient
    DAPR_AVAILABLE = True
except ImportError:
    DAPR_AVAILABLE = False
    DaprClient = None

try:
    from ..models import Todo, TodoCreate, TodoUpdate, TodoCreatedEvent, TodoUpdatedEvent, TodoDeletedEvent
except ImportError:
    import sys
    import os
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from models import Todo, TodoCreate, TodoUpdate, TodoCreatedEvent, TodoUpdatedEvent, TodoDeletedEvent
from datetime import datetime


class TodoService:
    def __init__(self, session: Session, dapr_client: Any = None, pubsub_name: str = "", topic_name: str = ""):
        self.session = session
        self.dapr_client = dapr_client
        self.pubsub_name = pubsub_name
        self.topic_name = topic_name
        self.dapr_enabled = DAPR_AVAILABLE and dapr_client is not None

    def _publish_event(self, event: dict, key: str):
        """Helper to publish an event to Dapr PubSub (if available)."""
        if not self.dapr_enabled:
            print(f"[LOCAL MODE] Would publish event: {key}")
            return

        try:
            self.dapr_client.publish_event(
                pubsub_name=self.pubsub_name,
                topic_name=self.topic_name,
                data=json.dumps(event),
                data_content_type='application/json'
            )
            print(f"Message published to Dapr PubSub topic '{self.topic_name}' with key '{key}'")
        except Exception as e:
            print(f"Failed to publish message to Dapr PubSub: {e}")

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
            elif sort_by == 'due_date':
                todos = sorted(todos, key=lambda x: x.due_date if x.due_date else datetime.max)
        return todos

    def get_by_id(self, todo_id: int, user_id: int) -> Optional[Todo]:
        return self.session.exec(select(Todo).where(Todo.id == todo_id, Todo.user_id == user_id)).first()

    def create(self, todo_create: TodoCreate, user_id: int) -> Todo:
        todo_data = todo_create.model_dump()
        todo_data['user_id'] = user_id
        todo = Todo(**todo_data)
        self.session.add(todo)
        self.session.commit()
        self.session.refresh(todo)

        if self.dapr_enabled:
            event = TodoCreatedEvent(todo_id=todo.id, user_id=todo.user_id, todo_data=todo).model_dump()
            self._publish_event(event, key=f"todo_created_{todo.id}")

        return todo

    def update(self, todo_id: int, todo_update: TodoUpdate, user_id: int) -> Optional[Todo]:
        todo = self.get_by_id(todo_id, user_id)
        if not todo:
            return None

        old_todo_data = todo.model_copy(deep=True)

        update_data = todo_update.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(todo, key, value)

        self.session.add(todo)
        self.session.commit()
        self.session.refresh(todo)

        if self.dapr_enabled:
            event = TodoUpdatedEvent(todo_id=todo.id, user_id=todo.user_id, old_todo_data=old_todo_data, new_todo_data=todo).model_dump()
            self._publish_event(event, key=f"todo_updated_{todo.id}")

        return todo

    def delete(self, todo_id: int, user_id: int) -> bool:
        todo = self.get_by_id(todo_id, user_id)
        if todo:
            todo_copy = todo.model_copy(deep=True)
            self.session.delete(todo)
            self.session.commit()

            if self.dapr_enabled:
                event = TodoDeletedEvent(todo_id=todo_copy.id, user_id=todo_copy.user_id, todo_data=todo_copy).model_dump()
                self._publish_event(event, key=f"todo_deleted_{todo_copy.id}")

            return True
        return False
