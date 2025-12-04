from App import db
from App.models import Notification, Subscription, Resident, DriveItem
from App.exceptions import ValidationError, ResourceNotFound
from datetime import datetime


def notify_subscribers(drive, message):
    """
    Observer pattern: Notify all residents subscribed to the street of the scheduled drive.
    """
    subscriptions = Subscription.query.filter_by(street_id=drive.street_id).all()
    timestamp = datetime.now()
    for sub in subscriptions:
        notification = Notification(
            resident_id=sub.resident_id, message=message, timestamp=timestamp
        )
        db.session.add(notification)

    db.session.commit()


def get_notification_history_json(resident_id):
    resident = Resident.query.get(resident_id)
    if not resident:
        raise ResourceNotFound(f"Resident with ID '{resident_id}' does not exist")
    notifications = Notification.query.filter_by(resident_id=resident_id).all()
    return [notification.get_json() for notification in notifications]

def get_notification_history(resident_id):
    resident = Resident.query.get(resident_id)
    if not resident:
        raise ResourceNotFound(f"Resident with ID '{resident_id}' does not exist")
    notifications = Notification.query.filter_by(resident_id=resident_id).all()
    return notifications


def mark_notification_as_read(notification_id, resident_id):
    notification = Notification.query.get(notification_id)
    if not notification:
        raise ResourceNotFound(f"Notification with ID '{notification_id}' does not exist")

    if notification.resident_id != resident_id:
        raise ValidationError("You can only mark your own notifications as read")

    notification.is_read = True
    db.session.commit()
    return True
