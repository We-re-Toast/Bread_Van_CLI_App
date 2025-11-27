import pytest
from App.controllers.resident import create_resident, update_resident_username, delete_resident
from App.exceptions import ResourceNotFound, DuplicateEntity

def test_create_resident_success(mocker):
    # Arrange
    username = "testresident"
    password = "password"
    area_id = 1
    street_id = 1
    house_number = 101

    MockUser = mocker.patch("App.controllers.resident.User")
    MockArea = mocker.patch("App.controllers.resident.Area")
    MockStreet = mocker.patch("App.controllers.resident.Street")
    MockResident = mocker.patch("App.controllers.resident.Resident")
    mock_session = mocker.patch("App.controllers.resident.db.session")

    MockUser.query.filter_by.return_value.first.return_value = None
    MockArea.query.filter_by.return_value.first.return_value = mocker.Mock()
    MockStreet.query.filter_by.return_value.first.return_value = mocker.Mock()

    # Act
    create_resident(username, password, area_id, street_id, house_number)

    # Assert
    MockResident.assert_called_once()
    call_args = MockResident.call_args[1]
    assert call_args['username'] == username
    assert call_args['area_id'] == area_id
    
    mock_session.add.assert_called_once()
    mock_session.commit.assert_called_once()

def test_create_resident_duplicate(mocker):
    # Arrange
    username = "testresident"
    MockUser = mocker.patch("App.controllers.resident.User")
    MockUser.query.filter_by.return_value.first.return_value = mocker.Mock()

    # Act & Assert
    with pytest.raises(DuplicateEntity):
        create_resident(username, "pass", 1, 1, 101)

def test_update_resident_username_success(mocker):
    # Arrange
    resident_id = 1
    new_username = "newname"
    mock_resident = mocker.Mock()
    mock_resident.id = resident_id

    MockResident = mocker.patch("App.controllers.resident.Resident")
    mock_session = mocker.patch("App.controllers.resident.db.session")

    MockResident.query.get.return_value = mock_resident
    MockResident.query.filter_by.return_value.first.return_value = None # No duplicate

    # Act
    result = update_resident_username(resident_id, new_username)

    # Assert
    assert result is True
    assert mock_resident.username == new_username
    mock_session.commit.assert_called_once()

def test_delete_resident_success(mocker):
    # Arrange
    resident_id = 1
    mock_resident = mocker.Mock()
    
    MockResident = mocker.patch("App.controllers.resident.Resident")
    mock_session = mocker.patch("App.controllers.resident.db.session")
    mock_session.get.return_value = mock_resident

    # Act
    result = delete_resident(resident_id)

    # Assert
    assert result is True
    mock_session.delete.assert_called_once_with(mock_resident)
    mock_session.commit.assert_called_once()
