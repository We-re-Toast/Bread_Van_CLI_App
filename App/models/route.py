from App.database import db

class Route(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    scheduledDriver = db.Column(db.Integer, db.ForeignKey('driver.id'), nullable=False)
    scheduledDate = db.Column(db.Date, nullable=True)
    scheduledTime = db.Column(db.DateTime, nullable=True)
    scheduledArea = db.Column(db.String(100), nullable=True)
    
    # A Route (Trip) is scheduled for a specific area and time but also
    # A route is just a collection of Stops - stop class holds the relevant residents and adresses.
    stops = db.relationship('Stop',back_populates='route', cascade='all, delete-orphan', lazy='joined') 

    def __init__(self, scheduledDriver, scheduledDate=None, scheduledTime=None, scheduledArea=None):
        self.scheduledDriver = scheduledDriver
        self.scheduledDate = scheduledDate
        self.scheduledTime = scheduledTime
        self.scheduledArea = scheduledArea
    
    def get_json(self):
        return {
            'id': self.id,
            'scheduledDriver': self.scheduledDriver,
            'scheduledDate': self.scheduledDate,
            'scheduledTime': self.scheduledTime,
            'scheduledArea': self.scheduledArea,
            'stops': [stop.get_json() for stop in self.stops]
        }
