from App.database import db
from .enums import DriveStatus


class Drive(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    time = db.Column(db.Time, nullable=False)
    status = db.Column(db.String(20), nullable=False)

    """Foreign Keys"""
    driver_id = db.Column(db.Integer, db.ForeignKey("driver.id"), nullable=False)
    area_id = db.Column(db.Integer, db.ForeignKey("area.id"), nullable=False)
    street_id = db.Column(db.Integer, db.ForeignKey("street.id"), nullable=False)

    """Relationships"""
    stop_requests = db.relationship("StopRequest", backref="drive", lazy=True)
    items = db.relationship("DriveItem", backref="drive", lazy=True, cascade="all, delete-orphan")
    area = db.relationship("Area", backref="drives")
    street = db.relationship("Street", backref="drives")

    def __init__(
        self, driver_id, area_id, street_id, date, time, status=DriveStatus.SCHEDULED
    ):
        self.driver_id = driver_id
        self.area_id = area_id
        self.street_id = street_id
        self.date = date
        self.time = time
        self.status = status

    def __repr__(self):
        return f"Drive ID: {self.id} | Area ID: {self.area_id} | Street ID: {self.street_id} | Driver ID: {self.driver_id} | Date: {self.date} | Time: {self.time} | Status: {self.status}"

    def get_json(self):
        return {
            "id": self.id,
            "driver_id": self.driver_id,
            "area_id": self.area_id,
            "street_id": self.street_id,
            "date": str(self.date),
            "time": str(self.time),
            "status": self.status,
            "items": [item.get_json() for item in self.items],
        }
