from App.database import db


class Route(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    driverId = db.Column(db.Integer, db.ForeignKey('driver.id'), nullable=False)

    # one-to-many relationship: a Route has many Stop entries
    stops = db.relationship(
        'Stop',
        back_populates='route',
        cascade='all, delete-orphan',
        lazy='joined'
    )

    def __init__(self, driverId):
        self.driverId = driverId

    def get_json(self):
        return {
            'id': self.id,
            'driverId': self.driverId,
            'stops': [s.get_json() for s in self.stops]
        }
from App.database import db

class Route(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    driverId = db.Column(db.Integer, db.ForeignKey('driver.id'), nullable=False)
