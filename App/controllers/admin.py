from App.database import db
from App.models import Admin
from App.exceptions import DuplicateEntity, ResourceNotFound


def create_admin(username, password):
    existing_admin = Admin.query.filter_by(username=username).first()
    if existing_admin:
        raise DuplicateEntity(f"Admin '{username}' already exists")

    new_admin = Admin(username=username, password=password)
    db.session.add(new_admin)
    db.session.commit()
    return new_admin
