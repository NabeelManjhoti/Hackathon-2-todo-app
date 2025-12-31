import pytest
from sqlmodel import Session, select
from src.models.user import User, UserCreate
from src.models.task import Task, TaskCreate, TaskUpdate
from src.services.task_service import (
    create_task,
    get_tasks,
    get_task,
    update_task,
    delete_task
)
from src.services.auth_service import create_user
import uuid


def test_create_task(session: Session):
    """Test creating a new task."""
    # Create a user first
    user_create = UserCreate(
        email="test@example.com",
        password="securepassword"
    )
    user = create_user(session, user_create)

    # Create a task for the user
    task_create = TaskCreate(
        title="Test Task",
        description="Test Description",
        completed=False
    )
    created_task = create_task(session, task_create, user.id)

    # Check that the task was created
    assert created_task.title == "Test Task"
    assert created_task.description == "Test Description"
    assert created_task.completed == False
    assert created_task.user_id == user.id

    # Verify task exists in database
    db_task = session.get(Task, created_task.id)
    assert db_task is not None
    assert db_task.title == created_task.title


def test_get_tasks(session: Session):
    """Test getting all tasks for a user."""
    # Create users
    user1_create = UserCreate(email="user1@example.com", password="password")
    user2_create = UserCreate(email="user2@example.com", password="password")
    user1 = create_user(session, user1_create)
    user2 = create_user(session, user2_create)

    # Create tasks for user1
    task1_create = TaskCreate(title="User1 Task 1", description="Description 1", completed=False)
    task2_create = TaskCreate(title="User1 Task 2", description="Description 2", completed=True)
    create_task(session, task1_create, user1.id)
    create_task(session, task2_create, user1.id)

    # Create tasks for user2
    task3_create = TaskCreate(title="User2 Task 1", description="Description 3", completed=False)
    create_task(session, task3_create, user2.id)

    # Get tasks for user1
    user1_tasks = get_tasks(session, user1.id)
    assert len(user1_tasks) == 2
    assert all(task.user_id == user1.id for task in user1_tasks)

    # Get tasks for user2
    user2_tasks = get_tasks(session, user2.id)
    assert len(user2_tasks) == 1
    assert user2_tasks[0].user_id == user2.id


def test_get_task(session: Session):
    """Test getting a specific task by ID for a user."""
    # Create a user
    user_create = UserCreate(email="test@example.com", password="password")
    user = create_user(session, user_create)

    # Create a task for the user
    task_create = TaskCreate(title="Test Task", description="Description", completed=False)
    created_task = create_task(session, task_create, str(user.id))

    # Get the task for the correct user
    retrieved_task = get_task(session, str(created_task.id), str(user.id))
    assert retrieved_task is not None
    assert retrieved_task.id == created_task.id
    assert retrieved_task.title == "Test Task"

    # Try to get the task for a different user (should return None)
    other_user_create = UserCreate(email="other@example.com", password="password")
    other_user = create_user(session, other_user_create)
    other_retrieved_task = get_task(session, str(created_task.id), str(other_user.id))
    assert other_retrieved_task is None


def test_update_task(session: Session):
    """Test updating a task."""
    # Create a user
    user_create = UserCreate(email="test@example.com", password="password")
    user = create_user(session, user_create)

    # Create a task for the user
    task_create = TaskCreate(title="Original Title", description="Original Description", completed=False)
    created_task = create_task(session, task_create, str(user.id))

    # Update the task
    task_update = TaskUpdate(
        title="Updated Title",
        description="Updated Description",
        completed=True
    )
    updated_task = update_task(session, str(created_task.id), task_update, str(user.id))

    assert updated_task is not None
    assert updated_task.title == "Updated Title"
    assert updated_task.description == "Updated Description"
    assert updated_task.completed == True

    # Verify update in database
    db_task = session.get(Task, created_task.id)
    assert db_task.title == "Updated Title"
    assert db_task.description == "Updated Description"
    assert db_task.completed == True


def test_update_task_not_found(session: Session):
    """Test updating a task that doesn't exist."""
    # Create a user
    user_create = UserCreate(email="test@example.com", password="password")
    user = create_user(session, user_create)

    # Try to update a non-existent task
    task_update = TaskUpdate(title="Updated Title")
    updated_task = update_task(session, str(uuid.uuid4()), task_update, str(user.id))

    assert updated_task is None


def test_update_task_wrong_user(session: Session):
    """Test updating a task that belongs to a different user."""
    # Create users
    user1_create = UserCreate(email="user1@example.com", password="password")
    user2_create = UserCreate(email="user2@example.com", password="password")
    user1 = create_user(session, user1_create)
    user2 = create_user(session, user2_create)

    # Create a task for user1
    task_create = TaskCreate(title="User1 Task", description="Description", completed=False)
    created_task = create_task(session, task_create, str(user1.id))

    # Try to update the task as user2 (should fail)
    task_update = TaskUpdate(title="Updated Title")
    updated_task = update_task(session, str(created_task.id), task_update, str(user2.id))

    assert updated_task is None


def test_delete_task(session: Session):
    """Test deleting a task."""
    # Create a user
    user_create = UserCreate(email="test@example.com", password="password")
    user = create_user(session, user_create)

    # Create a task for the user
    task_create = TaskCreate(title="Test Task", description="Description", completed=False)
    created_task = create_task(session, task_create, str(user.id))

    # Verify task exists
    db_task = session.get(Task, created_task.id)
    assert db_task is not None

    # Delete the task
    delete_result = delete_task(session, str(created_task.id), str(user.id))
    assert delete_result is True

    # Verify task no longer exists
    db_task = session.get(Task, created_task.id)
    assert db_task is None


def test_delete_task_not_found(session: Session):
    """Test deleting a task that doesn't exist."""
    # Create a user
    user_create = UserCreate(email="test@example.com", password="password")
    user = create_user(session, user_create)

    # Try to delete a non-existent task
    delete_result = delete_task(session, str(uuid.uuid4()), str(user.id))
    assert delete_result is False


def test_delete_task_wrong_user(session: Session):
    """Test deleting a task that belongs to a different user."""
    # Create users
    user1_create = UserCreate(email="user1@example.com", password="password")
    user2_create = UserCreate(email="user2@example.com", password="password")
    user1 = create_user(session, user1_create)
    user2 = create_user(session, user2_create)

    # Create a task for user1
    task_create = TaskCreate(title="User1 Task", description="Description", completed=False)
    created_task = create_task(session, task_create, str(user1.id))

    # Try to delete the task as user2 (should fail)
    delete_result = delete_task(session, str(created_task.id), str(user2.id))
    assert delete_result is False

    # Verify task still exists
    db_task = session.get(Task, created_task.id)
    assert db_task is not None