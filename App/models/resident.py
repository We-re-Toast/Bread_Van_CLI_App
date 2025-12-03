# App/models/resident.py
from datetime import datetime
from sqlalchemy.ext.mutable import MutableList
from sqlalchemy import JSON

from App.database import db
from .user import User
from .driver import Driver
from .stop import Stop
from .drive import Drive
  


MAX_INBOX_SIZE = 20


class Resident(User):  
    __tablename__ = "resident"

    id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    areaId = db.Column(db.Integer, db.ForeignKey('area.id'), nullable=False)
    streetId = db.Column(db.Integer, db.ForeignKey('street.id'), nullable=False)
    houseNumber = db.Column(db.Integer, nullable=False)
    inbox = db.Column(MutableList.as_mutable(JSON), default=[])
    subscriptions = db.Column(MutableList.as_mutable(JSON), default=[])

    area = db.relationship("Area", backref='residents')
    street = db.relationship("Street", backref='residents')
    stops = db.relationship('Stop', backref='resident')

    __mapper_args__ = {"polymorphic_identity": "Resident"}

    def __init__(self, username, password, areaId, streetId, houseNumber):
        super().__init__(username, password)
        self.areaId = areaId
        self.streetId = streetId
        self.houseNumber = houseNumber

    def update(self, subject, message: str):
        self.receive_notif(message)

    def subscribe(self, driver_id):
        if driver_id not in self.subscriptions:
            self.subscriptions.append(driver_id)
            db.session.commit()

    def unsubscribe(self, driver_id):
        if driver_id in self.subscriptions:
            self.subscriptions.remove(driver_id)
            db.session.commit()

    def receive_notif(self, message):
        if self.inbox is None:
            self.inbox = []

        if len(self.inbox) >= MAX_INBOX_SIZE:
            self.inbox.pop(0)

        timestamp = datetime.now().strftime("%Y:%m:%d:%H:%M:%S")
        notif = f"[{timestamp}]: {message}"
        self.inbox.append(notif)

        db.session.add(self)
        db.session.commit()

    def get_json(self):
        user_json = super().get_json()
        user_json['areaId'] = self.areaId
        user_json['streetId'] = self.streetId
        user_json['houseNumber'] = self.houseNumber
        user_json['inbox'] = self.inbox
        return user_json

    def request_stop(self, driveId):
        # Validate that the drive exists before creating a stop.
        try:
            drive = Drive.query.get(driveId)
            if not drive:
                return None
            new_stop = Stop(driveId=driveId, residentId=self.id)
            db.session.add(new_stop)
            db.session.commit()
            return new_stop
        except Exception:
            db.session.rollback()
            return None

    def cancel_stop(self, stopId):
        stop = Stop.query.get(stopId)
        if stop:
            db.session.delete(stop)
            db.session.commit()
        return

    def receive_notif(self, message):
        if self.inbox is None:
            self.inbox = []

        if len(self.inbox) >= MAX_INBOX_SIZE:
            self.inbox.pop(0)

        timestamp = datetime.now().strftime("%Y:%m:%d:%H:%M:%S")
        notif = f"[{timestamp}]: {message}"
        self.inbox.append(notif)
        db.session.add(self)
        db.session.commit()

    def view_inbox(self):
        return self.inbox

    def view_driver_stats(self, driverId):
        driver = Driver.query.get(driverId)
        return driver
