"""Task CRUD endpoints."""

from datetime import datetime
from typing import List
from uuid import UUID, uuid4

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.dependencies.database import get_db
from src.main import structured_logger
from src.models.task import Task
from src.schemas.task import CreateTaskRequest, TaskResponse, UpdateTaskRequest

# Type ignore for SQLModel column comparisons (mypy doesn't understand SQLModel's magic)
# These are valid SQLAlchemy/SQLModel expressions

router = APIRouter(prefix="/api/tasks", tags=["tasks"])


@router.post(
    "",
    response_model=TaskResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create new task",
    description="Create a new task with title and optional description/due date",
)
async def create_task(
    task_data: CreateTaskRequest,
    db: AsyncSession = Depends(get_db),
) -> Task:
    """Create a new task.

    Args:
        task_data: Task creation data (title, description, due_date)
        db: Database session from dependency injection

    Returns:
        Created task with all fields including generated ID and timestamps

    Raises:
        HTTPException: 400 if validation fails, 500 if database error
    """
    try:
        # Generate UUIDs for id and user_id
        task_id = uuid4()
        user_id = uuid4()  # Placeholder until authentication is implemented

        # Create task instance
        task = Task(
            id=task_id,
            user_id=user_id,
            title=task_data.title,
            description=task_data.description,
            due_date=task_data.due_date,
            completed=False,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
        )

        # Save to database
        db.add(task)
        await db.commit()
        await db.refresh(task)

        structured_logger.log(
            "INFO",
            "Task created",
            task_id=str(task.id),
            title=task.title,
        )

        return task

    except Exception as e:
        structured_logger.log(
            "ERROR",
            "Failed to create task",
            error=str(e),
            error_type=type(e).__name__,
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create task",
        )


@router.get(
    "",
    response_model=List[TaskResponse],
    status_code=status.HTTP_200_OK,
    summary="List all tasks",
    description="Retrieve all tasks in the system",
)
async def list_tasks(
    db: AsyncSession = Depends(get_db),
) -> List[Task]:
    """List all tasks.

    Args:
        db: Database session from dependency injection

    Returns:
        List of all tasks in the database

    Raises:
        HTTPException: 500 if database error
    """
    try:
        result = await db.execute(select(Task))
        tasks = result.scalars().all()

        structured_logger.log(
            "INFO",
            "Tasks retrieved",
            count=len(tasks),
        )

        return list(tasks)

    except Exception as e:
        structured_logger.log(
            "ERROR",
            "Failed to retrieve tasks",
            error=str(e),
            error_type=type(e).__name__,
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve tasks",
        )


@router.get(
    "/{task_id}",
    response_model=TaskResponse,
    status_code=status.HTTP_200_OK,
    summary="Get single task",
    description="Retrieve a specific task by its ID",
)
async def get_task(
    task_id: UUID,
    db: AsyncSession = Depends(get_db),
) -> Task:
    """Get a single task by ID.

    Args:
        task_id: UUID of the task to retrieve
        db: Database session from dependency injection

    Returns:
        Task with the specified ID

    Raises:
        HTTPException: 404 if task not found, 422 if invalid UUID, 500 if database error
    """
    try:
        result = await db.execute(select(Task).where(Task.id == task_id))  # type: ignore[arg-type]
        task = result.scalar_one_or_none()

        if task is None:
            structured_logger.log(
                "ERROR",
                "Task not found",
                task_id=str(task_id),
            )
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Task not found",
            )

        structured_logger.log(
            "INFO",
            "Task retrieved",
            task_id=str(task.id),
            title=task.title,
        )

        return task

    except HTTPException:
        raise
    except Exception as e:
        structured_logger.log(
            "ERROR",
            "Failed to retrieve task",
            task_id=str(task_id),
            error=str(e),
            error_type=type(e).__name__,
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve task",
        )


@router.put(
    "/{task_id}",
    response_model=TaskResponse,
    status_code=status.HTTP_200_OK,
    summary="Update task",
    description="Update all fields of an existing task",
)
async def update_task(
    task_id: UUID,
    task_data: UpdateTaskRequest,
    db: AsyncSession = Depends(get_db),
) -> Task:
    """Update an existing task.

    Args:
        task_id: UUID of the task to update
        task_data: Task update data (all fields optional)
        db: Database session from dependency injection

    Returns:
        Updated task with new values

    Raises:
        HTTPException: 404 if task not found, 400 if validation fails, 500 if database error
    """
    try:
        # Fetch existing task
        result = await db.execute(select(Task).where(Task.id == task_id))  # type: ignore[arg-type]
        task = result.scalar_one_or_none()

        if task is None:
            structured_logger.log(
                "ERROR",
                "Task not found for update",
                task_id=str(task_id),
            )
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Task not found",
            )

        # Update provided fields
        update_data = task_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(task, field, value)

        # Update timestamp
        task.updated_at = datetime.utcnow()

        await db.commit()
        await db.refresh(task)

        structured_logger.log(
            "INFO",
            "Task updated",
            task_id=str(task.id),
            updated_fields=list(update_data.keys()),
        )

        return task

    except HTTPException:
        raise
    except Exception as e:
        structured_logger.log(
            "ERROR",
            "Failed to update task",
            task_id=str(task_id),
            error=str(e),
            error_type=type(e).__name__,
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update task",
        )


@router.delete(
    "/{task_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete task",
    description="Delete a task by its ID",
)
async def delete_task(
    task_id: UUID,
    db: AsyncSession = Depends(get_db),
) -> None:
    """Delete a task.

    Args:
        task_id: UUID of the task to delete
        db: Database session from dependency injection

    Returns:
        None (204 No Content)

    Raises:
        HTTPException: 404 if task not found, 500 if database error
    """
    try:
        # Fetch existing task
        result = await db.execute(select(Task).where(Task.id == task_id))  # type: ignore[arg-type]
        task = result.scalar_one_or_none()

        if task is None:
            structured_logger.log(
                "ERROR",
                "Task not found for deletion",
                task_id=str(task_id),
            )
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Task not found",
            )

        # Delete task
        await db.delete(task)
        await db.commit()

        structured_logger.log(
            "INFO",
            "Task deleted",
            task_id=str(task_id),
        )

    except HTTPException:
        raise
    except Exception as e:
        structured_logger.log(
            "ERROR",
            "Failed to delete task",
            task_id=str(task_id),
            error=str(e),
            error_type=type(e).__name__,
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete task",
        )


@router.patch(
    "/{task_id}/complete",
    response_model=TaskResponse,
    status_code=status.HTTP_200_OK,
    summary="Toggle task completion",
    description="Toggle the completion status of a task (completed ↔ incomplete)",
)
async def toggle_task_completion(
    task_id: UUID,
    db: AsyncSession = Depends(get_db),
) -> Task:
    """Toggle task completion status.

    Args:
        task_id: UUID of the task to toggle
        db: Database session from dependency injection

    Returns:
        Updated task with toggled completion status

    Raises:
        HTTPException: 404 if task not found, 500 if database error
    """
    try:
        # Fetch existing task
        result = await db.execute(select(Task).where(Task.id == task_id))  # type: ignore[arg-type]
        task = result.scalar_one_or_none()

        if task is None:
            structured_logger.log(
                "ERROR",
                "Task not found for completion toggle",
                task_id=str(task_id),
            )
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Task not found",
            )

        # Toggle completion status
        task.completed = not task.completed
        task.updated_at = datetime.utcnow()

        await db.commit()
        await db.refresh(task)

        structured_logger.log(
            "INFO",
            "Task completion toggled",
            task_id=str(task.id),
            completed=task.completed,
        )

        return task

    except HTTPException:
        raise
    except Exception as e:
        structured_logger.log(
            "ERROR",
            "Failed to toggle task completion",
            task_id=str(task_id),
            error=str(e),
            error_type=type(e).__name__,
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to toggle task completion",
        )
