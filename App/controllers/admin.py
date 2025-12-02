from App.models import Admin, Driver, Area, Street, Item
from App.database import db

# All admin-related business logic will be moved here as functions

def admin_create_driver(username, password):
    existing_user = Admin.query.filter_by(username=username).first()
    if existing_user:
        raise ValueError("Username already taken.")
    driver = Driver(username=username, password=password, status="Offline", areaId=0, streetId=None)
    db.session.add(driver)
    db.session.commit()
    return driver

def admin_delete_driver(driver_id):
    driver = Driver.query.get(driver_id)
    if not driver:
        raise ValueError("Invalid driver ID.")
    db.session.delete(driver)
    db.session.commit()
    return driver

def admin_add_item(name, price, description, tags):
    item = Item(name=name, price=price, description=description, tags=tags)
    db.session.add(item)
    db.session.commit()
    return item

def admin_delete_item(item_id):
    item = Item.query.get(item_id)
    if not item:
        raise ValueError("Invalid item ID.")
    db.session.delete(item)
    db.session.commit()

def admin_view_all_areas():
    return Area.query.all()

def admin_view_all_streets():
    return Street.query.all()

def admin_view_all_items():
     return Item.query.all()
