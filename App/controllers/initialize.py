from App.database import db
from App.models import Admin, Driver, Resident, Area, Street, Item, Notification
from App.controllers.driver import driver_schedule_drive
from App.models.driver_stock import DriverStock


def initialize():
    db.drop_all()
    db.create_all()

    #Creating Admin
    admin = Admin(username="admin", password="adminpass")
    db.session.add(admin)
    db.session.commit()

    #Creating Areas and Streets
    area1 = Area(name='St. Augustine')
    db.session.add(area1)
    db.session.commit()

    street11 = Street(name="Gordon Street", areaId=area1.id)
    street12 = Street(name="Warner Street", areaId=area1.id)
    street13 = Street(name="College Road", areaId=area1.id)
    db.session.add_all([street11, street12, street13])
    db.session.commit()

    area2 = Area(name='Tunapuna')
    db.session.add(area2)
    db.session.commit()

    street21 = Street(name="Fairly Street", areaId=area2.id)
    street22 = Street(name="Saint John Road", areaId=area2.id)
    db.session.add_all([street21, street22])
    db.session.commit()

    area3 = Area(name='San Juan')
    db.session.add(area3)
    db.session.commit()

    #Creating Drivers
    driver1 = Driver(username="bob",
                     password="bobpass",
                     status="Offline",
                     areaId=area1.id,
                     streetId=street11.id)
    driver2 = Driver(username="mary",
                     password="marypass",
                     status="Available",
                     areaId=area2.id,
                     streetId=None)
    db.session.add_all([driver1, driver2])
    db.session.commit()

    #Creating Residents and Stops
    resident1 = Resident(username="alice",
                         password="alicepass",
                         areaId=area1.id,
                         streetId=street12.id,
                         houseNumber=48)
    resident2 = Resident(username="jane",
                         password="janepass",
                         areaId=area1.id,
                         streetId=street12.id,
                         houseNumber=50)
    resident3 = Resident(username="john",
                         password="johnpass",
                         areaId=area2.id,
                         streetId=street21.id,
                         houseNumber=13)
    db.session.add_all([resident1, resident2, resident3])
    db.session.commit()

    #Create Menu Items
    item1 = Item(name = "Bread Loaf", price = 12.50, description = "Freshly baked bread loaf.", tags = ["bread"])
    item2 = Item(name = "Croissant", price = 8.00, description = "Buttery croissant.", tags = ["pastry"])
    item3 = Item(name = "Muffin", price = 6.00, description = "Blueberry muffin.", tags = ["pastry"])
    item4 = Item(name = "Baguette", price = 10.00, description = "Crispy French baguette.", tags = ["bread"])
    item5 = Item(name = "Donut", price = 7.00, description = "Glazed donut.", tags = ["sweet" , "pastry"])
    item6 = Item(name = "Bagel", price = 5.00, description = "Fresh bagel.", tags = ["bread"])
    item7 = Item(name = "Sourdough Bread", price = 15.00, description = "Tangy sourdough bread.", tags = ["bread"])
    item8 = Item(name = "Cinnamon Roll", price = 6.00, description = "Sweet cinnamon roll.", tags = ["sweet" , "pastry"])
    item9 = Item(name = "Cheese Danish", price = 5.00, description = "Cream cheese danish.", tags = ["pastry"])
    db.session.add_all([item1, item2, item3, item4, item5, item6, item7, item8, item9])
    db.session.commit()

    # Add stock for drivers
    stock1 = DriverStock(driverId=driver1.id, itemId=item1.id, quantity=20)
    stock2 = DriverStock(driverId=driver1.id, itemId=item3.id, quantity=10)
    stock3 = DriverStock(driverId=driver2.id, itemId=item2.id, quantity=15)
    stock4 = DriverStock(driverId=driver2.id, itemId=item4.id, quantity=5)
    db.session.add_all([stock1, stock2, stock3, stock4])
    db.session.commit()
    

    #Creating Drives and Stops
    driver_schedule_drive(driver2, area1.id, street12.id, "2025-12-27", "11:00") 

    db.session.commit()
                     
    resident2.request_stop(0)
    db.session.commit()
