from App.database import db

class DriverStock(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  driverId = db.Column(db.Integer, db.ForeignKey('driver.id'), nullable=False)
  itemId = db.Column(db.Integer, db.ForeignKey('item.id'), nullable=False)
  quantity = db.Column(db.Integer, nullable=False)

  driver = db.relationship('Driver', backref='stock')
  item = db.relationship('Item')

  def __init__(self, driverId, itemId, quantity):
     self.driverId = driverId
     self.itemId = itemId
     self.quantity = quantity

  def get_json(self):
     return {
         'stockId': self.id,
         'driverId': self.driverId,
         'itemId': self.itemId,
         'itemName': self.item.name if self.item else None, 
         'quantity': self.quantity
     }