from App.models import User, Area, Street, Item, Driver, Resident


def get_area_id(name):
    if not name:
        return None
    area = Area.query.filter_by(name=name).first()
    if not area:
        raise ValueError(f"Area '{name}' not found")
    return area.id


def get_street_id(name, area_id):
    if not name:
        return None
    if not area_id:
        raise ValueError("Area must be specified to find a street")
    street = Street.query.filter_by(name=name, area_id=area_id).first()
    if not street:
        raise ValueError(f"Street '{name}' not found in area")
    return street.id


def get_driver_id(username):
    driver = Driver.query.filter_by(username=username).first()
    if not driver:
        raise ValueError(f"Driver '{username}' not found")
    return driver.id


def get_resident_id(username):
    resident = Resident.query.filter_by(username=username).first()
    if not resident:
        raise ValueError(f"Resident '{username}' not found")
    return resident.id


def get_item_id(name):
    item = Item.query.filter_by(name=name).first()
    if not item:
        raise ValueError(f"Item '{name}' not found")
    return item.id
