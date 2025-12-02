# App/models/driver_stock.py
from App.database import db

class DriverStock(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  driverId = db.Column(db.Integer, db.ForeignKey('driver.id'), nullable=False)
  itemName = db.Column(db.String(100), nullable=False)
  itemId = db.Column(db.Integer, db.ForeignKey('item.id'), nullable=False)
  quantity = db.Column(db.Integer, nullable=False)

  driver = db.relationship('Driver', backref='stock')
  item = db.relationship('Item')

  def __init__(self, driverId, itemId,itemName, quantity):
     self.driverId = driverId
     self.itemId = itemId
     self.itemName = itemName
     self.quantity = quantity

  def get_json(self):
     return {
         'id': self.id,
         'driverId': self.driverId,
         'itemId': self.itemId,
         'itemName': self.itemName,
         'quantity': self.quantity
     }