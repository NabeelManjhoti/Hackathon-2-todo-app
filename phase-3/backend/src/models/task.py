"""Task database model."""

from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4

from sqlmodel import Field, SQLModel


class Task(SQLModel, table=True):
    """Task entity representing a todo item.

    Attributes:
        id: Unique task identifier (UUID)
        user_id: Owner of the task (UUID, for future multi-user support)
        title: Task title (required, cannot be empty)
        description: Optional detailed description
        due_date: Optional due date for the task
        completed: Completion status (defaults to False)
        created_at: Timestamp when task was created (server default)
        updated_at: Timestamp when task was last updated (server default, auto-update)
    """

    __tablename__ = "tasks"

    id: UUID = Field(
        default_factory=uuid4,
        primary_key=True,
        nullable=False,
        description="Unique task identifier",
    )
    user_id: UUID = Field(
        nullable=False,
        description="User who owns this task",
    )
    title: str = Field(
        nullable=False,
        min_length=1,
        description="Task title (required, cannot be empty)",
    )
    description: Optional[str] = Field(
        default=None,
        nullable=True,
        description="Optional detailed description",
    )
    due_date: Optional[datetime] = Field(
        default=None,
        nullable=True,
        description="Optional due date for the task",
    )
    completed: bool = Field(
        default=False,
        nullable=False,
        description="Completion status",
    )
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        nullable=False,
        description="Timestamp when task was created",
    )
    updated_at: datetime = Field(
        default_factory=datetime.utcnow,
        nullable=False,
        description="Timestamp when task was last updated",
    )
