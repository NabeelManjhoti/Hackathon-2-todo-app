from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlmodel import Session
from typing import List
from ..database.session import get_session
from ..models.task import Task, TaskCreate, TaskRead, TaskUpdate
from ..models.user import User
from ..services.task_service import create_task, get_tasks, get_task, update_task, delete_task
from jose import jwt
from ..config.settings import settings


router = APIRouter()


def get_current_user_from_token(token: str) -> dict:
    """
    Get current user from JWT token.
    """
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
        user_id: str = payload.get("sub")
        email: str = payload.get("email")

        if user_id is None or email is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials"
            )

        return {"user_id": user_id, "email": email}
    except jwt.JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials"
        )


async def get_current_user(request: Request) -> dict:
    """
    Get current user from the Authorization header.
    """
    auth_header = request.headers.get("Authorization")

    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )

    token = auth_header.split(" ")[1]
    return get_current_user_from_token(token)


@router.post("/tasks/", response_model=TaskRead, status_code=status.HTTP_201_CREATED)
async def create_new_task(
    task_create: TaskCreate,
    current_user: dict = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Create a new task for the authenticated user.
    """
    db_task = create_task(session, task_create, current_user["user_id"])
    return db_task


@router.get("/tasks/", response_model=List[TaskRead])
async def read_tasks(
    current_user: dict = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Get all tasks for the authenticated user.
    """
    tasks = get_tasks(session, current_user["user_id"])
    return tasks


@router.get("/tasks/{task_id}", response_model=TaskRead)
async def read_task(
    task_id: str,
    current_user: dict = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Get a specific task by ID for the authenticated user.
    """
    task = get_task(session, task_id, current_user["user_id"])
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )
    return task


@router.put("/tasks/{task_id}", response_model=TaskRead)
async def update_existing_task(
    task_id: str,
    task_update: TaskUpdate,
    current_user: dict = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Update a task for the authenticated user.
    """
    updated_task = update_task(session, task_id, task_update, current_user["user_id"])
    if not updated_task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )
    return updated_task


@router.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_existing_task(
    task_id: str,
    current_user: dict = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Delete a task for the authenticated user.
    """
    success = delete_task(session, task_id, current_user["user_id"])
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )
    return