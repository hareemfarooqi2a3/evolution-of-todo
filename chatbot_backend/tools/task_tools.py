from sqlmodel import Session, select
import datetime
import sys
import os

# Handle imports for both running from within directory and as a package
try:
    from chatbot_backend.database import engine
    from chatbot_backend.models import Task
except ImportError:
    # Add parent directory to path for local development
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from database import engine
    from models import Task

def add_task(user_id: str, title: str, description: str = None):
    """
    Create a new task for a user.
    """
    with Session(engine) as session:
        task = Task(
            user_id=user_id,
            title=title,
            description=description,
            created_at=str(datetime.datetime.utcnow()),
            updated_at=str(datetime.datetime.utcnow()),
        )
        session.add(task)
        session.commit()
        session.refresh(task)
        return {"task_id": task.id, "status": "created", "title": task.title}

def list_tasks(user_id: str, status: str = "all"):
    """
    Retrieve tasks for a user, optionally filtering by status.
    """
    with Session(engine) as session:
        statement = select(Task).where(Task.user_id == user_id)
        if status == "pending":
            statement = statement.where(Task.completed == False)
        elif status == "completed":
            statement = statement.where(Task.completed == True)
        
        tasks = session.exec(statement).all()
        return [task.model_dump() for task in tasks]

def complete_task(user_id: str, task_id: int):
    """
    Mark a task as complete.
    """
    with Session(engine) as session:
        task = session.exec(select(Task).where(Task.id == task_id, Task.user_id == user_id)).first()
        if not task:
            return {"error": "Task not found"}
        task.completed = True
        task.updated_at = str(datetime.datetime.utcnow())
        session.add(task)
        session.commit()
        session.refresh(task)
        return {"task_id": task.id, "status": "completed", "title": task.title}

def update_task(user_id: str, task_id: int, title: str = None, description: str = None):
    """
    Update a task's title or description.
    """
    with Session(engine) as session:
        task = session.exec(select(Task).where(Task.id == task_id, Task.user_id == user_id)).first()
        if not task:
            return {"error": "Task not found"}
        if title:
            task.title = title
        if description:
            task.description = description
        task.updated_at = str(datetime.datetime.utcnow())
        session.add(task)
        session.commit()
        session.refresh(task)
        return {"task_id": task.id, "status": "updated", "title": task.title}

def delete_task(user_id: str, task_id: int):
    """
    Delete a task.
    """
    with Session(engine) as session:
        task = session.exec(select(Task).where(Task.id == task_id, Task.user_id == user_id)).first()
        if not task:
            return {"error": "Task not found"}
        session.delete(task)
        session.commit()
        return {"task_id": task_id, "status": "deleted"}
