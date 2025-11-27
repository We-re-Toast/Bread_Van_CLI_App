import pytest
from App.controllers.user import create_user, get_user, update_user
from App.models import User

def test_create_user(db_session):
    # Arrange
    username = "newuser"
    password = "password"

    # Act
    user = create_user(username, password)

    # Assert
    assert user.username == username
    assert user.check_password(password)
    assert user.id is not None
    assert User.query.get(user.id) is not None

def test_get_user(db_session, driver_user):
    # Act
    user = get_user(driver_user.id)

    # Assert
    assert user.id == driver_user.id
    assert user.username == driver_user.username

def test_update_user(db_session, driver_user):
    # Arrange
    new_username = "updateddriver"

    # Act
    result = update_user(driver_user.id, new_username)

    # Assert
    assert result is True
    assert driver_user.username == new_username
