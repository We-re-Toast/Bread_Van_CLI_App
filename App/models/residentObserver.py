from .observer import Observer
from .drive import Drive
from .resident import Resident

class residentObserver(Observer):


    def __init__(self, name, residentId):
        self.name = name
        self.residentId = residentId

    def update(self, drive):
        drive = Drive.query.get(drive.id)
        resident = Resident.query.get(self.residentId)
        message = f'Alert: Drive {drive.id} would be coming to your area {drive.areaId} on {drive.date} at {drive.time}.'
        resident.receive_notif(message)
        return 
