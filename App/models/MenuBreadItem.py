from App.database import db

class MenuBreadItem(db.Model):
    __tablename__ = 'menu_bread_item'
    menu_id = db.Column(db.Integer, db.ForeignKey('menu.id'), primary_key=True)
    bread_id = db.Column(db.Integer, db.ForeignKey('bread_item.id'), primary_key=True)
    
    def __init__(self, menu_id, bread_id):
        self.menu_id = menu_id
        self.bread_id = bread_id