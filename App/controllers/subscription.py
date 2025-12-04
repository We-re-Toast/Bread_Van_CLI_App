from App import db
from App.models import Subscription, Resident
from App.exceptions import ResourceNotFound, ValidationError

def subscribe_to_street(resident_id, street_id):
    existing = Subscription.query.filter_by(resident_id=resident_id, street_id=street_id).first()
    if existing:
        raise ValidationError("You are already subscribed to this street")
    
    new_sub = Subscription(resident_id=resident_id, street_id=street_id)
    db.session.add(new_sub)
    db.session.commit()
    return new_sub


def unsubscribe_from_street(resident_id, street_id):
    sub = Subscription.query.filter_by(resident_id=resident_id, street_id=street_id).first()
    if not sub:
        raise ResourceNotFound("Subscription not found")
    else:
        db.session.delete(sub)
        db.session.commit()
        return True


def view_subscriptions(resident_id):
    resident = Resident.query.get(resident_id)
    if not resident:
        raise ResourceNotFound("Resident not found")
    return resident.subscriptions
