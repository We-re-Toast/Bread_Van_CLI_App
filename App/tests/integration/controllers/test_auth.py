import pytest
from App.controllers.auth import login
from App.models import User

def test_login_success(db_session, driver_user):
    # Arrange
    username = driver_user.username
    password = "driverpass"

    # Act
    token = login(username, password)

    # Assert
    assert token is not None

def test_login_invalid_credentials(db_session, driver_user):
    # Arrange
    username = driver_user.username
    password = "wrongpassword"

    # Act
    token = login(username, password)

    # Assert
    assert token is None

def test_login_not_found(db_session):
    # Arrange
    username = "nonexistent"
    password = "password"

    # Act
    token = login(username, password)

    # Assert
    assert token is None
