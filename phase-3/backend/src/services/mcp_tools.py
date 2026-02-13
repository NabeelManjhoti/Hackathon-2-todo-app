"""MCP tools for task management operations."""

from datetime import datetime
from typing import Dict, Any, Optional
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.task import Task
from src.services.tool_response import success_response, error_response
from src.logger import structured_logger


async def add_task(
    session: AsyncSession,
    user_id: str,
    title: str,
    description: str = ""
) -> Dict[str, Any]:
    """Create a new task for the user.

    Args:
        session: Database session
        user_id: User ID (UUID string)
        title: Task title
        description: Optional task description

    Returns:
        Tool response with status, message, and task data
    """
    try:
        # Validate user_id format
        try:
            user_uuid = UUID(user_id)
        except ValueError:
            return error_response("Invalid user ID format")

        # Create task
        task = Task(
            user_id=user_uuid,
            title=title.strip(),
            description=description.strip() if description else None,
            completed=False,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
        )

        session.add(task)
        await session.commit()
        await session.refresh(task)

        structured_logger.log(
            "INFO",
            "Task created via MCP tool",
            task_id=str(task.id),
            user_id=user_id,
            title=task.title,
        )

        return success_response(
            message=f"Task '{title}' created successfully",
            data={
                "task_id": str(task.id),
                "title": task.title,
                "description": task.description,
                "completed": task.completed,
            }
        )

    except Exception as e:
        structured_logger.log("ERROR", "Failed to create task", error=str(e))
        return error_response(f"Failed to create task: {str(e)}")


async def list_tasks(
    session: AsyncSession,
    user_id: str,
    status_filter: str = "all"
) -> Dict[str, Any]:
    """List all tasks for the user.

    Args:
        session: Database session
        user_id: User ID (UUID string)
        status_filter: Filter by status - "all", "active", or "completed"

    Returns:
        Tool response with status, message, and tasks list
    """
    try:
        # Validate user_id format
        try:
            user_uuid = UUID(user_id)
        except ValueError:
            return error_response("Invalid user ID format")

        # Build query
        query = select(Task).where(Task.user_id == user_uuid)

        # Apply status filter
        if status_filter == "active":
            query = query.where(Task.completed == False)
        elif status_filter == "completed":
            query = query.where(Task.completed == True)
        # "all" - no additional filter

        # Order by created_at descending (newest first)
        query = query.order_by(Task.created_at.desc())

        # Execute query
        result = await session.execute(query)
        tasks = result.scalars().all()

        # Format tasks for response
        tasks_data = [
            {
                "id": str(task.id),
                "title": task.title,
                "description": task.description,
                "completed": task.completed,
                "created_at": task.created_at.isoformat(),
            }
            for task in tasks
        ]

        # Create message
        count = len(tasks_data)
        if count == 0:
            message = f"No {status_filter} tasks found"
        elif count == 1:
            message = f"Found 1 {status_filter} task"
        else:
            message = f"Found {count} {status_filter} tasks"

        return success_response(
            message=message,
            data={
                "tasks": tasks_data,
                "count": count,
                "filter": status_filter,
            }
        )

    except Exception as e:
        structured_logger.log("ERROR", "Failed to list tasks", error=str(e))
        return error_response(f"Failed to list tasks: {str(e)}")


async def complete_task(
    session: AsyncSession,
    user_id: str,
    task_id: str
) -> Dict[str, Any]:
    """Mark a task as completed.

    Args:
        session: Database session
        user_id: User ID (UUID string)
        task_id: Task ID (UUID string)

    Returns:
        Tool response with status and message
    """
    try:
        # Validate UUIDs
        try:
            user_uuid = UUID(user_id)
            task_uuid = UUID(task_id)
        except ValueError:
            return error_response("Invalid user ID or task ID format")

        # Find task with user isolation
        query = select(Task).where(
            Task.id == task_uuid,
            Task.user_id == user_uuid
        )
        result = await session.execute(query)
        task = result.scalar_one_or_none()

        if not task:
            return error_response(
                "Task not found or you don't have permission to access it"
            )

        # Check if already completed
        if task.completed:
            return success_response(
                message=f"Task '{task.title}' was already completed",
                data={"task_id": str(task.id), "title": task.title}
            )

        # Mark as completed
        task.completed = True
        task.updated_at = datetime.utcnow()
        await session.commit()

        structured_logger.log(
            "INFO",
            "Task completed via MCP tool",
            task_id=str(task.id),
            user_id=user_id,
            title=task.title,
        )

        return success_response(
            message=f"Task '{task.title}' marked as completed",
            data={"task_id": str(task.id), "title": task.title}
        )

    except Exception as e:
        structured_logger.log("ERROR", "Failed to complete task", error=str(e))
        return error_response(f"Failed to complete task: {str(e)}")
