from abc import ABC, abstractmethod
from App.models.observer import Observer

class Subject(ABC):
    
    @abstractmethod
    def attach(self, observer: "Observer") -> None:
        pass

    @abstractmethod
    def detach(self, observer: "Observer") -> None:
        pass

    @abstractmethod
    def notify(self, message : str) -> None:
        pass