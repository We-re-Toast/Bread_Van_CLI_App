from datetime import datetime
from sqlalchemy.ext.mutable import MutableList
from sqlalchemy import JSON

from App.database import db
from App.models.user import User
from App.models.observer import Observer
from App.models.stop import Stop

MAX_INBOX_SIZE = 20


class Resident(User, Observer):
    __tablename__ = "resident"

    id = db.Column(db.Integer, db.ForeignKey("user.id"), primary_key=True)
    areaId = db.Column(db.Integer, db.ForeignKey("area.id"), nullable=False)
    streetId = db.Column(db.Integer, db.ForeignKey("street.id"), nullable=False)
    houseNumber = db.Column(db.Integer, nullable=False)

    inbox = db.Column(MutableList.as_mutable(JSON), default=[])

    area = db.relationship("Area", backref="residents")
    stops = db.relationship("Stop", backref="resident")

    __mapper_args__ = {"polymorphic_identity": "Resident"}

    def __init__(self, username, password, areaId, streetId, houseNumber):
        super().__init__(username, password)
        self.areaId = areaId
        self.streetId = streetId
        self.houseNumber = houseNumber


    # Observer method
    def update(self, message):
        self.receive_notif(message)

    def receive_notif(self, message):

        if self.inbox is None:
            self.inbox = []

        # Maintain inbox size
        if len(self.inbox) >= MAX_INBOX_SIZE:
            self.inbox.pop(0)

        timestamp = datetime.now().strftime("%Y:%m:%d:%H:%M:%S")
        notif = f"[{timestamp}]: {message}"

        self.inbox.append(notif)
        db.session.add(self)
        db.session.commit()

    def request_stop(self, driveId):
        try:
            new_stop = Stop(driveId=driveId, residentId=self.id)
            db.session.add(new_stop)
            db.session.commit()
            return new_stop
        except:
            db.session.rollback()
            return None

    def cancel_stop(self, stopId):
        stop = Stop.query.get(stopId)
        if stop:
            db.session.delete(stop)
            db.session.commit()


    def view_inbox(self):
        return self.inbox

    def view_driver_stats(self, driverId):
        from App.models.driver import Driver
        return Driver.query.get(driverId)

    def get_json(self):
        base = super().get_json()
        base.update({
            "areaId": self.areaId,
            "streetId": self.streetId,
            "houseNumber": self.houseNumber,
            "inbox": self.inbox
        })
        return base
