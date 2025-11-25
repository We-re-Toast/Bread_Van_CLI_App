from werkzeug.security import check_password_hash, generate_password_hash
from App.database import db
from .drive import Drive

class User(db.Model):
    __tablename__ = "user"
    
    id = db.Column(db.Integer, primary_key=True)
    #street_id = db.Column(db.Integer, db.ForeignKey('street.id'))
    username =  db.Column(db.String(20), nullable=False, unique=True)
    password = db.Column(db.String(256), nullable=False)
    logged_in = db.Column(db.Boolean, nullable=False, default=False)
    type = db.Column(db.String(50))

    __mapper_args__ = {
        "polymorphic_on": type,
        "polymorphic_identity": "user"
    }

    def __init__(self, username, password):
        self.username = username
        self.set_password(password)
        self.logged_in = False
        self.inbox = []

    def get_json(self):
        return{
            'id': self.id,
            'username': self.username
        }

    def set_password(self, password):
        """Create hashed password."""
        self.password = generate_password_hash(password)
    
    def check_password(self, password):
        """Check hashed password."""
        return check_password_hash(self.password, password)

    def login(self, password):
        if self.check_password(password):
            self.logged_in = True
            db.session.commit()
            return True
        return False

    def logout(self):
        self.logged_in = False
        db.session.commit()

    def view_street_drives(self, areaId, streetId):
        return Drive.query.filter_by(areaId=areaId, streetId=streetId).all()
    

