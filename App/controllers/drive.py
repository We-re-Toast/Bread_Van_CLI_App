from App.models import Drive, DriveItem, Item, Driver, Street, StopRequest
from App.models.enums import DriveStatus
from App.database import db
from App.exceptions import ResourceNotFound, ValidationError, DuplicateEntity
from App.controllers.notification import notify_subscribers
from App.utils.validation import validate_date, validate_time
from datetime import datetime


def schedule_drive(
    driver_id, area_id, street_id, date_str, time_str, status, items
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
            add_drive_item(driver_id, new_drive.id, item["item_id"], item["quantity"], notify=False)

    # Format the message
    message = f"Drive ID: {new_drive.id}, Bread Van scheduled for {street.name} on {date_str} at {time_str} with the following items:"
    drive_items = DriveItem.query.filter_by(drive_id=new_drive.id).all()

    for drive_item in drive_items:
        item = drive_item.item
        message += f"\nItem: {item.name} - Quantity: {drive_item.quantity} | Price-Per-Item: ${item.price}"

    # Notify subscribers (Observer Pattern)
    notify_subscribers(new_drive, message)

    return new_drive

def view_drive(driver_id, drive_id):
    drive = Drive.query.filter_by(id=drive_id).first()
    if not drive or drive.driver_id != driver_id:
        raise ResourceNotFound(f"Drive with ID '{drive_id}' does not exist.")
    return drive


def view_drives(driver_id):
    drives = Drive.query.filter_by(driver_id=driver_id).all()
    if not drives:
        raise ResourceNotFound(f"No drives found.")
    return drives


def update_drive(drive_id, **kwargs):
    drive = db.session.get(Drive, drive_id)
    if not drive:
        raise ResourceNotFound("Drive not found")

    for key, value in kwargs.items():
        if hasattr(drive, key):
            setattr(drive, key, value)

    db.session.commit()
    return drive


def delete_drive(drive_id):
    drive = db.session.get(Drive, drive_id)
    if not drive:
        raise ResourceNotFound("Drive not found")

    db.session.delete(drive)
    db.session.commit()


def add_drive_item(driver_id, drive_id, item_id, quantity, notify=True):
    driver = Driver.query.get(driver_id)
    if not driver:
        raise ResourceNotFound("Driver not found")

    drive = Drive.query.filter_by(id=drive_id, driver_id=driver_id).first()
    if not drive:
        raise ResourceNotFound("Drive not found")

    item = Item.query.get(item_id)
    if not item:
        raise ResourceNotFound("Item not found")

    # check if drive item already exists
    drive_item = DriveItem.query.filter_by(drive_id=drive_id, item_id=item_id).first()
    if drive_item:
        raise DuplicateEntity("Drive item already exists")

    drive_item = DriveItem(drive_id=drive_id, item_id=item_id, quantity=quantity)
    db.session.add(drive_item)
    db.session.commit()
    if notify:
        message = f"Menu updated for drive {drive_id} on {drive.date} at {drive.time} in {drive.street.name}. New item available: {item.name} - Quantity: {quantity}"
        notify_subscribers(drive, message)
    return drive_item


def get_drive_items(drive_id):
    drive = Drive.query.get(drive_id)
    if not drive:
        raise ResourceNotFound("Drive not found")
    return drive.items


def remove_drive_item(driver_id, drive_id, item_id, notify=True):
    driver = Driver.query.get(driver_id)
    if not driver:
        raise ResourceNotFound("Driver not found")

    drive = Drive.query.filter_by(id=drive_id, driver_id=driver_id).first()
    if not drive:
        raise ResourceNotFound("Drive not found")

    drive_item = DriveItem.query.filter_by(drive_id=drive_id, item_id=item_id).first()
    if not drive_item:
        raise ResourceNotFound("Drive item not found")

    item_name = drive_item.item.name
    db.session.delete(drive_item)
    db.session.commit()
    if notify:
        message = f"Menu updated for drive {drive_id} on {drive.date} at {drive.time} in {drive.street.name}. Item removed: {item_name}"
        notify_subscribers(drive, message)
    return drive_item


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


def cancel_drive(driver_id, drive_id):
    drive = Drive.query.filter_by(driver_id=driver_id, id=drive_id).first()
    if not drive:
        raise ResourceNotFound(f"Drive with ID '{drive_id}' does not exist")
    drive.status = DriveStatus.CANCELLED
    db.session.commit()
    notify_subscribers(drive, f"Drive {drive_id} on {drive.date} at {drive.time} in {drive.street.name} has been cancelled")
    return drive


def view_stop_requests(driver_id, drive_id):
    drive = Drive.query.filter_by(driver_id=driver_id, id=drive_id).first()
    if not drive:
        raise ResourceNotFound(f"Drive with ID '{drive_id}' does not exist")
    stop_requests = StopRequest.query.filter_by(drive_id=drive.id).all()
    return stop_requests