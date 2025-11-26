from App.database import db

def resident_create(username, password, area_id, street_id, house_number):
    from App.models import Resident
    resident = Resident(username=username, password=password, areaId=area_id, streetId=street_id, houseNumber=house_number)
    db.session.add(resident)
    db.session.commit()
    return resident

def resident_subscribe_to_drive(resident, drive_id):
    from App.models import Drive
    drive = Drive.query.get(drive_id)
    if not drive:
        raise ValueError("Drive not found.")
    
    # Auto-subscribe residents to drives in their area and street
    if drive.areaId == resident.areaId and drive.streetId == resident.streetId:
        resident.subscribe_to_drive(drive_id)
        return True
    else:
        raise ValueError("Cannot subscribe to drives outside your area and street.")

def resident_unsubscribe_from_drive(resident, drive_id):
    resident.unsubscribe_from_drive(drive_id)
    return True

def resident_get_subscribed_drives(resident):
    from App.models import Drive
    return Drive.query.filter(Drive.id.in_(resident.subscribed_drives)).all()

def resident_request_stop(resident, drive_id):
    from App.models import Drive, Stop
    drives = Drive.query.filter_by(areaId=resident.areaId, streetId=resident.streetId, status="Upcoming").all()
    if not any(d.id == drive_id for d in drives):
        raise ValueError("Invalid drive choice.")
    existing_stop = Stop.query.filter_by(driveId=drive_id, residentId=resident.id).first()
    if existing_stop:
        raise ValueError(f"You have already requested a stop for drive {drive_id}.")
    return resident.request_stop(drive_id)

def resident_request_stop_from_notification(resident, drive_id):
    """Request a stop after receiving a notification about a drive"""
    from App.models import Drive, Stop
    # Verify the drive exists and is upcoming
    drive = Drive.query.get(drive_id)
    if not drive:
        raise ValueError("Drive not found.")
    
    if drive.status != "Upcoming":
        raise ValueError("Cannot request stops for completed or cancelled drives.")
    
    # Check if resident is in the correct area/street
    if drive.areaId != resident.areaId or drive.streetId != resident.streetId:
        raise ValueError("Cannot request stops for drives outside your area.")
    
    # Check if stop already exists
    existing_stop = Stop.query.filter_by(driveId=drive_id, residentId=resident.id).first()
    if existing_stop:
        raise ValueError("You have already requested a stop for this drive.")
    
    # Create the stop
    stop = resident.request_stop(drive_id)
    return stop

def resident_cancel_stop(resident, drive_id):
    from App.models import Stop
    stop = Stop.query.filter_by(driveId=drive_id, residentId=resident.id).first()
    if not stop:
        raise ValueError("No stop requested for this drive.")
    resident.cancel_stop(stop.id)
    return stop

def resident_view_inbox(resident):
    return resident.view_inbox()

def resident_get_notifications(resident, unread_only=False):
    """Get resident's notifications"""
    return resident.view_inbox(unread_only=unread_only)

def resident_get_notification_stats(resident):
    """Get notification statistics"""
    inbox = resident.view_inbox()
    unread_count = resident.get_unread_count()
    total_count = len(inbox)
    
    return {
        'total_notifications': total_count,
        'unread_notifications': unread_count,
        'notification_preferences': getattr(resident, 'notification_preferences', [])
    }

def resident_mark_notification_read(resident, notification_index):
    """Mark a specific notification as read"""
    resident.mark_notification_read(notification_index)
    return True

def resident_mark_all_notifications_read(resident):
    """Mark all notifications as read"""
    resident.mark_all_notifications_read()
    return True

def resident_clear_notifications(resident):
    """Clear all notifications"""
    resident.clear_inbox()
    return True

def resident_update_notification_preferences(resident, preferences):
    """Update notification preferences"""
    resident.update_notification_preferences(preferences)
    return resident

def resident_view_driver_stats(resident, driver_id):
    driver = resident.view_driver_stats(driver_id)
    if not driver:
        raise ValueError("Driver not found.")
    return driver

def resident_view_stock(resident, driver_id):
    driver = resident.view_driver_stats(driver_id)
    if not driver:
         raise ValueError("Driver not found.")
    from App.models import DriverStock
    stocks = DriverStock.query.filter_by(driverId=driver_id).all()
    return stocks
