from App.database import db
from datetime import datetime

class Notification(db.Model):
    _tablename_ = "notification"

    id = db.Column(db.Integer, primary_key=True)
    residientId = db.Column(db.Integer, db.ForeignKey('resident.id'), nullable=False)
    message = db.Column(db.String(255), nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, residentId, message):
        self.residientId = residentId
        self.message = message

    def __repr__(self):
        return f"<Notification {self.id}: {self.message}>"

