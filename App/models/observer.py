from typing import Dict, Any

class Subject:
    
    def attach(self, observer, key: str) -> None:
        """Attach an observer to a specific key (street_id)"""
        raise NotImplementedError("Subclasses must implement attach method")
    
    def detach(self, observer, key: str) -> None:
        """Detach an observer from a specific key (street_id)"""
        raise NotImplementedError("Subclasses must implement detach method")
    
    def notify(self, key: str, message: str, data: Dict[str, Any] = None) -> None:
        """Notify all observers of a specific key (street_id)"""
        raise NotImplementedError("Subclasses must implement notify method")

class Observer:
    
    def update(self, message: str, data: Dict[str, Any] = None) -> None:
        """Handle incoming notifications"""
        raise NotImplementedError("Subclasses must implement update method")