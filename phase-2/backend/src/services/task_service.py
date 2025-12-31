from sqlmodel import Session, select
from typing import List, Optional
from ..models.task import Task, TaskCreate, TaskUpdate
from ..models.user import User


def create_task(session: Session, task_create: TaskCreate, user_id: str) -> Task:
    """
    Create a new task for a user.
    """
    db_task = Task(
        title=task_create.title,
        description=task_create.description,
        completed=task_create.completed,
        user_id=user_id
    )
    session.add(db_task)
    session.commit()
    session.refresh(db_task)
    return db_task


def get_tasks(session: Session, user_id: str) -> List[Task]:
    """
    Get all tasks for a user.
    """
    tasks = session.exec(
        select(Task).where(Task.user_id == user_id)
    ).all()
    return tasks


def get_task(session: Session, task_id: str, user_id: str) -> Optional[Task]:
    """
    Get a specific task by ID for a user.
    """
    task = session.exec(
        select(Task).where(Task.id == task_id, Task.user_id == user_id)
    ).first()
    return task


def update_task(session: Session, task_id: str, task_update: TaskUpdate, user_id: str) -> Optional[Task]:
    """
    Update a task for a user.
    """
    db_task = session.exec(
        select(Task).where(Task.id == task_id, Task.user_id == user_id)
    ).first()

    if not db_task:
        return None

    # Update only fields that are provided
    for field, value in task_update.dict(exclude_unset=True).items():
        setattr(db_task, field, value)

    session.add(db_task)
    session.commit()
    session.refresh(db_task)
    return db_task


def delete_task(session: Session, task_id: str, user_id: str) -> bool:
    """
    Delete a task for a user.
    """
    db_task = session.exec(
        select(Task).where(Task.id == task_id, Task.user_id == user_id)
    ).first()

    if not db_task:
        return False

    session.delete(db_task)
    session.commit()
    return True