from App.database import db
from .user import User
from .enums import DriverStatus


class Driver(User):
    id = db.Column(db.Integer, db.ForeignKey("user.id"), primary_key=True)
    area_id = db.Column(db.Integer, db.ForeignKey("area.id"), nullable=True)
    street_id = db.Column(db.Integer, db.ForeignKey("street.id"), nullable=True)
    status = db.Column(db.String(20), nullable=False)

    """Relationships"""
    drives = db.relationship("Drive", backref="driver", lazy=True)

    area = db.relationship("Area", backref="drivers", lazy=True)
    street = db.relationship("Street", backref="drivers", lazy=True)

    __mapper_args__ = {
        "polymorphic_identity": "driver",
    }

    def __init__(
        self,
        username,
        password,
        status=DriverStatus.OFF_DUTY,
        area_id=None,
        street_id=None,
    ):
        super().__init__(username, password)
        self.status = status
        self.area_id = area_id
        self.street_id = street_id

    def __repr__(self):
        return f"ID: {self.id} | Driver: {self.username} | Status: {self.status} | Area ID: {self.area_id} | Street ID: {self.street_id}"

    def get_json(self):
        return {
            "id": self.id,
            "username": self.username,
            "status": self.status,
            "area_id": self.area_id,
            "street_id": self.street_id,
        }
