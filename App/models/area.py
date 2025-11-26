from App.database import db


class Area(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False, unique=True)

    """Relationships"""
    streets = db.relationship("Street", backref="area", lazy=True)
    residents = db.relationship("Resident", backref="area", lazy=True)

    def __init__(self, name):
        self.name = name

    def get_json(self):
        return {"id": self.id, "name": self.name}
