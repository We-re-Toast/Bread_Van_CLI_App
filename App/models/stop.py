from App.database import db


class Stop(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    #driveId = db.Column(db.Integer, db.ForeignKey('drive.id'), nullable=False) No longer required
    routeId = db.Column(db.Integer, db.ForeignKey('route.id'), nullable=True) #must link back to a route
    residentId = db.Column(db.Integer, db.ForeignKey('resident.id'), nullable=False) #resident requests stops.

    # optional relationship back to Route (a Stop can belong to a Route)
    route = db.relationship('Route', back_populates='stops')

    def __init__(self, residentId, routeId=None):
        self.residentId = residentId
        self.routeId = routeId

    def get_json(self):
        return {
            'id': self.id,
            'routeId': self.routeId,
            'residentId': self.residentId
        }
