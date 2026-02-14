"""MCP tools for task management operations.

This module provides Model Context Protocol (MCP) tools for natural language task management.
All tools enforce strict user isolation and return structured responses.

Tool Response Format:
    {
        "status": "success" | "error",
        "message": "Human-readable message",
        "data": {...} | None
    }

Security:
    - All tools validate user_id to ensure data isolation
    - UUID validation prevents injection attacks
    - SQLModel parameterized queries prevent SQL injection
    - User ownership verified before any data access or modification
"""

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


async def update_task(
    session: AsyncSession,
    user_id: str,
    task_id: str,
    title: Optional[str] = None,
    description: Optional[str] = None,
    due_date: Optional[str] = None
) -> Dict[str, Any]:
    """Update a task's title, description, or due date.

    Args:
        session: Database session
        user_id: User ID (UUID string)
        task_id: Task ID (UUID string)
        title: New task title (optional)
        description: New task description (optional)
        due_date: New due date in ISO format (optional)

    Returns:
        Tool response with status, message, and updated task data
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

        # Track what was updated
        updates = []

        # Update title if provided
        if title is not None:
            title_stripped = title.strip()
            if not title_stripped:
                return error_response("Task title cannot be empty")
            task.title = title_stripped
            updates.append("title")

        # Update description if provided
        if description is not None:
            task.description = description.strip() if description else None
            updates.append("description")

        # Update due_date if provided
        if due_date is not None:
            if due_date:
                try:
                    task.due_date = datetime.fromisoformat(due_date.replace('Z', '+00:00'))
                    updates.append("due date")
                except ValueError:
                    return error_response("Invalid due date format. Use ISO format (YYYY-MM-DD or YYYY-MM-DDTHH:MM:SS)")
            else:
                task.due_date = None
                updates.append("due date (removed)")

        # Check if anything was updated
        if not updates:
            return error_response("No fields provided to update")

        # Update timestamp and commit
        task.updated_at = datetime.utcnow()
        await session.commit()
        await session.refresh(task)

        structured_logger.log(
            "INFO",
            "Task updated via MCP tool",
            task_id=str(task.id),
            user_id=user_id,
            updates=updates,
        )

        return success_response(
            message=f"Task '{task.title}' updated successfully ({', '.join(updates)})",
            data={
                "task_id": str(task.id),
                "title": task.title,
                "description": task.description,
                "due_date": task.due_date.isoformat() if task.due_date else None,
                "completed": task.completed,
                "updated_fields": updates,
            }
        )

    except Exception as e:
        structured_logger.log("ERROR", "Failed to update task", error=str(e))
        return error_response(f"Failed to update task: {str(e)}")


async def delete_task(
    session: AsyncSession,
    user_id: str,
    task_id: str
) -> Dict[str, Any]:
    """Delete a task permanently.

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

        # Store task title for confirmation message
        task_title = task.title

        # Delete task
        await session.delete(task)
        await session.commit()

        structured_logger.log(
            "INFO",
            "Task deleted via MCP tool",
            task_id=str(task_id),
            user_id=user_id,
            title=task_title,
        )

        return success_response(
            message=f"Task '{task_title}' deleted successfully",
            data={"task_id": str(task_id), "title": task_title}
        )

    except Exception as e:
        structured_logger.log("ERROR", "Failed to delete task", error=str(e))
        return error_response(f"Failed to delete task: {str(e)}")
