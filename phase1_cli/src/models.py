from dataclasses import dataclass, field
from typing import Optional

@dataclass
class Todo:
    """Represents a single task in the to-do list."""
    id: int
    title: str
    description: Optional[str] = None
    completed: bool = False
