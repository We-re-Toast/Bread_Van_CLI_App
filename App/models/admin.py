from App.database import db
from .user import User

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
        from .driver import Driver
        driver = Driver(username=username,
                         password=password,
                         status="Offline",
                         areaId=0,
                         streetId=None)
        db.session.add(driver)
        db.session.commit()
        return driver

    def delete_driver(self, driverId):
        from .driver import Driver
        driver = Driver.query.get(driverId)
        if driver:
            db.session.delete(driver)
            db.session.commit()

    def add_area(self, name):
        from .area import Area
        area = Area(name=name)
        db.session.add(area)
        db.session.commit()
        return area

    def add_street(self, areaId, name):
        from .area import Area
        from .street import Street
        area = Area.query.get(areaId)
        if not area:
            return None
        street = Street(name=name, areaId=areaId)
        db.session.add(street)
        db.session.commit()
        return street

    def delete_area(self, areaId):
        from .area import Area
        area = Area.query.get(areaId)
        if not area:
            return None
        db.session.delete(area)
        db.session.commit()

    def delete_street(self, streetId):
        from .street import Street
        street = Street.query.get(streetId)
        if not street:
            return None
        db.session.delete(street)
        db.session.commit()

    def view_all_areas(self):
        from .area import Area
        return Area.query.all()

    def view_all_streets(self):
        from .street import Street
        return Street.query.all()