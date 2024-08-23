from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.repositories.user import UserORM


def test_create_user(client: TestClient, db: Session):
    # Create User
    response = client.post(
        "/api/v1/users/", json={"email": "test@example.com", "password": "testpassword"}
    )
    assert response.status_code == 201  # Created
    data = response.json()
    assert "id" in data
    assert data["email"] == "test@example.com"
    assert data["is_active"] is True
    db.commit()  # Commit the changes to the database


def test_get_user_by_email(client: TestClient, db: Session):
    # Get the user by email
    new_user = UserORM(email="test_get@example.com", hashed_password="testpassword")
    db.add(new_user)
    db.commit()  # Commit the changes to the database
    db.refresh(new_user)

    response = client.get(f"/api/v1/users/email/{new_user.email}")
    assert response.status_code == 200
    data = response.json()
    assert "id" in data
    assert data["email"] == new_user.email
    assert data["is_active"] is True


def test_update_user(client: TestClient, db: Session):
    # Update User
    new_user = UserORM(email="test_update@example.com", hashed_password="testpassword")
    db.add(new_user)
    db.commit()  # Commit the changes to the database
    db.refresh(new_user)

    response = client.put(
        f"/api/v1/users/{new_user.id}",
        json={"email": "updated@example.com", "is_active": False},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "updated@example.com"
    assert data["is_active"] is False


def test_delete_user(client: TestClient, db: Session):
    # Create a user
    new_user = UserORM(email="test_delete@example.com", hashed_password="testpassword")
    db.add(new_user)
    db.commit()  # Commit the changes to the database
    db.refresh(new_user)

    # Delete the user
    response = client.delete(f"/api/v1/users/{new_user.id}")
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "User deleted successfully"
