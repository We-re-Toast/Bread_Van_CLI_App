from App.database import db
from App.models import Item
from App.exceptions import ResourceNotFound, DuplicateEntity


def create_item(name, price, description, tags):
    if Item.query.filter_by(name=name).first():
        raise DuplicateEntity(f"Item with name '{name}' already exists")

    new_item = Item(name=name, price=price, description=description, tags=tags)
    db.session.add(new_item)
    db.session.commit()
    return new_item


def get_all_items():
    return Item.query.all()


def get_all_items_json():
    items = Item.query.all()
    if not items:
        return []
    return [item.get_json() for item in items]


def get_item(item_id):
    item = Item.query.get(item_id)
    if not item:
        raise ResourceNotFound(f"Item with ID '{item_id}' does not exist")
    return item


def update_item(item_id, name=None, price=None, description=None, tags=None):
    item = Item.query.get(item_id)
    if not item:
        raise ResourceNotFound(f"Item with ID '{item_id}' does not exist")

    if name:
        if Item.query.filter(Item.name == name, Item.id != item_id).first():
            raise DuplicateEntity(f"Item with name '{name}' already exists")
        item.name = name
    if price is not None:
        item.price = price
    if description:
        item.description = description
    if tags is not None:
        item.tags = tags

    db.session.commit()
    return item


def delete_item(item_id):
    item = Item.query.get(item_id)
    if not item:
        raise ResourceNotFound(f"Item with ID '{item_id}' does not exist")

    db.session.delete(item)
    db.session.commit()
    return True
