from App.database import db

class StreetSubscription(db.Model):
    __tablename__ = 'street_subscription'
    resident_id = db.Column(db.Integer, db.ForeignKey('resident.id'), primary_key=True)
    street_id = db.Column(db.Integer, db.ForeignKey('street.id'), primary_key=True)
   # street = db.relationship('Street', back_populates='subscriptions')
   #  resident = db.relationship('Resident', back_populates='subscriptions')

    def list():
        return StreetSubscription.query.all()

    def __init__(self, resident_id, street_id):

        self.resident_id = resident_id
        self.street_id = street_id