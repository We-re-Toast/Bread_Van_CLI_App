from abc import ABC, abstractmethod

class Observer:
    def update(self, message):
        """Receive notification from subject"""
        raise NotImplementedError("Observer must implement update()")


class SubjectMixin:
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

