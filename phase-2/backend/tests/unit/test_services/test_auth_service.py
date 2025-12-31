import pytest
from sqlmodel import Session, select
from src.models.user import User, UserCreate
from src.services.auth_service import (
    verify_password,
    get_password_hash,
    authenticate_user,
    create_access_token,
    get_user_by_email,
    create_user
)
from datetime import timedelta


def test_password_hashing():
    """Test password hashing and verification."""
    plain_password = "testpassword"
    hashed = get_password_hash(plain_password)

    # Verify the password
    assert verify_password(plain_password, hashed)
    assert not verify_password("wrongpassword", hashed)


def test_create_user(session: Session):
    """Test creating a new user."""
    user_create = UserCreate(
        email="test@example.com",
        password="securepassword",
        first_name="Test",
        last_name="User"
    )

    created_user = create_user(session, user_create)

    # Check that the user was created
    assert created_user.email == "test@example.com"
    assert created_user.first_name == "Test"
    assert created_user.last_name == "User"
    assert verify_password("securepassword", created_user.password_hash)

    # Verify user exists in database
    db_user = session.exec(select(User).where(User.email == "test@example.com")).first()
    assert db_user is not None
    assert db_user.email == created_user.email


def test_get_user_by_email(session: Session):
    """Test getting a user by email."""
    # Create a user first
    user_create = UserCreate(
        email="test@example.com",
        password="securepassword"
    )
    created_user = create_user(session, user_create)

    # Retrieve the user by email
    retrieved_user = get_user_by_email(session, "test@example.com")

    assert retrieved_user is not None
    assert retrieved_user.id == created_user.id
    assert retrieved_user.email == "test@example.com"


def test_authenticate_user_success(session: Session):
    """Test successful user authentication."""
    # Create a user
    user_create = UserCreate(
        email="test@example.com",
        password="securepassword"
    )
    created_user = create_user(session, user_create)

    # Authenticate with correct credentials
    authenticated_user = authenticate_user(session, "test@example.com", "securepassword")

    assert authenticated_user is not None
    assert authenticated_user.id == created_user.id
    assert authenticated_user.email == "test@example.com"


def test_authenticate_user_failure(session: Session):
    """Test failed user authentication."""
    # Create a user
    user_create = UserCreate(
        email="test@example.com",
        password="securepassword"
    )
    created_user = create_user(session, user_create)

    # Try to authenticate with wrong password
    authenticated_user = authenticate_user(session, "test@example.com", "wrongpassword")

    assert authenticated_user is None

    # Try to authenticate with non-existent email
    authenticated_user = authenticate_user(session, "nonexistent@example.com", "securepassword")

    assert authenticated_user is None


def test_create_access_token():
    """Test creating an access token."""
    data = {"sub": "user123", "email": "test@example.com"}
    token = create_access_token(data=data)

    # Just verify that a token was created (it should be a string)
    assert isinstance(token, str)
    assert len(token) > 0


def test_create_access_token_with_expiration():
    """Test creating an access token with custom expiration."""
    data = {"sub": "user123", "email": "test@example.com"}
    expires_delta = timedelta(minutes=15)
    token = create_access_token(data=data, expires_delta=expires_delta)

    # Just verify that a token was created
    assert isinstance(token, str)
    assert len(token) > 0