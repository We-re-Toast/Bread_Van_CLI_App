# App/models/admin.py
from App.database import db
from .user import User
from .driver import Driver
from .area import Area
from .street import Street

class Admin(User):
    __tablename__ = "admin"

    id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)

    __mapper_args__ = {
        "polymorphic_identity": "Admin",
    }

    def __init__(self, username, password):
        super().__init__(username, password)

    def get_json(self):
        user_json = super().get_json()
        return user_json

    def create_driver(self, username, password):
        driver = Driver(username=username,
                         password=password,
                         status="Offline",
                         areaId=0,
                         streetId=None)
        db.session.add(driver)
        db.session.commit()
        return driver

    def delete_driver(self, driverId):
        driver = Driver.query.get(driverId)
        if driver:
            db.session.delete(driver)
            db.session.commit()

    def add_area(self, name):
        area = Area(name=name)
        db.session.add(area)
        db.session.commit()
        return area

    def add_street(self, areaId, name):
        area = Area.query.get(areaId)
        if not area:
            return None
        street = Street(name=name, areaId=areaId)
        db.session.add(street)
        db.session.commit()
        return street

    def delete_area(self, areaId):
        area = Area.query.get(areaId)
        if not area:
            return None
        db.session.delete(area)
        db.session.commit()

    def delete_street(self, streetId):
        street = Street.query.get(streetId)
        if not street:
            return None
        db.session.delete(street)
        db.session.commit()

    def view_all_areas(self):
        return Area.query.all()

    def view_all_streets(self):
        return Street.query.all()
        

  
