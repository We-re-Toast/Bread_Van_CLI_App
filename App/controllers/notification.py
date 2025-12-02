from App.models import Notification
from App.database import db

def create_notification(resident_id, message, driver_id=None):
    notification = Notification(resident_id=resident_id, message=message, driver_id=driver_id)
    db.session.add(notification)
    db.session.commit()
    return notification

def get_notifications(resident_id):
    notificationList = Notification.query.filter_by(resident_id=resident_id)
    return notificationList.order_by(Notification.date.desc()).all()