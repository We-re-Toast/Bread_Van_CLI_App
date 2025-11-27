import pytest
from App.controllers.street import create_street, update_street_name, delete_street
from App.exceptions import DuplicateEntity, ResourceNotFound

def test_create_street_success(mocker):
    # Arrange
    name = "New Street"
    area_id = 1
    MockStreet = mocker.patch("App.controllers.street.Street")
    mock_session = mocker.patch("App.controllers.street.db.session")
    
    MockStreet.query.filter_by.return_value.first.return_value = None

    # Act
    create_street(name, area_id)

    # Assert
    MockStreet.assert_called_once_with(name=name, area_id=area_id)
    mock_session.add.assert_called_once()
    mock_session.commit.assert_called_once()

def test_create_street_duplicate(mocker):
    # Arrange
    name = "Existing Street"
    area_id = 1
    MockStreet = mocker.patch("App.controllers.street.Street")
    MockStreet.query.filter_by.return_value.first.return_value = mocker.Mock()

    # Act & Assert
    with pytest.raises(DuplicateEntity):
        create_street(name, area_id)

def test_update_street_name_success(mocker):
    # Arrange
    street_id = 1
    new_name = "Updated Street"
    mock_street = mocker.Mock()
    
    mock_session = mocker.patch("App.controllers.street.db.session")
    mock_session.get.return_value = mock_street

    # Act
    result = update_street_name(street_id, new_name)

    # Assert
    assert result.name == new_name
    mock_session.commit.assert_called_once()

def test_delete_street_success(mocker):
    # Arrange
    street_id = 1
    mock_street = mocker.Mock()
    
    mock_session = mocker.patch("App.controllers.street.db.session")
    mock_session.get.return_value = mock_street

    # Act
    result = delete_street(street_id)

    # Assert
    assert result is True
    mock_session.delete.assert_called_once_with(mock_street)
    mock_session.commit.assert_called_once()
