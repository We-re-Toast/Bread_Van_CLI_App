from App.database import db
from App.models import Driver, Area, Street
from App.models.enums import DriverStatus
from App.exceptions import ResourceNotFound, DuplicateEntity


def create_driver(
    username, password, status=DriverStatus.OFF_DUTY, area_id=None, street_id=None
):
    existing_driver = Driver.query.filter_by(username=username).first()
    if existing_driver:
        raise DuplicateEntity(f"Driver '{username}' already exists")

    if area_id and street_id:
        area = Area.query.filter_by(id=area_id).first()
        street = Street.query.filter_by(id=street_id, area_id=area_id).first()
        if not area or not street:
            raise ResourceNotFound(
                f"Area with ID '{area_id}' or Street with ID '{street_id}' not found"
            )

    new_driver = Driver(
        username=username,
        password=password,
        status=status,
        area_id=area_id,
        street_id=street_id,
    )
    db.session.add(new_driver)
    db.session.commit()
    return new_driver


def get_all_drivers():
    drivers = Driver.query.all()
    return [str(driver) for driver in drivers]


def get_all_drivers_json():
    drivers = Driver.query.all()
    return [driver.get_json() for driver in drivers]


def update_driver_status(driver_id, status):
    driver = Driver.query.get(driver_id)
    if not driver:
        raise ResourceNotFound(f"Driver with ID '{driver_id}' does not exist")
    driver.status = status
    db.session.commit()
    return driver


def update_driver_username(driver_id, new_username):
    driver = Driver.query.get(driver_id)
    if not driver:
        raise ResourceNotFound(f"Driver with ID '{driver_id}' does not exist")
    if Driver.query.filter_by(username=new_username).first():
        raise DuplicateEntity(f"Username '{new_username}' is already taken")
    driver.username = new_username
    db.session.commit()
    return driver


def update_area_info(driver_id, new_area_id):
    driver = Driver.query.get(driver_id)
    if not driver:
        raise ResourceNotFound(f"Driver with ID '{driver_id}' does not exist")

    new_area = Area.query.get(new_area_id)
    if not new_area:
        raise ResourceNotFound(f"Area with ID '{new_area_id}' does not exist")
    
    driver.area_id = new_area_id
    db.session.commit()
    return driver


def update_street_info(driver_id, new_street_id):
    driver = Driver.query.get(driver_id)
    if not driver:
        raise ResourceNotFound(f"Driver with ID '{driver_id}' does not exist")
    
    new_street = Street.query.get(new_street_id)
    if not new_street:
        raise ResourceNotFound(f"Street with ID '{new_street_id}' does not exist")
    
    driver.street_id = new_street_id
    db.session.commit()
    return driver

def get_driver_status_and_location(driver_id):
    driver = Driver.query.get(driver_id)
    if not driver:
        raise ResourceNotFound(f"Driver with ID '{driver_id}' does not exist")
    return {
        "driver_id": driver.id,
        "driver_name": driver.username,
        "status": driver.status,
        "current_location": f"{driver.street.name}, {driver.area.name}"
    }

def delete_driver(driver_id):
    driver = Driver.query.get(driver_id)
    if not driver:
        raise ResourceNotFound("Driver not found")

    db.session.delete(driver)
    db.session.commit()
    return True