from App.database import db


class StopRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.String(200), nullable=True)

    """Foreign keys"""
    resident_id = db.Column(db.Integer, db.ForeignKey("resident.id"), nullable=False)
    drive_id = db.Column(db.Integer, db.ForeignKey("drive.id"), nullable=False)

    def __init__(self, drive_id, resident_id, message):
        self.drive_id = drive_id
        self.resident_id = resident_id
        self.message = message

    def __repr__(self):
        return f"ID: {self.id}, Drive ID: {self.drive_id}, Resident ID: {self.resident_id}, Message: {self.message}"

    def get_json(self):
        return {
            "id": self.id,
            "drive_id": self.drive_id,
            "resident_id": self.resident_id,
            "message": self.message,
        }
