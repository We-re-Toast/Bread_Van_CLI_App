from App.database import db
from datetime import datetime
from .user import User
from .drive import Drive
from .street import Street
# Remove: from .resident import Resident  # This causes circular import


class Driver(User):
    __tablename__ = "driver"

    id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    status = db.Column(db.String(20), nullable=False)
    drives = db.relationship('Drive', backref='driver')
    # Note: areaId and streetId are runtime state (not database columns)
    # street_id is inherited from User class

    __mapper_args__ = {
        "polymorphic_identity": "Driver",
    }

    def __init__(self, username, password, status, areaId=None, streetId=None):
        super().__init__(username, password)
        self.status = status
        # Runtime state for tracking current location during drives
        self.areaId = areaId
        self.streetId = streetId
        # Set inherited street_id if streetId is provided
        if streetId is not None:
            self.street_id = streetId

    
    def list():
        return Driver.query.all()
    

    def get_by_id(id):
        return Driver.query.get(id)


    def get_json(self):
        user_json = super().get_json()
        user_json['status'] = self.status
        # Include street_id from User (inherited)
        user_json['street_id'] = self.street_id
        # Include runtime state if needed
        if hasattr(self, 'areaId'):
            user_json['areaId'] = self.areaId
        if hasattr(self, 'streetId'):
            user_json['streetId'] = self.streetId
        return user_json

    def login(self, password):
        if super().login(password):
            # Reset runtime state
            self.areaId = None
            self.streetId = None
            self.street_id = None  # Clear inherited street_id
            self.status = "Available"
            db.session.commit()
            return True
        return False

    def logout(self):
        super().logout()
        self.status = "Offline"
        db.session.commit()

    def schedule_drive(self, areaId, streetId, date_str, time_str, menu_id):
        try:
            date = datetime.strptime(date_str, "%Y-%m-%d").date()
            time = datetime.strptime(time_str, "%H:%M").time()
        except Exception:
            print(
                "Invalid date or time format. Please use YYYY-MM-DD for date and HH:MM for time."
            )
            return

        new_drive = Drive(driverId=self.id,
                          areaId=areaId,
                          streetId=streetId,
                          date=date,
                          time=time,
                          menu_id=menu_id,
                          status="Upcoming")
        db.session.add(new_drive)
        db.session.commit()
        return new_drive

    def cancel_drive(self, driveId):  
        drive = Drive.query.get(driveId)
        if drive:
            drive.status = "Cancelled"
            db.session.commit()

           
            from .StreetSubscription import StreetSubscription
            from .resident import Resident
            
            if drive.streetId is not None:
                subscriptions = StreetSubscription.query.filter_by(street_id=drive.streetId).all()
                for subscription in subscriptions:
                    resident = Resident.query.get(subscription.resident_id)
                    if resident:
                        resident.receive_notif(
                            f"CANCELLED: Drive {drive.id} by {self.id} on {drive.date} at {drive.time}"
                        )
                db.session.commit()
        return None

    def view_drives(self):
        return Drive.query.filter_by(driverId=self.id).all()

    def start_drive(self, driveId):
        drive = Drive.query.get(driveId)
        if drive:
            self.status = "Busy"
            self.areaId = drive.areaId
            self.streetId = drive.streetId
            self.street_id = drive.streetId
            drive.status = "In Progress"
            db.session.commit()
            return drive
        return None

    def end_drive(self, driveId):
        drive = Drive.query.get(driveId)
        if drive:
            self.status = "Available"
            drive.status = "Completed"
            db.session.commit()
            return drive
        return None

    def view_requested_stops(self, driveId):
        drive = Drive.query.get(driveId)
        if drive:
            return drive.stops
        return None