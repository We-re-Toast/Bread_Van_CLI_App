from App.database import db
from datetime import datetime
from .user import User
from .drive import Drive
from .street import Street
from .driver_stock import DriverStock


class Driver(User):
    __tablename__ = "driver"

    id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    status = db.Column(db.String(20), nullable=False)
    areaId = db.Column(db.Integer, db.ForeignKey('area.id'), nullable=False)
    streetId = db.Column(db.Integer, db.ForeignKey('street.id'))

    area = db.relationship("Area", backref="drivers")
    street = db.relationship("Street", backref="drivers")

    __mapper_args__ = {
        "polymorphic_identity": "Driver",
    }

    def __init__(self, username, password, status, areaId, streetId):
        super().__init__(username, password)
        self.status = status
        self.areaId = areaId
        self.streetId = streetId

    def get_json(self):
        user_json = super().get_json()
        user_json['status'] = self.status
        user_json['areaId'] = self.areaId
        user_json['streetId'] = self.streetId
        return user_json

    def login(self, password):
        if super().login(password):
            self.areaId = 0
            self.streetId = 0
            self.status = "Available"
            db.session.commit()
            return True
        return False

    def logout(self):
        super().logout()
        self.status = "Offline"
        db.session.commit()

def schedule_drive(self, areaId, streetId, date_str, time_str):
    date = datetime.strptime(date_str, "%Y-%m-%d").date()
    time = datetime.strptime(time_str, "%H:%M").time()

    new_drive = Drive(
        driverId=self.id,
        areaId=areaId,
        streetId=streetId,
        date=date,
        time=time,
        status="Upcoming"
    )

    db.session.add(new_drive)
    db.session.commit()

    street = Street.query.get(streetId)

    if street:
        # Attach residents ONCE
        street.register_residents_as_observers()

        # get menu
        menu_items = DriverStock.query.filter_by(driverId=self.id).all()
        eta = f"{date} {time}"

        # send notification
        street.notify_drive_scheduled(new_drive, self, menu_items, eta)

    return new_drive



    def cancel_drive(self, driveId):
        drive = Drive.query.get(driveId)
        if drive:
            drive.status = "Cancelled"
            db.session.commit()

            street = None
            if self.streetId is not None:
                street = Street.query.get(self.streetId)
            if street:
                for resident in street.residents:
                    resident.receive_notif(
                        f"CANCELLED: Drive {drive.id} by {self.id} on {drive.date} at {drive.time}"
                    )
                db.session.commit()
        return None

    def view_drives(self):
        return Drive.query.filter_by(driverId=self.id).all()

    def start_drive(self, driveId):
        drive = Drive.query.get(driveId)
        if drive:
            self.status = "Busy"
            self.areaId = drive.areaId
            self.streetId = drive.streetId
            drive.status = "In Progress"
            db.session.commit()
            return drive
        return None

    def end_drive(self, driveId):
        drive = Drive.query.get(driveId)
        if drive:
            self.status = "Available"
            drive.status = "Completed"
            db.session.commit()
            return drive
        return None

    def view_requested_stops(self, driveId):
        drive = Drive.query.get(driveId)
        if drive:
            return drive.stops
        return None
