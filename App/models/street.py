from App.database import db

class Street(db.Model):
    __tablename__ = 'street'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False, unique=True)
    areaId = db.Column(db.Integer, db.ForeignKey('area.id'), nullable=False)
   
    drives = db.relationship('Drive', backref ='street')
    subscriptions = db.relationship('StreetSubscription', backref ='street')
   
    
    def list():
        return Street.query.all()


    def __init__(self, name, areaId):
        self.name = name
        self.areaId = areaId

    def get_json(self):
        return {
            'id': self.id,
            'name': self.name,
            'areaId': self.areaId
        }