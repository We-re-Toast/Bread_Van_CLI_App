from datetime import datetime
from App.database import db

class Notification(db.Model):
    __tablename__ = "notifications"

    id = db.Column(db.Integer, primary_key=True)
    resident_id = db.Column(db.Integer, db.ForeignKey("resident.id"), nullable=False)
    driver_id = db.Column(db.Integer, db.ForeignKey("driver.id"), nullable=True)
    message = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, default=datetime.now)

    def __init__(self, resident_id, message, driver_id=None):
        self.resident_id = resident_id
        self.message = message
        self.driver_id = driver_id
        self.date = datetime.now()

    def get_json(self):
        return {
            "id": self.id,
            "resident_id": self.resident_id,
            "driver_id": self.driver_id,
            "message": self.message,
            "date": self.date
        }
