import pytest
from src.models.user import User, UserCreate, UserRead, UserUpdate
from datetime import datetime
import uuid


def test_user_model_creation():
    """Test creating a User model instance."""
    user_id = uuid.uuid4()
    email = "test@example.com"
    password_hash = "hashed_password"

    user = User(
        id=user_id,
        email=email,
        password_hash=password_hash,
        first_name="Test",
        last_name="User"
    )

    assert user.id == user_id
    assert user.email == email
    assert user.password_hash == password_hash
    assert user.first_name == "Test"
    assert user.last_name == "User"
    assert isinstance(user.created_at, datetime)
    assert isinstance(user.updated_at, datetime)


def test_user_create_model():
    """Test creating a UserCreate model instance."""
    user_create = UserCreate(
        email="test@example.com",
        password="securepassword",
        first_name="Test",
        last_name="User"
    )

    assert user_create.email == "test@example.com"
    assert user_create.password == "securepassword"
    assert user_create.first_name == "Test"
    assert user_create.last_name == "User"


def test_user_read_model():
    """Test creating a UserRead model instance."""
    user_id = uuid.uuid4()
    user_read = UserRead(
        id=user_id,
        email="test@example.com",
        first_name="Test",
        last_name="User",
        created_at=datetime.utcnow()
    )

    assert user_read.id == user_id
    assert user_read.email == "test@example.com"
    assert user_read.first_name == "Test"
    assert user_read.last_name == "User"
    assert isinstance(user_read.created_at, datetime)


def test_user_update_model():
    """Test creating a UserUpdate model instance."""
    user_update = UserUpdate(
        first_name="Updated",
        last_name="Name"
    )

    assert user_update.first_name == "Updated"
    assert user_update.last_name == "Name"