from App.database import db


class Stop(db.Model):
    __tablename__ = 'stop'
    id = db.Column(db.Integer, primary_key=True)
    driveId = db.Column(db.Integer, db.ForeignKey('drive.id'), nullable=False)
    residentId = db.Column(db.Integer,
                           db.ForeignKey('resident.id'),
                           nullable=False)

    drive = db.relationship("Drive", back_populates="stops")  
    resident = db.relationship("Resident", back_populates="stops")  
    
    def __init__(self, driveId, residentId):
        self.driveId = driveId
        self.residentId = residentId

    def get_json(self):
        return {
            'id': self.id,
            'driveId': self.driveId,
            'residentId': self.residentId
        }