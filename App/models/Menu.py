from App.database import db

class Menu(db.Model):
    __tablename__ = "menu"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable = False)
    items = db.relationship('MenuBreadItem', backref='menu')
    drives = db.relationship('Drive', backref = 'menu')
    
    def __init__(self, name):
        self.name = name