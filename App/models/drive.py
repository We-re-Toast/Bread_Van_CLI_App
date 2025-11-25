from App.database import db
from .Notification import Notification

class Drive(db.Model):
    __tablename__ = 'drive'
    id = db.Column(db.Integer, primary_key=True)
    driverId = db.Column(db.Integer, db.ForeignKey('driver.id'), nullable=False)
    areaId = db.Column(db.Integer, db.ForeignKey('area.id'), nullable=False)
    menu_id = db.Column(db.Integer,db.ForeignKey('menu.id'))
    streetId = db.Column(db.Integer, db.ForeignKey('street.id'), nullable=False)
    date = db.Column(db.Date, nullable=False)  
    time = db.Column(db.Time, nullable=False)
    status = db.Column(db.String(20), nullable=False) # enum ?? 
    stops = db.relationship('Stop', back_populates='drive')
    notifications = db.relationship('Notification', backref='drive')
    
    
    def __init__(self, driverId, areaId, streetId, date, time, status, menu_id=None):
        self.driverId = driverId
        self.areaId = areaId
        self.streetId = streetId
        self.date = date
        self.time = time
        self.status = status
        self.menu_id = menu_id

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