from App.database import db


class Subscription(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    """Foreign keys"""
    resident_id = db.Column(db.Integer, db.ForeignKey("resident.id"), nullable=False)
    street_id = db.Column(db.Integer, db.ForeignKey("street.id"), nullable=False)

    def __init__(self, resident_id, street_id):
        self.resident_id = resident_id
        self.street_id = street_id

    def __repr__(self):
        return f"<Subscription {self.id} - Resident {self.resident_id} to Street {self.street_id}>"

    def to_json(self):
        return {
            "id": self.id,
            "resident_id": self.resident_id,
            "street_id": self.street_id,
        }
