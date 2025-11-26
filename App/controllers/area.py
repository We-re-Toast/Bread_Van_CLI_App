from App.models import Area
from App.database import db
from App.exceptions import DuplicateEntity, ResourceNotFound


def create_area(name):
    existing_area = Area.query.filter_by(name=name).first()
    if existing_area:
        raise DuplicateEntity(f"Area '{name}' already exists")

    new_area = Area(name=name)
    db.session.add(new_area)
    db.session.commit()
    return new_area


def get_all_areas():
    areas = Area.query.all()
    return [str(area) for area in areas]


def get_all_areas_json():
    areas = Area.query.all()
    return [area.get_json() for area in areas]


def update_area_name(area_id, new_name):
    area = db.session.get(Area, area_id)
    if not area:
        raise ResourceNotFound("Area not found")

    area.name = new_name
    db.session.commit()
    return area


def delete_area(area_id):
    area = db.session.get(Area, area_id)
    if not area:
        raise ResourceNotFound("Area not found")

    db.session.delete(area)
    db.session.commit()
    return True
