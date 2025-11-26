from App.database import db
from .observer import SubjectMixin

class Drive(db.Model, SubjectMixin):
    id = db.Column(db.Integer, primary_key=True)
    driverId = db.Column(db.Integer, db.ForeignKey('driver.id'), nullable=False)
    areaId = db.Column(db.Integer, db.ForeignKey('area.id'), nullable=False)
    streetId = db.Column(db.Integer, db.ForeignKey('street.id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    time = db.Column(db.Time, nullable=False)
    status = db.Column(db.String(20), nullable=False)
    menu = db.Column(db.String(200), nullable=True)
    eta = db.Column(db.Time, nullable=True)

    area = db.relationship("Area", backref="drives")
    street = db.relationship("Street", backref="drives")

    def __init__(self, driverId, areaId, streetId, date, time, status, menu=None, eta=None):
        db.Model.__init__(self)
        SubjectMixin.__init__(self)
        self.driverId = driverId
        self.areaId = areaId
        self.streetId = streetId
        self.date = date
        self.time = time
        self.status = status
        self.menu = menu
        self.eta = eta

    def get_json(self):
        return {
            'id': self.id,
            'driverId': self.driverId,
            'areaId': self.areaId,
            'streetId': self.streetId,
            'date': self.date,
            'time': self.time,
            'status': self.status,
            'menu': self.menu,
            'eta': self.eta
        }

    def set_menu_and_eta(self, menu, eta):
        self.menu = menu
        self.eta = eta
        db.session.commit()
        self.notify_subscribers()

    def notify_subscribers(self):
        """Notify all residents subscribed to this drive"""
        from .resident import Resident
        subscribed_residents = Resident.query.filter(
            Resident.subscribed_drives.contains([self.id])
        ).all()
        
        for resident in subscribed_residents:
            resident.update(self, self.menu, self.eta)

    def notify_new_drive(self):
        """Notify all residents in the area/street about a new drive"""
        from .resident import Resident
        residents_in_area = Resident.query.filter_by(
            areaId=self.areaId, 
            streetId=self.streetId
        ).all()
        
        for resident in residents_in_area:
            if "drive_scheduled" in getattr(resident, 'notification_preferences', []):
                message = f"New bread van scheduled for {self.date} at {self.time}"
                if self.menu:
                    message += f" | Menu: {self.menu}"
                if self.eta:
                    message += f" | ETA: {self.eta.strftime('%H:%M')}"
                
                resident.receive_notif(message, "drive_scheduled", self.id)
                
                resident.subscribe_to_drive(self.id)