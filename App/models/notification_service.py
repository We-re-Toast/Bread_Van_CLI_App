from typing import Dict, List, Any
from App.database import db

class NotificationService:
    """Service that manages observer subscriptions and notifications"""
    
    _instance = None
    _observers: Dict[str, List] = {}  # street_id -> list of resident observers
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(NotificationService, cls).__new__(cls)
            cls._observers = {}
        return cls._instance
    
    def attach(self, observer, street_id: str) -> None:
        if street_id not in self._observers:
            self._observers[street_id] = []
        
        if observer not in self._observers[street_id]:
            self._observers[street_id].append(observer)
    
    def detach(self, observer, street_id: str) -> None:
        if street_id in self._observers:
            if observer in self._observers[street_id]:
                self._observers[street_id].remove(observer)
    
    def notify(self, street_id: str, message: str, data: Dict[str, Any] = None) -> None:
        if street_id in self._observers:
            for observer in self._observers[street_id]:
                # Call the update method on the resident
                observer.update(message, data)
    
    def subscribe_resident_to_street(self, resident) -> None:
        self.attach(resident, str(resident.streetId))
    
    def unsubscribe_resident_from_street(self, resident) -> None:
        self.detach(resident, str(resident.streetId))

# Global notification service instance
notification_service = NotificationService()