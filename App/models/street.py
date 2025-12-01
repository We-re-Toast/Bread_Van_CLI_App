# App/models/street.py
from App.database import db

class Street(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False, unique=True)
    areaId = db.Column(db.Integer, db.ForeignKey('area.id'), nullable=False)

    def __init__(self, name, areaId):
        self.name = name
        self.areaId = areaId

    def get_json(self):
        return {
            'id': self.id,
            'name': self.name,
            'areaId': self.areaId
        }