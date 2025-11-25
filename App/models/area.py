from App.database import db


class Area(db.Model):
    __tablename__ = 'area'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False, unique=True)
   # driveId = db.Column(db.Integer, db.ForeignKey('drive.id'), nullable=False)
    streets = db.relationship('Street', backref='area')
   # drive = db.relationship("Drive", back_populates="area")
   # residents = db.relationship('Resident', back_populates='area')

    def __init__(self, name):
        self.name = name

    def get_json(self):
        return {'id': self.id, 'name': self.name}
