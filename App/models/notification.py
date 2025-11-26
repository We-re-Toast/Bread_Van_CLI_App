from App.database import db


class Notification(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.String(255), nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False)
    is_read = db.Column(db.Boolean, default=False, nullable=False)

    resident_id = db.Column(db.Integer, db.ForeignKey("resident.id"), nullable=False)

    def __init__(self, resident_id, message, timestamp):
        self.resident_id = resident_id
        self.message = message
        self.timestamp = timestamp

    def __repr__(self):
        return f"Notification ID: {self.id} | Resident ID: {self.resident_id} | Message: {self.message} | Timestamp: {self.timestamp} | Read: {self.is_read}"

    def get_json(self):
        return {
            "id": self.id,
            "resident_id": self.resident_id,
            "message": self.message,
            "timestamp": self.timestamp.isoformat(),
            "is_read": self.is_read,
        }
