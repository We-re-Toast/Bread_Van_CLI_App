import pytest
from App.controllers.item import (
    create_item,
    get_all_items,
    get_item,
    update_item,
    delete_item,
)
from App.models import Item
from App.exceptions import ResourceNotFound, DuplicateEntity


def test_create_item(db_session):
    # Arrange
    name = "Test Item"
    price = 10.0
    description = "Test Description"
    tags = ["test"]

    # Act
    item = create_item(name, price, description, tags)

    # Assert
    assert item.name == name
    assert item.price == price
    assert item.description == description
    assert item.tags == tags
    assert item.id is not None
    assert Item.query.get(item.id) is not None


def test_create_duplicate_item(db_session):
    # Arrange
    name = "Duplicate Item"
    create_item(name, 10.0, "Desc", [])

    # Act & Assert
    with pytest.raises(DuplicateEntity):
        create_item(name, 20.0, "Other Desc", [])


def test_get_all_items(db_session):
    # Arrange
    create_item("Item 1", 10.0, "Desc 1", [])
    create_item("Item 2", 20.0, "Desc 2", [])

    # Act
    items = get_all_items()

    # Assert
    assert len(items) == 2


def test_get_item(db_session):
    # Arrange
    item = create_item("Item 1", 10.0, "Desc 1", [])

    # Act
    fetched_item = get_item(item.id)

    # Assert
    assert fetched_item.id == item.id
    assert fetched_item.name == item.name


def test_get_item_not_found(db_session):
    # Act & Assert
    with pytest.raises(ResourceNotFound):
        get_item(999)


def test_update_item(db_session):
    # Arrange
    item = create_item("Item 1", 10.0, "Desc 1", [])
    new_name = "Updated Item"
    new_price = 15.0

    # Act
    updated_item = update_item(item.id, name=new_name, price=new_price)

    # Assert
    assert updated_item.name == new_name
    assert updated_item.price == new_price
    assert updated_item.description == "Desc 1"  # Unchanged


def test_update_item_not_found(db_session):
    # Act & Assert
    with pytest.raises(ResourceNotFound):
        update_item(999, name="New Name")


def test_delete_item(db_session):
    # Arrange
    item = create_item("Item 1", 10.0, "Desc 1", [])

    # Act
    result = delete_item(item.id)

    # Assert
    assert result is True
    assert Item.query.get(item.id) is None


def test_delete_item_not_found(db_session):
    # Act & Assert
    with pytest.raises(ResourceNotFound):
        delete_item(999)
