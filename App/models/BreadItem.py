from App.database import db

class BreadItem(db.Model):
    __tablename__ = "bread_item"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable = False)
    price = db.Column(db.Float, nullable = False)
    menus = db.relationship('MenuBreadItem', backref='bread_item')
    
    def __init__(self, name, price):
        self.name = name
        self.price = price