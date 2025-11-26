from App.models import User, Driver
from App.database import db

def create_user(username, password):
    newuser = User(username=username, password=password)
    db.session.add(newuser)
    db.session.commit()
    return newuser

def get_user_by_username(username):
    result = db.session.execute(db.select(User).filter_by(username=username))
    return result.scalar_one_or_none()

def get_user(id):
    return db.session.get(User, id)

def get_all_users():
    return db.session.scalars(db.select(User)).all()

def get_all_users_json():
    users = get_all_users()
    if not users:
        return []
    users = [user.get_json() for user in users]
    return users

def update_user(id, username):
    user = get_user(id)
    if user:
        user.username = username
        # user is already in the session; no need to re-add
        db.session.commit()
        return True
    return None

def user_login(username, password):
    user = db.session.execute(db.select(User).filter_by(username=username)).scalar_one_or_none()
    if user and user.check_password(password):
        user.logged_in = True
        if isinstance(user, Driver):
            user.status = "Available"
        db.session.commit()
        return user
    raise ValueError("Invalid username or password.")

def user_logout(user):
    user.logged_in = False
    if isinstance(user, Driver):
        user.status = "Offline"
    db.session.commit()
    return user

def user_view_street_drives(user, area_id, street_id):
    return user.view_street_drives(area_id, street_id)
