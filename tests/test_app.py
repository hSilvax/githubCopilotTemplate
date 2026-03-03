import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_list_activities():
    # Arrange: (No setup needed for in-memory activities)

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert any("description" in v for v in data.values())

def test_signup_success():
    # Arrange
    email = "testuser@mergington.edu"
    activity = "Drama Club"

    # Act
    response = client.post(f"/activities/{activity}/signup", params={"email": email})

    # Assert
    assert response.status_code == 200
    assert "Signed up" in response.json()["message"]

def test_signup_duplicate():
    # Arrange
    email = "emma@mergington.edu"  # Already signed up for Programming Class
    activity = "Programming Class"

    # Act
    response = client.post(f"/activities/{activity}/signup", params={"email": email})

    # Assert
    assert response.status_code == 400
    assert "already signed" in response.json()["detail"]

def test_signup_nonexistent_activity():
    # Arrange
    email = "test@mergington.edu"
    activity = "Nonexistent"

    # Act
    response = client.post(f"/activities/{activity}/signup", params={"email": email})

    # Assert
    assert response.status_code == 404
    assert "not found" in response.json()["detail"]
