import pytest
from fastapi.testclient import TestClient


def get_auth_token(client: TestClient, email: str = "test@example.com") -> str:
    """Helper function to get an authentication token."""
    # Register a user
    client.post(
        "/api/v1/auth/register",
        json={
            "email": email,
            "password": "securepassword"
        }
    )

    # Login to get token
    response = client.post(
        "/api/v1/auth/login",
        data={
            "email": email,
            "password": "securepassword"
        }
    )

    return response.json()["access_token"]


def test_create_task(client: TestClient):
    """Test creating a new task."""
    token = get_auth_token(client)

    response = client.post(
        "/api/v1/tasks/",
        json={
            "title": "Test Task",
            "description": "Test Description",
            "completed": False
        },
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Test Task"
    assert data["description"] == "Test Description"
    assert data["completed"] is False
    assert "id" in data
    assert "user_id" in data
    assert "created_at" in data
    assert "updated_at" in data


def test_get_tasks(client: TestClient):
    """Test getting all tasks for a user."""
    token = get_auth_token(client)

    # Create some tasks
    client.post(
        "/api/v1/tasks/",
        json={
            "title": "Task 1",
            "description": "Description 1",
            "completed": False
        },
        headers={"Authorization": f"Bearer {token}"}
    )

    client.post(
        "/api/v1/tasks/",
        json={
            "title": "Task 2",
            "description": "Description 2",
            "completed": True
        },
        headers={"Authorization": f"Bearer {token}"}
    )

    # Get all tasks
    response = client.get(
        "/api/v1/tasks/",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert any(task["title"] == "Task 1" for task in data)
    assert any(task["title"] == "Task 2" for task in data)


def test_get_single_task(client: TestClient):
    """Test getting a single task."""
    token = get_auth_token(client)

    # Create a task
    create_response = client.post(
        "/api/v1/tasks/",
        json={
            "title": "Single Task",
            "description": "Single Description",
            "completed": False
        },
        headers={"Authorization": f"Bearer {token}"}
    )

    task_id = create_response.json()["id"]

    # Get the task
    response = client.get(
        f"/api/v1/tasks/{task_id}",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Single Task"
    assert data["description"] == "Single Description"
    assert data["completed"] is False
    assert data["id"] == task_id


def test_update_task(client: TestClient):
    """Test updating a task."""
    token = get_auth_token(client)

    # Create a task
    create_response = client.post(
        "/api/v1/tasks/",
        json={
            "title": "Original Title",
            "description": "Original Description",
            "completed": False
        },
        headers={"Authorization": f"Bearer {token}"}
    )

    task_id = create_response.json()["id"]

    # Update the task
    response = client.put(
        f"/api/v1/tasks/{task_id}",
        json={
            "title": "Updated Title",
            "description": "Updated Description",
            "completed": True
        },
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Updated Title"
    assert data["description"] == "Updated Description"
    assert data["completed"] is True


def test_delete_task(client: TestClient):
    """Test deleting a task."""
    token = get_auth_token(client)

    # Create a task
    create_response = client.post(
        "/api/v1/tasks/",
        json={
            "title": "Task to Delete",
            "description": "Description",
            "completed": False
        },
        headers={"Authorization": f"Bearer {token}"}
    )

    task_id = create_response.json()["id"]

    # Delete the task
    response = client.delete(
        f"/api/v1/tasks/{task_id}",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 204

    # Verify the task is gone
    get_response = client.get(
        f"/api/v1/tasks/{task_id}",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert get_response.status_code == 404


def test_task_isolation_between_users(client: TestClient):
    """Test that users can only access their own tasks."""
    # Create user 1 and get token
    token1 = get_auth_token(client, "user1@example.com")

    # Create user 2 and get token
    token2 = get_auth_token(client, "user2@example.com")

    # User 1 creates a task
    create_response = client.post(
        "/api/v1/tasks/",
        json={
            "title": "User 1 Task",
            "description": "Description",
            "completed": False
        },
        headers={"Authorization": f"Bearer {token1}"}
    )

    task_id = create_response.json()["id"]
    assert task_id is not None

    # User 2 tries to access user 1's task
    response = client.get(
        f"/api/v1/tasks/{task_id}",
        headers={"Authorization": f"Bearer {token2}"}
    )

    # Should return 404 since user 2 doesn't have access to user 1's task
    assert response.status_code == 404

    # User 2 should only see their own tasks (which should be 0)
    get_tasks_response = client.get(
        "/api/v1/tasks/",
        headers={"Authorization": f"Bearer {token2}"}
    )
    assert get_tasks_response.status_code == 200
    assert len(get_tasks_response.json()) == 0

    # User 1 should still see their task
    get_tasks_response = client.get(
        "/api/v1/tasks/",
        headers={"Authorization": f"Bearer {token1}"}
    )
    assert get_tasks_response.status_code == 200
    assert len(get_tasks_response.json()) == 1
    assert get_tasks_response.json()[0]["title"] == "User 1 Task"


def test_unauthorized_access(client: TestClient):
    """Test that unauthorized access is denied."""
    # Try to create a task without authentication
    response = client.post(
        "/api/v1/tasks/",
        json={
            "title": "Unauthorized Task",
            "description": "Description"
        }
    )

    assert response.status_code == 401

    # Try to get tasks without authentication
    response = client.get("/api/v1/tasks/")
    assert response.status_code == 401