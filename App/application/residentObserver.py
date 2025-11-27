from App.database import db
from .observer import Observer
from App.models.drive import Drive
from App.models.resident import Resident
from App.models.Notification import Notification

class residentObserver(Observer):


    def __init__(self, residentId):
        self.residentId = residentId

    def update(self, drive):
        resident = Resident.query.get(self.residentId)
        message = f'Alert: Drive {drive.id} would be coming to you on {drive.street.name}, {drive.street.area.name} on {drive.date} at {drive.time}.'
        message += f'\nMENU: {drive.menu.name}'
        new_notification = Notification(message, self.residentId, drive.id)
        db.session.add(new_notification)
        db.session.commit()
        return new_notification
