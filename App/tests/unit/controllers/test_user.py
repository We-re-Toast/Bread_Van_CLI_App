import pytest
from App.controllers.user import create_user, get_user_by_username, get_user, update_user

def test_create_user(mocker):
    # Arrange
    username = "testuser"
    password = "password"
    
    MockUser = mocker.patch("App.controllers.user.User")
    mock_session = mocker.patch("App.controllers.user.db.session")

    # Act
    create_user(username, password)

    # Assert
    MockUser.assert_called_once_with(username=username, password=password)
    mock_session.add.assert_called_once()
    mock_session.commit.assert_called_once()

def test_get_user_by_username(mocker):
    # Arrange
    username = "testuser"
    mock_user = mocker.Mock()
    
    mock_session = mocker.patch("App.controllers.user.db.session")
    mock_result = mocker.Mock()
    mock_result.scalar_one_or_none.return_value = mock_user
    mock_session.execute.return_value = mock_result

    # Act
    result = get_user_by_username(username)

    # Assert
    assert result == mock_user

def test_get_user(mocker):
    # Arrange
    user_id = 1
    mock_user = mocker.Mock()
    
    mock_session = mocker.patch("App.controllers.user.db.session")
    mock_session.get.return_value = mock_user

    # Act
    result = get_user(user_id)

    # Assert
    assert result == mock_user
    mock_session.get.assert_called_once()

def test_update_user_success(mocker):
    # Arrange
    user_id = 1
    new_username = "newname"
    mock_user = mocker.Mock()
    
    mock_session = mocker.patch("App.controllers.user.db.session")
    mock_session.get.return_value = mock_user

    # Act
    result = update_user(user_id, new_username)

    # Assert
    assert result is True
    assert mock_user.username == new_username
    mock_session.commit.assert_called_once()

def test_update_user_not_found(mocker):
    # Arrange
    user_id = 1
    new_username = "newname"
    
    mock_session = mocker.patch("App.controllers.user.db.session")
    mock_session.get.return_value = None

    # Act
    result = update_user(user_id, new_username)

    # Assert
    assert result is None
    mock_session.commit.assert_not_called()
