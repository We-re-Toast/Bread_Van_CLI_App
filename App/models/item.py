from App.database import db


class Item(db.Model):
    __tablename__ = 'item'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    price = db.Column(db.Float, nullable=False)
    description = db.Column(db.String(255))
    tags = db.Column(db.JSON)

    def __init__(self, name, price, description, tags):
       self.name = name
       self.price = price
       self.description = description
       self.tags = tags

    def get_json(self):
       return {
           'id': self.id,
           'name': self.name,
           'price': self.price,
           'description': self.description,
           'tags': self.tags
       }
    