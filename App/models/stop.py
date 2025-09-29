from App.database import db


class Stop(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    driveId = db.Column(db.Integer, db.ForeignKey('drive.id'), nullable=False)
    residentId = db.Column(db.Integer,
                           db.ForeignKey('resident.id'),
                           nullable=False)

    drive = db.relationship("Drive", backref="stops")

    def __init__(self, driveId, residentId):
        self.driveId = driveId
        self.residentId = residentId

    def get_json(self):
        return {
            'id': self.id,
            'driveId': self.driveId,
            'residentId': self.residentId
        }
