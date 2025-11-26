from sqlalchemy.orm import joinedload
from App.models import Street
from App.database import db
from App.exceptions import DuplicateEntity, ResourceNotFound


def create_street(name, area_id):
    existing_street = Street.query.filter_by(name=name, area_id=area_id).first()
    if existing_street:
        raise DuplicateEntity(f"Street '{name}' already exists in Area ID '{area_id}'")

    new_street = Street(name=name, area_id=area_id)
    db.session.add(new_street)
    db.session.commit()
    return new_street


def get_all_streets():
    streets = Street.query.options(joinedload(Street.area)).all()
    return [str(street) for street in streets]


def get_all_streets_json():
    streets = Street.query.all()
    return [street.get_json() for street in streets]


def update_street_name(street_id, new_name):
    street = db.session.get(Street, street_id)
    if not street:
        raise ResourceNotFound("Street not found")

    street.name = new_name
    db.session.commit()
    return street


def delete_street(street_id):
    street = db.session.get(Street, street_id)
    if not street:
        raise ResourceNotFound("Street not found")

    db.session.delete(street)
    db.session.commit()
    return True
