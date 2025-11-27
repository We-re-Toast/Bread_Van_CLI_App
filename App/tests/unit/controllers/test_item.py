import pytest
from App.controllers.item import create_item, update_item, delete_item
from App.exceptions import DuplicateEntity, ResourceNotFound

def test_create_item_success(mocker):
    # Arrange
    name = "Bread"
    price = 2.50
    description = "Fresh"
    tags = ["food"]
    
    MockItem = mocker.patch("App.controllers.item.Item")
    mock_session = mocker.patch("App.controllers.item.db.session")
    
    MockItem.query.filter_by.return_value.first.return_value = None

    # Act
    create_item(name, price, description, tags)

    # Assert
    MockItem.assert_called_once_with(name=name, price=price, description=description, tags=tags)
    mock_session.add.assert_called_once()
    mock_session.commit.assert_called_once()

def test_create_item_duplicate(mocker):
    # Arrange
    name = "Bread"
    MockItem = mocker.patch("App.controllers.item.Item")
    MockItem.query.filter_by.return_value.first.return_value = mocker.Mock()

    # Act & Assert
    with pytest.raises(DuplicateEntity):
        create_item(name, 1.0, "desc", [])

def test_update_item_success(mocker):
    # Arrange
    item_id = 1
    new_name = "New Bread"
    mock_item = mocker.Mock()
    mock_item.id = item_id
    
    MockItem = mocker.patch("App.controllers.item.Item")
    mock_session = mocker.patch("App.controllers.item.db.session")
    
    MockItem.query.get.return_value = mock_item
    MockItem.query.filter.return_value.first.return_value = None # No duplicate

    # Act
    result = update_item(item_id, name=new_name)

    # Assert
    assert result.name == new_name
    mock_session.commit.assert_called_once()

def test_delete_item_success(mocker):
    # Arrange
    item_id = 1
    mock_item = mocker.Mock()
    
    MockItem = mocker.patch("App.controllers.item.Item")
    mock_session = mocker.patch("App.controllers.item.db.session")
    
    MockItem.query.get.return_value = mock_item

    # Act
    result = delete_item(item_id)

    # Assert
    assert result is True
    mock_session.delete.assert_called_once_with(mock_item)
    mock_session.commit.assert_called_once()
