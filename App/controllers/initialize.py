from App.database import db
from App.models import Admin, Item
from App.controllers.resident import create_resident
from App.controllers.driver import create_driver
from App.controllers.area import create_area
from App.controllers.street import create_street
from App.controllers.drive import create_drive, add_drive_item, schedule_drive
from App.controllers.subscription import subscribe_to_street


def initialize():
    db.drop_all()
    db.create_all()

    # Create Admin
    admin = Admin("admin", "adminpass")
    db.session.add(admin)
    db.session.commit()
    print("Admin created: admin/adminpass")

    # Create Area
    area = create_area("Downtown")
    print(f"Area created: {area.name}")

    # Create Streets
    main_st = create_street("Main St", area.id)
    first_ave = create_street("First Ave", area.id)
    print(f"Streets created: {main_st.name}, {first_ave.name}")

    # Create Driver
    driver = create_driver("driver1", "driverpass")
    print(f"Driver created: {driver.username}/driverpass")

    # Create Resident
    resident = create_resident("resident1", "residentpass", area.id, main_st.id, 101)
    print(f"Resident created: {resident.username}/residentpass")

    # Subscribe Resident to Main St
    subscribe_to_street(resident.id, main_st.id)
    print(f"Resident {resident.username} subscribed to {main_st.name}")

    # Schedule a Drive (triggers notification)
    # Note: Date/Time should be strings as per our controller logic which converts them,
    # or objects if we bypass controller. But we use controller `create_drive`.
    # `create_drive` expects strings for validation.
    drive = schedule_drive(
        driver_id=driver.id,
        area_id=area.id,
        street_id=main_st.id,
        date_str="2023-12-25",
        time_str="10:00",
        status="Scheduled",
    )
    print(f"Drive scheduled on {main_st.name} at {drive.time}")

    # Create Items and Add to Drive
    bread = Item(name="Bread", price=2.50, description="Fresh Bread", tags=[])
    croissant = Item(
        name="Croissant", price=1.50, description="Buttery Croissant", tags=[]
    )
    db.session.add(bread)
    db.session.add(croissant)
    db.session.commit()

    add_drive_item(drive.id, bread.id, 5)
    add_drive_item(drive.id, croissant.id, 3)
    print(f"Items added to drive: {bread.name}, {croissant.name}")
