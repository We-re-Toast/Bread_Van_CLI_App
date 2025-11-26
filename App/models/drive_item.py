from App.database import db


class DriveItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    quantity = db.Column(db.Integer, nullable=False)

    """Foreign Keys"""
    drive_id = db.Column(db.Integer, db.ForeignKey("drive.id"), nullable=False)
    item_id = db.Column(db.Integer, db.ForeignKey("item.id"), nullable=False)

    """Relationships"""
    item = db.relationship("Item", backref="drive_items", lazy=True)

    def __init__(self, drive_id, item_id, quantity):
        self.drive_id = drive_id
        self.item_id = item_id
        self.quantity = quantity

    def __repr__(self):
        return f"ID: {self.id} | Drive ID: {self.drive_id} | Item ID: {self.item_id} | Quantity: {self.quantity}"

    def get_json(self):
        return {
            "id": self.id,
            "drive_id": self.drive_id,
            "item_id": self.item_id,
            "item_name": self.item.name,
            "quantity": self.quantity,
        }
