from .Subject import Subject
from models.StreetSubscription import StreetSubscription

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

            observer = ResidentObserver(subscription.residet_id)
            observer.update(drive)