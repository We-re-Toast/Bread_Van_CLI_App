from .Subject import Subject
from App.models.StreetSubscription import StreetSubscription
from App.application.residentObserver import *

class DriveNotifier(Subject):

    def __init__(self):
        super().__init__()
    
    def attach(self, observer):
        super().append(observer)

    def detach(self, observer):
        super().detach(observer)

    def notify(self, drive):

        subscriptions = StreetSubscription.query.filter_by(street_id = drive.streetId)

        for subscription in subscriptions:

            observer = residentObserver(residentId=subscription.resident_id)
            observer.update(drive)