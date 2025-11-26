from App.database import db
from typing import List, Dict, Optional

class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)  
    price = db.Column(db.Float, nullable=False)
    description = db.Column(db.String(255))
      

    def __init__(self, name: str, price: float, description: str = ""):
        self.name = name
        self.price = price
        self.description = description
       

    def get_json(self) -> Dict:
        return {
            'id': self.id,
            'name': self.name,
            'price': self.price,
            'description': self.description,
            'tags': self.tags
        }
    
    def update_price(self, new_price: float) -> None:
        """Update item price with validation"""
        if new_price >= 0:
            self.price = new_price
        else:
            raise ValueError("Price cannot be negative")
    
    def __repr__(self) -> str:
        return f'<Item {self.id}: {self.name} - ${self.price}>'
    
# class Item(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(50), nullable=False)
#     price = db.Column(db.Float, nullable=False)
#     description = db.Column(db.String(255))
#     tags = db.Column(db.JSON)

#     def __init__(self, name, price, description, tags):
#        self.name = name
#        self.price = price
#        self.description = description
#        self.tags = tags

#     def get_json(self):
#        return {
#            'id': self.id,
#            'name': self.name,
#            'price': self.price,
#            'description': self.description,
#            'tags': self.tags
#        }
    