from abc import ABC, abstractmethod

class Observer(ABC):
    @abstractmethod
    def update(self, message):
        """Receive notification from subject"""
        pass

class Subject(ABC):
    def __init__(self):
        self._observers = []

    def attach(self, observer):
        if observer not in self._observers:
            self._observers.append(observer)

    def detach(self, observer):
        try:
            self._observers.remove(observer)
        except ValueError:
            pass

    def notify(self, message):
        for observer in self._observers:
            observer.update(message)
