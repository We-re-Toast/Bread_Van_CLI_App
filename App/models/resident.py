from datetime import datetime
from sqlalchemy.ext.mutable import MutableList
from sqlalchemy import JSON

from App.database import db
from .user import User

MAX_INBOX_SIZE = 50

class Resident(User):
    __tablename__ = "resident"

    id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    areaId = db.Column(db.Integer, db.ForeignKey('area.id'), nullable=False)
    streetId = db.Column(db.Integer, db.ForeignKey('street.id'), nullable=False)
    houseNumber = db.Column(db.Integer, nullable=False)
    inbox = db.Column(MutableList.as_mutable(JSON), default=[])
    notification_preferences = db.Column(MutableList.as_mutable(JSON), default=["drive_scheduled", "menu_updated", "eta_updated"])
    subscribed_drives = db.Column(MutableList.as_mutable(JSON), default=[])

    area = db.relationship("Area", backref='residents')
    street = db.relationship("Street", backref='residents')
    stops = db.relationship('Stop', backref='resident')

    __mapper_args__ = {
        "polymorphic_identity": "Resident",
    }

    def __init__(self, username, password, areaId, streetId, houseNumber):
        super().__init__(username, password)
        self.areaId = areaId
        self.streetId = streetId
        self.houseNumber = houseNumber
        self.subscribed_drives = []
        self.notification_preferences = ["drive_scheduled", "menu_updated", "eta_updated"]

    def get_json(self):
        user_json = super().get_json()
        user_json['areaId'] = self.areaId
        user_json['streetId'] = self.streetId
        user_json['houseNumber'] = self.houseNumber
        user_json['inbox'] = self.inbox
        user_json['notification_preferences'] = self.notification_preferences
        user_json['subscribed_drives'] = self.subscribed_drives
        return user_json

    # Observer pattern implementation
    def update(self, drive, menu, eta):
        """Called when a drive they're subscribed to is updated"""
        if "menu_updated" in self.notification_preferences and menu:
            message = f"Menu updated for drive on {drive.date}: {menu}"
            if eta:
                message += f" | ETA: {eta.strftime('%H:%M')}"
            self.receive_notif(message, "menu_updated", drive.id)
        
        elif "eta_updated" in self.notification_preferences and eta:
            message = f"ETA updated for drive on {drive.date}: {eta.strftime('%H:%M')}"
            self.receive_notif(message, "eta_updated", drive.id)

    def subscribe_to_drive(self, drive_id):
        """Subscribe to notifications for a specific drive"""
        if drive_id not in self.subscribed_drives:
            self.subscribed_drives.append(drive_id)
            db.session.commit()

    def unsubscribe_from_drive(self, drive_id):
        """Unsubscribe from notifications for a specific drive"""
        if drive_id in self.subscribed_drives:
            self.subscribed_drives.remove(drive_id)
            db.session.commit()

    def is_subscribed_to_drive(self, drive_id):
        return drive_id in self.subscribed_drives

    def update_notification_preferences(self, preferences):
        """Update what types of notifications the resident wants to receive"""
        self.notification_preferences = preferences
        db.session.commit()

    def request_stop(self, driveId):
        try:
            from .stop import Stop
            new_stop = Stop(driveId=driveId, residentId=self.id)
            db.session.add(new_stop)
            db.session.commit()
            
            # Notify about stop request
            self.receive_notif(f"Stop requested for drive {driveId}", "stop_requested", driveId)
            return new_stop
        except Exception:
            db.session.rollback()
            return None

    def cancel_stop(self, stopId):
        from .stop import Stop
        stop = Stop.query.get(stopId)
        if stop:
            drive_id = stop.driveId
            db.session.delete(stop)
            db.session.commit()
            self.receive_notif(f"Stop cancelled for drive {drive_id}", "stop_cancelled", drive_id)
        return

    def receive_notif(self, message, notification_type="info", drive_id=None):
        """Receive a notification and store in inbox"""
        if self.inbox is None:
            self.inbox = []

        if len(self.inbox) >= MAX_INBOX_SIZE:
            self.inbox.pop(0)

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        notification = {
            "timestamp": timestamp,
            "message": message,
            "type": notification_type,
            "drive_id": drive_id,
            "read": False
        }
        
        self.inbox.append(notification)
        db.session.commit()

    def mark_notification_read(self, notification_index):
        """Mark a specific notification as read"""
        if 0 <= notification_index < len(self.inbox):
            self.inbox[notification_index]["read"] = True
            db.session.commit()

    def mark_all_notifications_read(self):
        """Mark all notifications as read"""
        for notification in self.inbox:
            notification["read"] = True
        db.session.commit()

    def clear_inbox(self):
        """Clear all notifications"""
        self.inbox = []
        db.session.commit()

    def get_unread_count(self):
        """Get count of unread notifications"""
        return sum(1 for notification in self.inbox if not notification.get("read", False))

    def view_inbox(self, unread_only=False):
        """View inbox, optionally filtered by unread status"""
        if unread_only:
            return [notification for notification in self.inbox if not notification.get("read", False)]
        return self.inbox

    def view_driver_stats(self, driverId):
        from .driver import Driver
        driver = Driver.query.get(driverId)
        return driver