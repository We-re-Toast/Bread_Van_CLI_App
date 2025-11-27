import pytest
from App.controllers.driver import create_driver
from App.controllers.resident import create_resident
from App.controllers.area import create_area
from App.controllers.street import create_street
from App.models import Driver, Resident, Area, Street
from App.exceptions import DuplicateEntity

def test_create_area(db_session):
    # Arrange
    name = "New Area"

    # Act
    area = create_area(name)

    # Assert
    assert area.name == name
    assert area.id is not None
    assert Area.query.get(area.id) is not None

def test_create_duplicate_area(db_session, area):
    # Arrange
    name = area.name

    # Act & Assert
    with pytest.raises(DuplicateEntity):
        create_area(name)

def test_create_street(db_session, area):
    # Arrange
    name = "New Street"

    # Act
    street = create_street(name, area.id)

    # Assert
    assert street.name == name
    assert street.area_id == area.id
    assert street.id is not None
    assert Street.query.get(street.id) is not None

def test_create_driver(db_session):
    # Arrange
    username = "newdriver"
    password = "password"

    # Act
    driver = create_driver(username, password)

    # Assert
    assert driver.username == username
    assert driver.check_password(password)
    assert driver.id is not None
    assert Driver.query.get(driver.id) is not None

def test_create_resident(db_session, area, street):
    # Arrange
    username = "newresident"
    password = "password"
    house_number = 123

    # Act
    resident = create_resident(username, password, area.id, street.id, house_number)

    # Assert
    assert resident.username == username
    assert resident.check_password(password)
    assert resident.area_id == area.id
    assert resident.street_id == street.id
    assert resident.house_number == house_number
    assert resident.id is not None
    assert Resident.query.get(resident.id) is not None
