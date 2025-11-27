import pytest
from App.controllers.area import create_area, update_area_name, delete_area
from App.exceptions import DuplicateEntity, ResourceNotFound

def test_create_area_success(mocker):
    # Arrange
    name = "New Area"
    MockArea = mocker.patch("App.controllers.area.Area")
    mock_session = mocker.patch("App.controllers.area.db.session")
    
    MockArea.query.filter_by.return_value.first.return_value = None

    # Act
    create_area(name)

    # Assert
    MockArea.assert_called_once_with(name=name)
    mock_session.add.assert_called_once()
    mock_session.commit.assert_called_once()

def test_create_area_duplicate(mocker):
    # Arrange
    name = "Existing Area"
    MockArea = mocker.patch("App.controllers.area.Area")
    MockArea.query.filter_by.return_value.first.return_value = mocker.Mock()

    # Act & Assert
    with pytest.raises(DuplicateEntity):
        create_area(name)

def test_update_area_name_success(mocker):
    # Arrange
    area_id = 1
    new_name = "Updated Area"
    mock_area = mocker.Mock()
    mock_area.id = area_id
    
    mock_session = mocker.patch("App.controllers.area.db.session")
    mock_session.get.return_value = mock_area

    # Act
    result = update_area_name(area_id, new_name)

    # Assert
    assert result.name == new_name
    mock_session.commit.assert_called_once()

def test_delete_area_success(mocker):
    # Arrange
    area_id = 1
    mock_area = mocker.Mock()
    
    mock_session = mocker.patch("App.controllers.area.db.session")
    mock_session.get.return_value = mock_area

    # Act
    result = delete_area(area_id)

    # Assert
    assert result is True
    mock_session.delete.assert_called_once_with(mock_area)
    mock_session.commit.assert_called_once()
