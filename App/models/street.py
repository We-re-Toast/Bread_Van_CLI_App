from App.database import db


class Street(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    area_id = db.Column(db.Integer, db.ForeignKey("area.id"), nullable=False)

    """Relationships"""
    # A street can have one or many residents
    residents = db.relationship("Resident", backref="street", lazy=True)

    # A street can have zero or many subscribers
    subscribers = db.relationship("Subscription", backref="street", lazy=True)

    def __init__(self, name, area_id):
        self.name = name
        self.area_id = area_id

    def get_json(self):
        return {"id": self.id, "name": self.name, "area_id": self.area_id}
