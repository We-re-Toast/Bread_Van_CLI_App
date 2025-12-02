from App.database import db
from App.models import DriverStock

class Drive(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    driverId = db.Column(db.Integer, db.ForeignKey('driver.id'), nullable=False)
    areaId = db.Column(db.Integer, db.ForeignKey('area.id'), nullable=False)
    streetId = db.Column(db.Integer, db.ForeignKey('street.id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    time = db.Column(db.Time, nullable=False)
    status = db.Column(db.String(20), nullable=False)

    area = db.relationship("Area", backref="drives")
    street = db.relationship("Street", backref="drives")

    def __init__(self, driverId, areaId, streetId, date, time, status):
        self.driverId = driverId
        self.areaId = areaId
        self.streetId = streetId
        self.date = date
        self.time = time
        self.status = status

    def get_json(self):
        return {
            'id': self.id,
            'driverId': self.driverId,
            'areaId': self.areaId,
            'streetId': self.streetId,
            'date': self.date.strftime("%Y-%m-%d") if self.date else None,
            'time': self.time.strftime("%H:%M:%S") if self.time else None,
            'status': self.status
        }

    def set_menu(self):
        stock_items = DriverStock.query.filter_by(driverId=self.driverId).all()
        
        print("\nYour Stock:")
        for item in stock_items:
            print(f"ID: {item.id} Name: {item.name}: {item.quantity} available")
        
        menu = []
        while True:
            print(f"\nCurrent menu: {menu}")
            item_name = input("Enter item id (or '-1' to finish): ")
            if item_name.lower() == '-1':
                break
                
            quantity = input("Enter quantity: ")
            if item_name and quantity:
                menu.append(f"{item_name} x{quantity}")
            else:
                print("Please enter both item name and quantity")
        
        self.menu = ", ".join(menu)
        db.session.commit()
        
        print(f"Final menu: {self.menu}")
        return self.menu