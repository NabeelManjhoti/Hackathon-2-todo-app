"""Task request and response schemas."""

from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field


class CreateTaskRequest(BaseModel):
    """Request schema for creating a new task.

    Attributes:
        title: Task title (required, cannot be empty)
        description: Optional detailed description
        due_date: Optional due date in ISO 8601 format
    """

    title: str = Field(
        ...,
        min_length=1,
        description="Task title (required, cannot be empty)",
        examples=["Complete project documentation"],
    )
    description: Optional[str] = Field(
        None,
        description="Optional detailed description",
        examples=["Write comprehensive API documentation"],
    )
    due_date: Optional[datetime] = Field(
        None,
        description="Optional due date in ISO 8601 format",
        examples=["2026-02-15T17:00:00Z"],
    )


class UpdateTaskRequest(BaseModel):
    """Request schema for updating an existing task.

    All fields are optional - only provided fields will be updated.

    Attributes:
        title: Updated task title
        description: Updated task description
        due_date: Updated due date
        completed: Updated completion status
    """

    title: Optional[str] = Field(
        None,
        min_length=1,
        description="Updated task title",
        examples=["Updated task title"],
    )
    description: Optional[str] = Field(
        None,
        description="Updated task description",
        examples=["Updated description"],
    )
    due_date: Optional[datetime] = Field(
        None,
        description="Updated due date in ISO 8601 format",
        examples=["2026-02-20T17:00:00Z"],
    )
    completed: Optional[bool] = Field(
        None,
        description="Updated completion status",
        examples=[True],
    )


class TaskResponse(BaseModel):
    """Response schema for task data.

    Attributes:
        id: Unique task identifier
        user_id: User who owns this task
        title: Task title
        description: Task description (optional)
        due_date: Task due date (optional)
        completed: Completion status
        created_at: Timestamp when task was created
        updated_at: Timestamp when task was last updated
    """

    id: UUID = Field(
        ...,
        description="Unique task identifier",
        examples=["550e8400-e29b-41d4-a716-446655440000"],
    )
    user_id: UUID = Field(
        ...,
        description="User who owns this task",
        examples=["660e8400-e29b-41d4-a716-446655440001"],
    )
    title: str = Field(
        ...,
        description="Task title",
        examples=["Complete project documentation"],
    )
    description: Optional[str] = Field(
        None,
        description="Task description",
        examples=["Write comprehensive API documentation"],
    )
    due_date: Optional[datetime] = Field(
        None,
        description="Task due date in ISO 8601 format",
        examples=["2026-02-15T17:00:00Z"],
    )
    completed: bool = Field(
        ...,
        description="Completion status",
        examples=[False],
    )
    created_at: datetime = Field(
        ...,
        description="Timestamp when task was created",
        examples=["2026-02-08T10:00:00Z"],
    )
    updated_at: datetime = Field(
        ...,
        description="Timestamp when task was last updated",
        examples=["2026-02-08T10:00:00Z"],
    )

    model_config = {
        "from_attributes": True,  # Pydantic v2 (was orm_mode in v1)
    }
