"""Task CRUD endpoints with authentication and user isolation."""

from datetime import datetime
from typing import Annotated, List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.dependencies.auth import get_current_user
from src.dependencies.database import get_session
from src.logger import structured_logger
from src.models.task import Task
from src.models.user import User
from src.schemas.task import CreateTaskRequest, TaskResponse, UpdateTaskRequest

router = APIRouter(prefix="/api/tasks", tags=["tasks"])


@router.post(
    "",
    response_model=TaskResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create new task",
    description="Create a new task for the authenticated user",
)
async def create_task(
    task_data: CreateTaskRequest,
    current_user: Annotated[User, Depends(get_current_user)],
    session: Annotated[AsyncSession, Depends(get_session)],
) -> Task:
    """Create a new task for the authenticated user.

    Args:
        task_data: Task creation data (title, description, due_date)
        current_user: Authenticated user from JWT token
        session: Database session from dependency injection

    Returns:
        Created task with all fields including generated ID and timestamps

    Raises:
        HTTPException: 401 if not authenticated, 400 if validation fails
    """
    # Store user_id to avoid lazy loading issues
    user_id = current_user.id

    # Create task instance with authenticated user's ID
    task = Task(
        user_id=user_id,
        title=task_data.title,
        description=task_data.description,
        due_date=task_data.due_date,
        completed=False,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow(),
    )

    # Save to database
    session.add(task)
    await session.commit()
    await session.refresh(task)

    structured_logger.log(
        "INFO",
        "Task created",
        task_id=str(task.id),
        user_id=str(user_id),
        title=task.title,
    )

    # Convert to response model to avoid async serialization issues
    return TaskResponse.model_validate(task)


@router.get(
    "",
    response_model=List[TaskResponse],
    status_code=status.HTTP_200_OK,
    summary="List user's tasks",
    description="Retrieve all tasks belonging to the authenticated user",
)
async def list_tasks(
    current_user: Annotated[User, Depends(get_current_user)],
    session: Annotated[AsyncSession, Depends(get_session)],
) -> List[Task]:
    """List all tasks for the authenticated user.

    Args:
        current_user: Authenticated user from JWT token
        session: Database session from dependency injection

    Returns:
        List of tasks belonging to the authenticated user

    Raises:
        HTTPException: 401 if not authenticated
    """
    # Store user_id to avoid lazy loading issues
    user_id = current_user.id

    # Filter tasks by authenticated user's ID
    result = await session.execute(
        select(Task).where(Task.user_id == user_id)  # type: ignore[arg-type]
    )
    tasks = result.scalars().all()

    structured_logger.log(
        "INFO",
        "Tasks retrieved",
        user_id=str(user_id),
        count=len(tasks),
    )

    # Convert to response models to avoid async serialization issues
    return [TaskResponse.model_validate(task) for task in tasks]


@router.get(
    "/{task_id}",
    response_model=TaskResponse,
    status_code=status.HTTP_200_OK,
    summary="Get single task",
    description="Retrieve a specific task (must be owned by authenticated user)",
)
async def get_task(
    task_id: UUID,
    current_user: Annotated[User, Depends(get_current_user)],
    session: Annotated[AsyncSession, Depends(get_session)],
) -> Task:
    """Get a single task by ID (with ownership verification).

    Args:
        task_id: UUID of the task to retrieve
        current_user: Authenticated user from JWT token
        session: Database session from dependency injection

    Returns:
        Task with the specified ID

    Raises:
        HTTPException: 401 if not authenticated, 403 if not owner, 404 if not found
    """
    # Store user_id to avoid lazy loading issues
    user_id = current_user.id

    result = await session.execute(select(Task).where(Task.id == task_id))  # type: ignore[arg-type]
    task = result.scalar_one_or_none()

    if task is None:
        structured_logger.log(
            "ERROR",
            "Task not found",
            task_id=str(task_id),
            user_id=str(user_id),
        )
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found",
        )

    # Verify ownership
    if task.user_id != user_id:
        structured_logger.log(
            "WARNING",
            "Unauthorized task access attempt",
            task_id=str(task_id),
            task_owner=str(task.user_id),
            requesting_user=str(user_id),
        )
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this task",
        )

    structured_logger.log(
        "INFO",
        "Task retrieved",
        task_id=str(task.id),
        user_id=str(user_id),
    )

    # Convert to response model to avoid async serialization issues
    return TaskResponse.model_validate(task)


@router.put(
    "/{task_id}",
    response_model=TaskResponse,
    status_code=status.HTTP_200_OK,
    summary="Update task",
    description="Update a task (must be owned by authenticated user)",
)
async def update_task(
    task_id: UUID,
    task_data: UpdateTaskRequest,
    current_user: Annotated[User, Depends(get_current_user)],
    session: Annotated[AsyncSession, Depends(get_session)],
) -> Task:
    """Update an existing task (with ownership verification).

    Args:
        task_id: UUID of the task to update
        task_data: Task update data (all fields optional)
        current_user: Authenticated user from JWT token
        session: Database session from dependency injection

    Returns:
        Updated task with new values

    Raises:
        HTTPException: 401 if not authenticated, 403 if not owner, 404 if not found
    """
    # Store user_id to avoid lazy loading issues
    user_id = current_user.id

    # Fetch existing task
    result = await session.execute(select(Task).where(Task.id == task_id))  # type: ignore[arg-type]
    task = result.scalar_one_or_none()

    if task is None:
        structured_logger.log(
            "ERROR",
            "Task not found for update",
            task_id=str(task_id),
            user_id=str(user_id),
        )
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found",
        )

    # Verify ownership
    if task.user_id != user_id:
        structured_logger.log(
            "WARNING",
            "Unauthorized task update attempt",
            task_id=str(task_id),
            task_owner=str(task.user_id),
            requesting_user=str(user_id),
        )
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this task",
        )

    # Update provided fields
    update_data = task_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(task, field, value)

    # Update timestamp
    task.updated_at = datetime.utcnow()

    await session.commit()
    await session.refresh(task)

    structured_logger.log(
        "INFO",
        "Task updated",
        task_id=str(task.id),
        user_id=str(user_id),
        updated_fields=list(update_data.keys()),
    )

    # Convert to response model to avoid async serialization issues
    return TaskResponse.model_validate(task)


@router.delete(
    "/{task_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete task",
    description="Delete a task (must be owned by authenticated user)",
)
async def delete_task(
    task_id: UUID,
    current_user: Annotated[User, Depends(get_current_user)],
    session: Annotated[AsyncSession, Depends(get_session)],
) -> None:
    """Delete a task (with ownership verification).

    Args:
        task_id: UUID of the task to delete
        current_user: Authenticated user from JWT token
        session: Database session from dependency injection

    Returns:
        None (204 No Content)

    Raises:
        HTTPException: 401 if not authenticated, 403 if not owner, 404 if not found
    """
    # Store user_id to avoid lazy loading issues
    user_id = current_user.id

    # Fetch existing task
    result = await session.execute(select(Task).where(Task.id == task_id))  # type: ignore[arg-type]
    task = result.scalar_one_or_none()

    if task is None:
        structured_logger.log(
            "ERROR",
            "Task not found for deletion",
            task_id=str(task_id),
            user_id=str(user_id),
        )
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found",
        )

    # Verify ownership
    if task.user_id != user_id:
        structured_logger.log(
            "WARNING",
            "Unauthorized task deletion attempt",
            task_id=str(task_id),
            task_owner=str(task.user_id),
            requesting_user=str(user_id),
        )
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this task",
        )

    # Delete task
    await session.delete(task)
    await session.commit()

    structured_logger.log(
        "INFO",
        "Task deleted",
        task_id=str(task_id),
        user_id=str(user_id),
    )


@router.patch(
    "/{task_id}/complete",
    response_model=TaskResponse,
    status_code=status.HTTP_200_OK,
    summary="Toggle task completion",
    description="Toggle completion status (must be owned by authenticated user)",
)
async def toggle_task_completion(
    task_id: UUID,
    current_user: Annotated[User, Depends(get_current_user)],
    session: Annotated[AsyncSession, Depends(get_session)],
) -> Task:
    """Toggle task completion status (with ownership verification).

    Args:
        task_id: UUID of the task to toggle
        current_user: Authenticated user from JWT token
        session: Database session from dependency injection

    Returns:
        Updated task with toggled completion status

    Raises:
        HTTPException: 401 if not authenticated, 403 if not owner, 404 if not found
    """
    # Store user_id to avoid lazy loading issues
    user_id = current_user.id

    # Fetch existing task
    result = await session.execute(select(Task).where(Task.id == task_id))  # type: ignore[arg-type]
    task = result.scalar_one_or_none()

    if task is None:
        structured_logger.log(
            "ERROR",
            "Task not found for completion toggle",
            task_id=str(task_id),
            user_id=str(user_id),
        )
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found",
        )

    # Verify ownership
    if task.user_id != user_id:
        structured_logger.log(
            "WARNING",
            "Unauthorized task completion toggle attempt",
            task_id=str(task_id),
            task_owner=str(task.user_id),
            requesting_user=str(user_id),
        )
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this task",
        )

    # Toggle completion status
    task.completed = not task.completed
    task.updated_at = datetime.utcnow()

    await session.commit()
    await session.refresh(task)

    structured_logger.log(
        "INFO",
        "Task completion toggled",
        task_id=str(task.id),
        user_id=str(user_id),
        completed=task.completed,
    )

    # Convert to response model to avoid async serialization issues
    return TaskResponse.model_validate(task)
