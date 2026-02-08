"""
Recurring Tasks Automation Service

This service listens to the "todo-events" Kafka topic for task completion events.
When a recurring task is completed (TodoUpdated with completed=true), it automatically
creates the next occurrence based on the recurring_interval (daily, weekly, monthly).
"""

from confluent_kafka import Consumer, KafkaException, KafkaError
import json
import os
import sys
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from sqlmodel import create_engine, Session, SQLModel, Field, Column
from sqlalchemy import JSON
from typing import Optional, List


# Configuration
KAFKA_BOOTSTRAP_SERVERS = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "localhost:9093")
KAFKA_TOPIC = os.getenv("KAFKA_TOPIC", "todo-events")
KAFKA_GROUP_ID = os.getenv("KAFKA_GROUP_ID", "recurring-tasks-service-group")
DATABASE_URL = os.getenv("DATABASE_URL")

# Valid recurring intervals
VALID_INTERVALS = {"daily", "weekly", "monthly"}


# Database Models (matching backend/models.py)
class Todo(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    description: Optional[str] = None
    completed: bool = False
    priority: Optional[str] = None
    tags: Optional[List[str]] = Field(default=None, sa_column=Column(JSON))
    due_date: Optional[datetime] = None
    recurring_interval: Optional[str] = None
    user_id: Optional[int] = Field(default=None, foreign_key="user.id")


def get_database_engine():
    """Create and return a database engine."""
    if not DATABASE_URL:
        raise ValueError("DATABASE_URL environment variable is not set")
    return create_engine(DATABASE_URL)


def calculate_next_due_date(current_due_date: Optional[datetime], interval: str) -> datetime:
    """
    Calculate the next due date based on the recurring interval.

    Args:
        current_due_date: The current due date of the completed task
        interval: One of 'daily', 'weekly', 'monthly'

    Returns:
        The calculated next due date
    """
    # If no current due date, start from now
    base_date = current_due_date if current_due_date else datetime.utcnow()

    if interval == "daily":
        return base_date + timedelta(days=1)
    elif interval == "weekly":
        return base_date + timedelta(weeks=1)
    elif interval == "monthly":
        return base_date + relativedelta(months=1)
    else:
        # Default to daily if unknown interval
        print(f"[WARNING] Unknown interval '{interval}', defaulting to daily")
        return base_date + timedelta(days=1)


def create_next_occurrence(session: Session, completed_todo_data: dict) -> Optional[Todo]:
    """
    Create the next occurrence of a recurring task.

    Args:
        session: Database session
        completed_todo_data: The data of the completed todo

    Returns:
        The newly created Todo or None if creation failed
    """
    try:
        # Parse the due date if present
        current_due_date = None
        due_date_str = completed_todo_data.get("due_date")
        if due_date_str:
            try:
                current_due_date = datetime.fromisoformat(due_date_str.replace("Z", "+00:00"))
            except ValueError:
                print(f"[WARNING] Could not parse due_date: {due_date_str}")

        recurring_interval = completed_todo_data.get("recurring_interval")

        # Calculate the next due date
        next_due_date = calculate_next_due_date(current_due_date, recurring_interval)

        # Create the new todo instance
        new_todo = Todo(
            title=completed_todo_data.get("title"),
            description=completed_todo_data.get("description"),
            completed=False,  # New occurrence starts as not completed
            priority=completed_todo_data.get("priority"),
            tags=completed_todo_data.get("tags"),
            due_date=next_due_date,
            recurring_interval=recurring_interval,  # Keep the recurring interval
            user_id=completed_todo_data.get("user_id")
        )

        session.add(new_todo)
        session.commit()
        session.refresh(new_todo)

        return new_todo

    except Exception as e:
        print(f"[ERROR] Failed to create next occurrence: {e}")
        session.rollback()
        return None


def is_recurring_task_completion(event_data: dict) -> bool:
    """
    Check if the event represents a recurring task being completed.

    Args:
        event_data: The event data from Kafka

    Returns:
        True if this is a recurring task completion event
    """
    event_type = event_data.get("event_type")

    if event_type != "TodoUpdated":
        return False

    # Get the new todo data (after the update)
    new_todo_data = event_data.get("new_todo_data")
    if not new_todo_data:
        # Fallback for different event structure
        new_todo_data = event_data.get("todo_data")

    if not new_todo_data:
        return False

    # Check if the task is now completed
    completed = new_todo_data.get("completed", False)
    if not completed:
        return False

    # Check if it has a valid recurring interval
    recurring_interval = new_todo_data.get("recurring_interval")
    if not recurring_interval:
        return False

    if recurring_interval.lower() not in VALID_INTERVALS:
        print(f"[WARNING] Invalid recurring interval: {recurring_interval}")
        return False

    # Check if it was previously not completed (to avoid duplicate processing)
    old_todo_data = event_data.get("old_todo_data")
    if old_todo_data:
        old_completed = old_todo_data.get("completed", False)
        if old_completed:
            # Task was already completed, this isn't a new completion
            return False

    return True


def consume_events():
    """Main event consumption loop."""
    # Initialize database engine
    try:
        engine = get_database_engine()
        print(f"[*] Database connection established")
    except ValueError as e:
        print(f"[ERROR] Database configuration error: {e}")
        sys.exit(1)

    # Kafka consumer configuration
    conf = {
        'bootstrap.servers': KAFKA_BOOTSTRAP_SERVERS,
        'group.id': KAFKA_GROUP_ID,
        'auto.offset.reset': 'earliest'
    }

    consumer = Consumer(conf)

    try:
        consumer.subscribe([KAFKA_TOPIC])

        print(f"[*] Recurring Tasks Service started")
        print(f"[*] Listening on topic '{KAFKA_TOPIC}'...")
        print(f"[*] Consumer group: '{KAFKA_GROUP_ID}'")
        print(f"[*] Valid recurring intervals: {VALID_INTERVALS}")

        while True:
            msg = consumer.poll(timeout=1.0)

            if msg is None:
                continue

            if msg.error():
                if msg.error().code() == KafkaError._PARTITION_EOF:
                    # End of partition event, not an error
                    sys.stderr.write('%% %s [%d] reached end at offset %d\n' %
                                     (msg.topic(), msg.partition(), msg.offset()))
                elif msg.error():
                    raise KafkaException(msg.error())
            else:
                # Process message
                try:
                    event_data = json.loads(msg.value().decode('utf-8'))
                except json.JSONDecodeError as e:
                    print(f"[ERROR] Failed to parse message JSON: {e}")
                    continue

                event_type = event_data.get("event_type")

                # Log all received events
                todo_id = event_data.get("todo_id")
                user_id = event_data.get("user_id")
                print(f"[*] Received event: {event_type} for Todo ID: {todo_id} (User: {user_id})")

                # Check if this is a recurring task completion
                if is_recurring_task_completion(event_data):
                    new_todo_data = event_data.get("new_todo_data") or event_data.get("todo_data")
                    recurring_interval = new_todo_data.get("recurring_interval")

                    print(f"[*] Recurring task completed: '{new_todo_data.get('title')}' "
                          f"(interval: {recurring_interval})")

                    # Create the next occurrence
                    with Session(engine) as session:
                        new_todo = create_next_occurrence(session, new_todo_data)

                        if new_todo:
                            print(f"[SUCCESS] Created next occurrence: Todo ID {new_todo.id}, "
                                  f"due: {new_todo.due_date.isoformat() if new_todo.due_date else 'N/A'}")
                        else:
                            print(f"[ERROR] Failed to create next occurrence for Todo ID: {todo_id}")

    except KeyboardInterrupt:
        print("\n[*] Shutting down Recurring Tasks Service...")
    finally:
        # Close down consumer to commit final offsets
        consumer.close()
        print("[*] Consumer closed")


if __name__ == "__main__":
    consume_events()
