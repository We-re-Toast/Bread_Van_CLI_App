from App.database import db
from datetime import datetime
from .user import User
from .drive import Drive
from .street import Street
from typing import List
from .observer import Observer
from .subject import Subject


class Driver(User, Subject):
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
        self._observers: List[Observer] = []

    def attach(self, observer: "Observer") -> None:
        if observer not in self._observers:
            self._observers.append(observer)

    def detach(self, observer: "Observer") -> None:
        if observer in self._observers:
            self._observers.remove(observer)
    
    def notify(self, message: str) -> None:
        for observer in self._observers:
            observer.update(self, message)

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
        try:
            date = datetime.strptime(date_str, "%Y-%m-%d").date()
            time = datetime.strptime(time_str, "%H:%M").time()
        except Exception:
            print(
                "Invalid date or time format. Please use YYYY-MM-DD for date and HH:MM for time."
            )
            return

        new_drive = Drive(driverId=self.id,
                          areaId=areaId,
                          streetId=streetId,
                          date=date,
                          time=time,
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
