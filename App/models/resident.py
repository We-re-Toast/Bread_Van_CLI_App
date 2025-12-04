from App.database import db
from .user import User


class Resident(User):

    id = db.Column(db.Integer, db.ForeignKey("user.id"), primary_key=True)
    house_number = db.Column(db.Integer, nullable=False)

    """Foreign Keys"""
    area_id = db.Column(db.Integer, db.ForeignKey("area.id"), nullable=False)
    street_id = db.Column(db.Integer, db.ForeignKey("street.id"), nullable=False)

    """Relationships"""
    stop_requests = db.relationship("StopRequest", backref="resident", lazy=True)
    subscriptions = db.relationship("Subscription", backref="resident", lazy=True, cascade="all, delete-orphan")
    inbox = db.relationship("Notification", backref="resident", lazy=True, cascade="all, delete-orphan")

    __mapper_args__ = {
        "polymorphic_identity": "resident",
    }

    def __init__(self, username, password, area_id, street_id, house_number):
        super().__init__(username, password)
        self.area_id = area_id
        self.street_id = street_id
        self.house_number = house_number

    def __repr__(self):
        return f"ID: {self.id} | Username: {self.username} | Area: {self.area.name} | Street: {self.street.name} | House Number: {self.house_number}"

    def get_json(self):
        return {
            "id": self.id,
            "username": self.username,
            "area_id": self.area_id,
            "area_name": self.area.name,
            "street_id": self.street_id,
            "street_name": self.street.name,
            "house_number": self.house_number,
        }
