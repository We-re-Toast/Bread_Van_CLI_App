from App.database import db
from .observer import Subject



class Street(db.Model, Subject):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False, unique=True)
    areaId = db.Column(db.Integer, db.ForeignKey('area.id'), nullable=False)

    def __init__(self, name, areaId):
        db.Model.__init__(self)
        Subject.__init__(self)
        self.name = name
        self.areaId = areaId

    def notify_drive_scheduled(self, drive, driver, menu_items, eta):
        menu_str = ", ".join([f"{item.item.name} (x{item.quantity})" for item in menu_items])
        message = f"SCHEDULED>> Drive {drive.id} by Driver {driver.id} ETA {eta}. Menu: {menu_str}"
        self.notify(message)

    def get_json(self):
        return {
            'id': self.id,
            'name': self.name,
            'areaId': self.areaId
        }
