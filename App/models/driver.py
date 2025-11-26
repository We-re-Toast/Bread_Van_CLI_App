from App.database import db
from datetime import datetime
from .user import User

class Driver(User):
    __tablename__ = "driver"

    id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    status = db.Column(db.String(20), nullable=False)
    areaId = db.Column(db.Integer, db.ForeignKey('area.id'), nullable=False)
    streetId = db.Column(db.Integer, db.ForeignKey('street.id'))

    area = db.relationship("Area", backref="drivers")
    street = db.relationship("Street", backref="drivers")

    __mapper_args__ = {
        "polymorphic_identity": "Driver",
    }

    def __init__(self, username, password, status, areaId, streetId):
        super().__init__(username, password)
        self.status = status
        self.areaId = areaId
        self.streetId = streetId

    def get_json(self):
        user_json = super().get_json()
        user_json['status'] = self.status
        user_json['area'] = self.area.name
        user_json['street'] = self.street.name
        return user_json

    def login(self, password):
        if super().login(password):
            self.areaId = 0
            self.streetId = 0
            self.status = "Available"
            db.session.commit()
            return True
        return False

    def logout(self):
        super().logout()
        self.status = "Offline"
        db.session.commit()

    def schedule_drive(self, areaId, streetId, date_str, time_str, menu=None, eta=None):
        try:
            # Import locally to avoid circular imports
            from .drive import Drive
            
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
                        status="Upcoming",
                        menu=menu,
                        eta=eta)
        db.session.add(new_drive)
        db.session.commit()
        
        menu_text = f"Menu: {menu}" if menu else "No menu specified"
        eta_text = f"ETA: {eta}" if eta else f"at {time_str}"
        
        # Note: You'll need to implement notification_service or remove this part
        # notification_service.notify(
        #     str(streetId),
        #     f"Bread van scheduled for {date_str} {eta_text}. {menu_text}",
        #     notification_data
        # )
        
        return new_drive

    def cancel_drive(self, driveId):
        from .drive import Drive

        drive = Drive.query.get(driveId)
        if drive:
            drive.status = "Cancelled"
            db.session.commit()
        return None

    def view_drives(self):
        from .drive import Drive
        
        return Drive.query.filter_by(driverId=self.id).all()

    def start_drive(self, driveId):
        from .drive import Drive

        drive = Drive.query.get(driveId)
        if drive:
            self.status = "Busy"
            self.areaId = drive.areaId
            self.streetId = drive.streetId
            drive.status = "In Progress"
            db.session.commit()
            return drive
        return None

    def end_drive(self, driveId):
        # Import locally to avoid circular imports
        from .drive import Drive
        drive = Drive.query.get(driveId)
        if drive:
            self.status = "Available"
            self.streetId = None
            drive.status = "Completed"
            db.session.commit()
            return drive
        return None

    def view_requested_stops(self, driveId):
        from .drive import Drive

        drive = Drive.query.get(driveId)
        if drive:
            return drive.stops
        return None

    def update_drive_menu(self, driveId, menu):
        from .drive import Drive

        drive = Drive.query.get(driveId)
        if drive and drive.driverId == self.id:
            drive.menu = menu
            db.session.commit()
            return drive
        return None

    def update_drive_eta(self, driveId, eta):
        from .drive import Drive

        drive = Drive.query.get(driveId)
        if drive and drive.driverId == self.id:
            drive.eta = eta
            db.session.commit()
            return drive
        return None