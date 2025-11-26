from sqlalchemy.orm import joinedload
from App.models import Resident, Driver, Area, Street, User
from App.database import db
from App.exceptions import ResourceNotFound, DuplicateEntity, ValidationError


def view_driver_status(driver_id):
    driver = Driver.query.get(driver_id)
    if not driver:
        raise ResourceNotFound(f"Driver with ID '{driver_id}' does not exist")
    return driver.status


def update_area_info(resident_id, new_area_id):
    resident = Resident.query.get(resident_id)
    if not resident:
        raise ResourceNotFound("Resident not found")

    new_area = Area.query.get(new_area_id)
    if not new_area:
        raise ResourceNotFound("Area not found")

    resident.area_id = new_area_id
    db.session.commit()
    return resident


def update_street_info(resident_id, new_street_id):
    resident = Resident.query.get(resident_id)
    if not resident:
        raise ResourceNotFound("Resident not found")

    new_street = Street.query.get(new_street_id)
    if not new_street:
        raise ResourceNotFound("Street not found")

    resident.street_id = new_street_id
    db.session.commit()
    return resident


def update_house_number(resident_id, new_house_number):
    resident = Resident.query.get(resident_id)
    if not resident:
        raise ResourceNotFound("Resident not found")

    resident.house_number = new_house_number
    db.session.commit()
    return resident


def update_resident_username(resident_id, new_username):
    resident = Resident.query.get(resident_id)
    if not resident:
        raise ResourceNotFound("Resident not found")

    if Resident.query.filter_by(username=new_username).first():
        raise DuplicateEntity(f"Username '{new_username}' is already taken")

    resident.username = new_username
    db.session.commit()
    return True


def create_resident(username, password, area_id, street_id, house_number):
    existing_resident = User.query.filter_by(username=username).first()
    if existing_resident:
        raise DuplicateEntity(f"Resident '{username}' already exists")

    area = Area.query.filter_by(id=area_id).first()
    if not area:
        raise ResourceNotFound(f"Area with ID '{area_id}' not found")

    street = Street.query.filter_by(id=street_id, area_id=area_id).first()
    if not street:
        raise ResourceNotFound(
            f"Street with ID '{street_id}' not found in Area '{area_id}'"
        )

    new_resident = Resident(
        username=username,
        password=password,
        area_id=area_id,
        street_id=street_id,
        house_number=house_number,
    )
    db.session.add(new_resident)
    db.session.commit()
    return new_resident


def get_all_residents():
    residents = Resident.query.options(
        joinedload(Resident.area), joinedload(Resident.street)
    ).all()
    return [str(resident) for resident in residents]


def get_all_residents_json():
    residents = Resident.query.options(
        joinedload(Resident.area), joinedload(Resident.street)
    ).all()
    return [resident.get_json() for resident in residents]


def delete_resident(resident_id):
    resident = db.session.get(Resident, resident_id)
    if not resident:
        raise ResourceNotFound("Resident not found")

    db.session.delete(resident)
    db.session.commit()
    return True
