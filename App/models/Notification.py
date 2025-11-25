from werkzeug.security import check_password_hash, generate_password_hash
from App.database import db


class Notification(db.Model):
    __tablename__ = "notification"
    
    id = db.Column(db.Integer, primary_key=True)
    resident_id = db.Column(db.Integer, db.ForeignKey('resident.id'))
    drive_id = db.Column(db.Integer, db.ForeignKey('drive.id'))
   # drive = db.relationship('Drive', back_populates = 'notifications')
    # resident = db.relationship('Resident', back_populates = 'notifications')
   