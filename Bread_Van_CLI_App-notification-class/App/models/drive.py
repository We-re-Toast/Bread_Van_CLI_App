from App.database import db

class Drive(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    driverId = db.Column(db.Integer, db.ForeignKey('driver.id'), nullable=False)
    areaId = db.Column(db.Integer, db.ForeignKey('area.id'), nullable=False)
    streetId = db.Column(db.Integer, db.ForeignKey('street.id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    time = db.Column(db.Time, nullable=False)
    status = db.Column(db.String(20), nullable=False)

    area = db.relationship("Area", backref="drives")
    street = db.relationship("Street", backref="drives")

    def __init__(self, driverId, areaId, streetId, date, time, status):
        self.driverId = driverId
        self.areaId = areaId
        self.streetId = streetId
        self.date = date
        self.time = time
        self.status = status

    def get_json(self):
        return {
            'id': self.id,
            'driverId': self.driverId,
            'areaId': self.areaId,
            'streetId': self.streetId,
            'date': self.date.strftime("%Y-%m-%d") if self.date else None,
            'time': self.time.strftime("%H:%M:%S") if self.time else None,
            'status': self.status
        }