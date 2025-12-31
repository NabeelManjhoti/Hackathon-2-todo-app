import pytest
from src.models.task import Task, TaskCreate, TaskRead, TaskUpdate
from datetime import datetime
import uuid


def test_task_model_creation():
    """Test creating a Task model instance."""
    task_id = uuid.uuid4()
    user_id = uuid.uuid4()

    task = Task(
        id=task_id,
        title="Test Task",
        description="Test Description",
        completed=False,
        user_id=user_id
    )

    assert task.id == task_id
    assert task.title == "Test Task"
    assert task.description == "Test Description"
    assert task.completed == False
    assert task.user_id == user_id
    assert isinstance(task.created_at, datetime)
    assert isinstance(task.updated_at, datetime)


def test_task_create_model():
    """Test creating a TaskCreate model instance."""
    task_create = TaskCreate(
        title="New Task",
        description="New Description",
        completed=True
    )

    assert task_create.title == "New Task"
    assert task_create.description == "New Description"
    assert task_create.completed == True


def test_task_read_model():
    """Test creating a TaskRead model instance."""
    task_id = uuid.uuid4()
    user_id = uuid.uuid4()
    task_read = TaskRead(
        id=task_id,
        title="Read Task",
        description="Read Description",
        completed=False,
        user_id=user_id,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )

    assert task_read.id == task_id
    assert task_read.title == "Read Task"
    assert task_read.description == "Read Description"
    assert task_read.completed == False
    assert task_read.user_id == user_id
    assert isinstance(task_read.created_at, datetime)
    assert isinstance(task_read.updated_at, datetime)


def test_task_update_model():
    """Test creating a TaskUpdate model instance."""
    task_update = TaskUpdate(
        title="Updated Title",
        description="Updated Description",
        completed=True
    )

    assert task_update.title == "Updated Title"
    assert task_update.description == "Updated Description"
    assert task_update.completed == True


def test_task_default_values():
    """Test default values for Task model."""
    task_id = uuid.uuid4()
    user_id = uuid.uuid4()

    task = Task(
        id=task_id,
        title="Test Task",
        user_id=user_id
    )

    # Check default values
    assert task.completed == False
    assert task.description is None
    assert isinstance(task.created_at, datetime)
    assert isinstance(task.updated_at, datetime)