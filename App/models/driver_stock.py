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

   def __init__(self, driverId, itemId, itemName=None, quantity=None):
      """
      Backwards-compatible constructor.

      Supported call styles:
      - DriverStock(driverId, itemId, quantity)               # positional old style
      - DriverStock(driverId=.., itemId=.., quantity=..)       # keyword style
      - DriverStock(driverId, itemId, itemName, quantity)      # new style with itemName
      """
      self.driverId = driverId
      self.itemId = itemId
      # Handle positional old-style call where third arg is quantity
      if quantity is None and isinstance(itemName, int):
         self.itemName = ''
         self.quantity = itemName
      else:
         # Normal case: itemName may be None or a string; quantity may be provided as kw
         self.itemName = itemName or ''
         # If quantity provided, use it; otherwise default to 0 to satisfy non-null column
         self.quantity = quantity if quantity is not None else 0

   def get_json(self):
      data = {
         'id': self.id,
         'driverId': self.driverId,
         'itemId': self.itemId,
         'quantity': self.quantity
      }
      # Only include itemName if it's set to a non-empty value
      if getattr(self, 'itemName', None):
         data['itemName'] = self.itemName
      return data