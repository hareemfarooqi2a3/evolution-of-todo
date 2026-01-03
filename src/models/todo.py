from typing import Optional
from pydantic import BaseModel, field_validator

class Todo(BaseModel):
    """
    Represents a single todo item.
    """
    id: int
    title: str
    description: Optional[str] = None
    completed: bool = False

    @field_validator('title')
    def title_must_not_be_empty(cls, v: str) -> str:
        """
        Validates that the title is not empty.
        """
        if not v.strip():
            raise ValueError('Title must not be empty')
        return v
