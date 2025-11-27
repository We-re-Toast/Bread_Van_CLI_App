from datetime import datetime
from App.database import db
from .user import User
from .driver import Driver
from .area import Area
from .street import Street
from .drive import Drive

class Admin(User):
    __tablename__ = "admin"

    id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)

    __mapper_args__ = {
        "polymorphic_identity": "Admin",
    }

    def __init__(self, username, password):
        super().__init__(username, password)

    def list():
        return Admin.query.all()
    
    def get_by_id(id):
        return Admin.query.get(id)

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
        
    # schedule_drive(driver_id, street_id, date_str, time_str, menu_id)
    def schedule_drive(self, driver_ID, areaId, streetId, date_str, time_str, menu_id):
        try:
            date = datetime.strptime(date_str, "%Y-%m-%d").date()
            time = datetime.strptime(time_str, "%H:%M").time()
        except Exception:
            print(
                "Invalid date or time format. Please use YYYY-MM-DD for date and HH:MM for time."
            )
            return

        new_drive = Drive(driverId=driver_ID,
                          areaId=areaId,
                          streetId=streetId,
                          date=date,
                          time=time,
                          menu_id = menu_id,
                          status="Upcoming")
        db.session.add(new_drive)
        db.session.commit()

        street = Street.query.get(streetId)
        if street:
            for resident in street.residents:
                resident.receive_notif(
                    f"SCHEDULED>> Drive {new_drive.id} by Driver {self.id} on {date} at {time}"
                )
            db.session.commit()
        return (new_drive)
