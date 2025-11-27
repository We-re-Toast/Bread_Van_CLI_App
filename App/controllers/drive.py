from App.models import Drive, DriveItem, Item, Driver, Street
from App.models.enums import DriveStatus
from App.database import db
from App.exceptions import ResourceNotFound, ValidationError, DuplicateEntity

# CRUD


from App.controllers.notification import notify_subscribers
from App.utils.validation import validate_date, validate_time
from datetime import datetime


def create_drive(driver_id, area_id, street_id, date, time, status, items=None):
    # Validation
    if not validate_date(str(date)):
        raise ValidationError("Invalid date format")
    if not validate_time(str(time)):
        raise ValidationError("Invalid time format")

    # Convert to objects
    if isinstance(date, str):
        date = datetime.strptime(date, "%Y-%m-%d").date()
    if isinstance(time, str):
        time = datetime.strptime(time, "%H:%M").time()

    new_drive = Drive(
        driver_id=driver_id,
        area_id=area_id,
        street_id=street_id,
        date=date,
        time=time,
        status=status,
    )
    db.session.add(new_drive)
    db.session.commit()

    if items:
        for item in items:
            add_drive_item(new_drive.id, item["item_id"], item["quantity"])

    # Notify subscribers (Observer Pattern)
    notify_subscribers(new_drive)

    return new_drive


def update_drive(drive_id, **kwargs):
    drive = db.session.get(Drive, drive_id)
    if not drive:
        raise ResourceNotFound("Drive not found")

    for key, value in kwargs.items():
        if hasattr(drive, key):
            setattr(drive, key, value)

    db.session.commit()
    return drive


def get_all_drives():
    drives = Drive.query.all()
    return [drive.get_json() for drive in drives]


def delete_drive(drive_id):
    drive = db.session.get(Drive, drive_id)
    if not drive:
        raise ResourceNotFound("Drive not found")

    db.session.delete(drive)
    db.session.commit()


def add_drive_item(drive_id, item_id, quantity):
    drive = db.session.get(Drive, drive_id)
    if not drive:
        raise ResourceNotFound("Drive not found")

    item = db.session.get(Item, item_id)
    if not item:
        raise ResourceNotFound("Item not found")

    drive_item = DriveItem(drive_id=drive_id, item_id=item_id, quantity=quantity)
    db.session.add(drive_item)
    db.session.commit()
    return drive_item


def remove_drive_item(drive_id, item_id):
    drive_item = DriveItem.query.filter_by(drive_id=drive_id, item_id=item_id).first()
    if not drive_item:
        raise ResourceNotFound("Drive item not found")

    db.session.delete(drive_item)
    db.session.commit()
    return True


def get_drive_items(drive_id):
    drive = db.session.get(Drive, drive_id)
    if not drive:
        raise ResourceNotFound("Drive not found")
    return [item.get_json() for item in drive.items]


def schedule_drive(
    driver_id, area_id, street_id, date_str, time_str, status, items=None
):
    driver = Driver.query.get(driver_id)
    street = Street.query.filter_by(id=street_id, area_id=area_id).first()

    if not driver or not street:
        raise ResourceNotFound("Invalid driver or street ID")

    # parse date/time strings into proper types
    try:
        date = datetime.strptime(date_str, "%Y-%m-%d").date()
        time = datetime.strptime(time_str, "%H:%M").time()
    except ValueError:
        raise ValidationError("Invalid date or time format. Use YYYY-MM-DD and HH:MM")

    # prevent scheduling in the past
    scheduled_dt = datetime.combine(date, time)
    if scheduled_dt < datetime.now():
        raise ValidationError("Cannot schedule a drive in the past")

    # prevent duplicate drive for same street/date/time
    existing = Drive.query.filter_by(
        area_id=area_id, street_id=street.id, date=date, time=time
    ).first()
    if existing:
        raise DuplicateEntity(
            f"A drive is already scheduled for {street.name} at {time_str} on {date_str}"
        )
    status = DriveStatus.SCHEDULED

    new_drive = Drive(
        driver_id=driver.id,
        area_id=area_id,
        street_id=street.id,
        date=date,
        time=time,
        status=status,
    )
    db.session.add(new_drive)
    db.session.commit()

    if items:
        for item in items:
            add_drive_item(new_drive.id, item["item_id"], item["quantity"])

    # Notify subscribers (Observer Pattern)
    notify_subscribers(new_drive)

    return new_drive


def view_drives(driver_id):
    existing_driver = Driver.query.get(driver_id)
    if not existing_driver:
        raise ResourceNotFound(f"Driver with ID '{driver_id}' does not exist")
    drives = Drive.query.filter_by(driver_id=driver_id).all()
    return drives


def start_drive(driver_id, drive_id):
    drive = Drive.query.filter_by(driver_id=driver_id, id=drive_id).first()
    if not drive:
        raise ResourceNotFound(f"Drive with ID '{drive_id}' does not exist")
    drive.status = DriveStatus.IN_PROGRESS
    db.session.commit()
    return drive


def complete_drive(driver_id, drive_id):
    drive = Drive.query.filter_by(driver_id=driver_id, id=drive_id).first()
    if not drive:
        raise ResourceNotFound(f"Drive with ID '{drive_id}' does not exist")
    drive.status = DriveStatus.COMPLETED
    db.session.commit()
    return drive

    drive.status = DriveStatus.COMPLETED
    db.session.commit()
    return drive
