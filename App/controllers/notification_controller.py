from App.models.notification_service import notification_service
from App.models import Resident, Drive

class NotificationController:
    """Controller for notification-related operations"""
    
    @staticmethod
    def notify_street_residents(street_id: int, message: str, data: dict = None):
        """Notify all residents on a street"""
        notification_service.notify(str(street_id), message, data)
    
    @staticmethod
    def subscribe_resident_to_street(resident: Resident):
        """Subscribe a resident to street notifications"""
        notification_service.attach(resident, str(resident.streetId))
    
    @staticmethod
    def unsubscribe_resident_from_street(resident: Resident):
        """Unsubscribe a resident from street notifications"""
        notification_service.detach(resident, str(resident.streetId))
    
    @staticmethod
    def broadcast_drive_schedule(drive: Drive, driver_name: str):
        """Broadcast drive schedule to all residents on the street"""
        message = f"Bread van scheduled by {driver_name} for {drive.date} at {drive.time}"
        data = {
            "drive_id": drive.id,
            "driver_name": driver_name,
            "date": str(drive.date),
            "time": str(drive.time),
            "type": "drive_scheduled"
        }
        notification_service.notify(str(drive.streetId), message, data)