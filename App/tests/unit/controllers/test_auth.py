import pytest
from App.controllers.auth import login

def test_login_success(mocker):
    # Arrange
    username = "testuser"
    password = "password"
    user_id = 1
    
    mock_user = mocker.Mock()
    mock_user.id = user_id
    mock_user.check_password.return_value = True
    
    mock_session = mocker.patch("App.controllers.auth.db.session")
    mock_result = mocker.Mock()
    mock_result.scalar_one_or_none.return_value = mock_user
    mock_session.execute.return_value = mock_result
    
    mock_create_token = mocker.patch("App.controllers.auth.create_access_token")
    mock_create_token.return_value = "fake_token"

    # Act
    token = login(username, password)

    # Assert
    assert token == "fake_token"
    mock_user.check_password.assert_called_once_with(password)
    mock_create_token.assert_called_once_with(identity=str(user_id))

def test_login_failure_wrong_password(mocker):
    # Arrange
    username = "testuser"
    password = "wrongpassword"
    
    mock_user = mocker.Mock()
    mock_user.check_password.return_value = False
    
    mock_session = mocker.patch("App.controllers.auth.db.session")
    mock_result = mocker.Mock()
    mock_result.scalar_one_or_none.return_value = mock_user
    mock_session.execute.return_value = mock_result

    # Act
    token = login(username, password)

    # Assert
    assert token is None

def test_login_failure_user_not_found(mocker):
    # Arrange
    username = "nonexistent"
    password = "password"
    
    mock_session = mocker.patch("App.controllers.auth.db.session")
    mock_result = mocker.Mock()
    mock_result.scalar_one_or_none.return_value = None
    mock_session.execute.return_value = mock_result

    # Act
    token = login(username, password)

    # Assert
    assert token is None
