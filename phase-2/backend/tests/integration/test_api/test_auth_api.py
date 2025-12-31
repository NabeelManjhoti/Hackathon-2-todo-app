import pytest
from fastapi.testclient import TestClient


def test_register_user(client: TestClient):
    """Test user registration endpoint."""
    response = client.post(
        "/api/v1/auth/register",
        json={
            "email": "test@example.com",
            "password": "securepassword",
            "first_name": "Test",
            "last_name": "User"
        }
    )

    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "test@example.com"
    assert data["first_name"] == "Test"
    assert data["last_name"] == "User"
    assert "id" in data
    assert "created_at" in data


def test_register_user_duplicate(client: TestClient):
    """Test registering a user with an existing email."""
    # Register the first user
    client.post(
        "/api/v1/auth/register",
        json={
            "email": "duplicate@example.com",
            "password": "securepassword"
        }
    )

    # Try to register with the same email
    response = client.post(
        "/api/v1/auth/register",
        json={
            "email": "duplicate@example.com",
            "password": "anotherpassword"
        }
    )

    assert response.status_code == 409  # Conflict


def test_login_user(client: TestClient):
    """Test user login endpoint."""
    # Register a user first
    client.post(
        "/api/v1/auth/register",
        json={
            "email": "login@example.com",
            "password": "securepassword"
        }
    )

    # Login with correct credentials
    response = client.post(
        "/api/v1/auth/login",
        data={
            "email": "login@example.com",
            "password": "securepassword"
        }
    )

    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"
    assert "user" in data
    assert data["user"]["email"] == "login@example.com"


def test_login_user_invalid_credentials(client: TestClient):
    """Test login with invalid credentials."""
    # Register a user first
    client.post(
        "/api/v1/auth/register",
        json={
            "email": "login@example.com",
            "password": "securepassword"
        }
    )

    # Login with wrong password
    response = client.post(
        "/api/v1/auth/login",
        data={
            "email": "login@example.com",
            "password": "wrongpassword"
        }
    )

    assert response.status_code == 401


def test_login_user_nonexistent(client: TestClient):
    """Test login with non-existent user."""
    response = client.post(
        "/api/v1/auth/login",
        data={
            "email": "nonexistent@example.com",
            "password": "securepassword"
        }
    )

    assert response.status_code == 401


def test_verify_token(client: TestClient):
    """Test token verification endpoint."""
    # Register and login to get a token
    client.post(
        "/api/v1/auth/register",
        json={
            "email": "verify@example.com",
            "password": "securepassword"
        }
    )

    login_response = client.post(
        "/api/v1/auth/login",
        data={
            "email": "verify@example.com",
            "password": "securepassword"
        }
    )

    token = login_response.json()["access_token"]

    # Verify the token
    response = client.post(
        "/api/v1/auth/verify",
        json={"token": token}
    )

    assert response.status_code == 200
    data = response.json()
    assert data["valid"] is True
    assert "user_id" in data
    assert "email" in data
    assert data["email"] == "verify@example.com"