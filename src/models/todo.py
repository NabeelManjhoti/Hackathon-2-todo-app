"""
Todo Application - Todo Model

This module defines the data model for todo items.
"""
from dataclasses import dataclass
from typing import Optional


@dataclass
class TodoItem:
    """Data class representing a todo item."""
    task: str
    completed: bool = False
    id: Optional[int] = None

    def __post_init__(self):
        """Validate the todo item after initialization."""
        if not self.task or not self.task.strip():
            raise ValueError("Task cannot be empty")

        self.task = self.task.strip()