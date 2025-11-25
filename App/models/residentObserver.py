from .observer import Observer
from .drive import Drive

class residentObserver(Observer):


    def __init__(self, name):
        self.name = name

    def update(self, drive):
        drive = Drive.query.get(drive.id)
        message = f'Alert: Drive {drive.id} would be coming to your area {drive.areaId} on {drive.date} at {drive.time}.'
        
        return message
