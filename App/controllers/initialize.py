# App/controllers/initialize.py
from App.database import db
from App.models import Admin, Driver, Resident, Area, Street, DriverStock


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

    stock1 = DriverStock(driverId=1, itemId=1, itemName="Bread", quantity=50)
    stock2 = DriverStock(driverId=2, itemId=2, itemName="Rolls", quantity=20)
    db.session.add_all([stock1, stock2])
    db.session.commit()

    #Creating Drives and Stops
    driver2.schedule_drive(area1.id, street11.id, "2025-10-26", "10:00")
    db.session.commit()

    driver1.schedule_drive(area2.id, street21.id, "2025-10-27", "11:00")
    db.session.commit()
                     
    resident2.request_stop(0)
    db.session.commit()

    # Additional Trinidad & Tobago seed data
    # Add 4 new Areas with 2 streets each
    area4 = Area(name='Port-of-Spain')
    area5 = Area(name='San Fernando')
    area6 = Area(name='Chaguanas')
    area7 = Area(name='Arima')
    db.session.add_all([area4, area5, area6, area7])
    db.session.commit()

    street41 = Street(name='Ariapita Avenue', areaId=area4.id)
    street42 = Street(name='Charlotte Street', areaId=area4.id)
    street51 = Street(name='Cipriani Boulevard', areaId=area5.id)
    street52 = Street(name='Duncan Street', areaId=area5.id)
    street61 = Street(name='Chin Chin Road', areaId=area6.id)
    street62 = Street(name='Mon Repos Road', areaId=area6.id)
    street71 = Street(name='Market Street', areaId=area7.id)
    street72 = Street(name='Sangre Grande Road', areaId=area7.id)
    db.session.add_all([street41, street42, street51, street52, street61, street62, street71, street72])
    db.session.commit()

    # Add 4 new Drivers (do not add new admins)
    driver3 = Driver(username="ken",
                     password="kenpass",
                     status="Available",
                     areaId=area4.id,
                     streetId=street41.id)
    driver4 = Driver(username="nisha",
                     password="nishapass",
                     status="Offline",
                     areaId=area5.id,
                     streetId=street51.id)
    driver5 = Driver(username="omar",
                     password="omarpass",
                     status="Available",
                     areaId=area6.id,
                     streetId=street61.id)
    driver6 = Driver(username="rita",
                     password="ritapass",
                     status="Available",
                     areaId=area7.id,
                     streetId=street71.id)
    db.session.add_all([driver3, driver4, driver5, driver6])
    db.session.commit()

    # Add 4 new Residents
    resident4 = Resident(username="paul",
                         password="paulpass",
                         areaId=area4.id,
                         streetId=street42.id,
                         houseNumber=10)
    resident5 = Resident(username="maria",
                         password="mariapass",
                         areaId=area5.id,
                         streetId=street52.id,
                         houseNumber=22)
    resident6 = Resident(username="trevor",
                         password="trevorpass",
                         areaId=area6.id,
                         streetId=street62.id,
                         houseNumber=5)
    resident7 = Resident(username="anel",
                         password="anelpass",
                         areaId=area7.id,
                         streetId=street72.id,
                         houseNumber=77)
    db.session.add_all([resident4, resident5, resident6, resident7])
    db.session.commit()

    # Add some initial stock for new drivers
    stock3 = DriverStock(driverId=driver3.id, itemId=1, itemName="Bread", quantity=40)
    stock4 = DriverStock(driverId=driver4.id, itemId=2, itemName="Rolls", quantity=25)
    db.session.add_all([stock3, stock4])
    db.session.commit()

    # Schedule drives associated with these new locations (dates within 60 days)
    driver3.schedule_drive(area4.id, street41.id, "2025-12-10", "09:00")
    driver4.schedule_drive(area5.id, street51.id, "2025-12-12", "10:30")
    driver5.schedule_drive(area6.id, street61.id, "2025-12-15", "08:45")
    driver6.schedule_drive(area7.id, street71.id, "2025-12-20", "14:00")
    db.session.commit()
