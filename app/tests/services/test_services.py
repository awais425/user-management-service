# app/tests/services/test_user_service.py
from unittest.mock import MagicMock

import pytest
from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.core.model import User
from app.repositories.user import UserRepository
from app.schemas.user import UserCreate, UserUpdate
from app.services.user_service import UserService


@pytest.fixture
def mock_user_repository():
    return MagicMock(UserRepository)

@pytest.fixture
def mock_kafka_producer():
    return MagicMock()

@pytest.fixture
def user_service(mock_user_repository, mock_kafka_producer):
    return UserService(user_repository=mock_user_repository, kafka_producer=mock_kafka_producer)


@pytest.fixture
def mock_db_session():
    return MagicMock(Session)


def test_create_user(user_service, mock_user_repository, mock_db_session):
    user_create = UserCreate(email="test@example.com", password="testpassword")
    user_model = User(
        id=1, email=user_create.email, hashed_password=user_create.password
    )

    mock_user_repository.create_user.return_value = user_model

    created_user = user_service.create_user(mock_db_session, user_create)

    assert created_user == user_model
    mock_user_repository.create_user.assert_called_once_with(
        mock_db_session, user_create
    )


def test_get_user_by_email(user_service, mock_user_repository, mock_db_session):
    email = "test@example.com"
    user_model = User(id=1, email=email, hashed_password="hashedpassword")

    mock_user_repository.get_user_by_email.return_value = user_model

    found_user = user_service.get_user_by_email(mock_db_session, email)

    assert found_user == user_model
    mock_user_repository.get_user_by_email.assert_called_once_with(
        mock_db_session, email
    )


def test_get_user_by_email_not_found(
    user_service, mock_user_repository, mock_db_session
):
    email = "test@example.com"

    mock_user_repository.get_user_by_email.return_value = None

    with pytest.raises(HTTPException) as exc_info:
        user_service.get_user_by_email(mock_db_session, email)

    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == "User not found"


def test_get_user_by_id(user_service, mock_user_repository, mock_db_session):
    user_id = 1
    user_model = User(
        id=user_id, email="test@example.com", hashed_password="hashedpassword"
    )

    mock_user_repository.get_user_by_id.return_value = user_model

    found_user = user_service.get_user_by_id(mock_db_session, user_id)

    assert found_user == user_model
    mock_user_repository.get_user_by_id.assert_called_once_with(
        mock_db_session, user_id
    )


def test_get_user_by_id_not_found(user_service, mock_user_repository, mock_db_session):
    user_id = 1

    mock_user_repository.get_user_by_id.return_value = None

    with pytest.raises(HTTPException) as exc_info:
        user_service.get_user_by_id(mock_db_session, user_id)

    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == "User not found"


def test_update_user(user_service, mock_user_repository, mock_db_session):
    user_id = 1
    user_update = UserUpdate(email="updated@example.com", is_active=True)
    user_model = User(
        id=user_id, email="test@example.com", hashed_password="hashedpassword"
    )

    mock_user_repository.get_user_by_id.return_value = user_model
    updated_user_model = User(
        id=user_id,
        email=user_update.email,
        hashed_password=user_model.hashed_password,
        is_active=user_update.is_active,
    )
    mock_user_repository.update_user.return_value = updated_user_model

    updated_user = user_service.update_user(mock_db_session, user_id, user_update)

    assert updated_user == updated_user_model
    mock_user_repository.get_user_by_id.assert_called_once_with(
        mock_db_session, user_id
    )
    mock_user_repository.update_user.assert_called_once_with(
        mock_db_session, user_id, user_update
    )


def test_update_user_not_found(user_service, mock_user_repository, mock_db_session):
    user_id = 1
    user_update = UserUpdate(email="updated@example.com", is_active=True)

    mock_user_repository.get_user_by_id.return_value = None

    with pytest.raises(HTTPException) as exc_info:
        user_service.update_user(mock_db_session, user_id, user_update)

    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == "User not found"


def test_delete_user(user_service, mock_user_repository, mock_db_session):
    user_id = 1
    user_model = User(
        id=user_id, email="test@example.com", hashed_password="hashedpassword"
    )

    mock_user_repository.get_user_by_id.return_value = user_model
    mock_user_repository.delete_user.return_value = "User deleted successfully"

    deleted_user = user_service.delete_user(mock_db_session, user_id)

    assert deleted_user == "User deleted successfully"
    mock_user_repository.get_user_by_id.assert_called_once_with(
        mock_db_session, user_id
    )
    mock_user_repository.delete_user.assert_called_once_with(mock_db_session, user_id)


def test_delete_user_not_found(user_service, mock_user_repository, mock_db_session):
    user_id = 1

    mock_user_repository.get_user_by_id.return_value = None

    with pytest.raises(HTTPException) as exc_info:
        user_service.delete_user(mock_db_session, user_id)

    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == "User not found"


