from abc import ABC, abstractmethod 

class Subject(ABC):

    def __init__(self):
        self._observers = []
    
    def attach(self, observer):
        self._observers.append(observer)

    def detach(self, observer):
        self._observers.remove(observer)

    @abstractmethod
    def notify(self, drive):
        pass