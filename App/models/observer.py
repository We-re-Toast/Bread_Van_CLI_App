from abc import ABC, abstractmethod
from typing import List

class Observer:
    def update(self, drive, menu, eta):
        """Update method - can be overridden by subclasses"""
        pass

class SubjectMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._observers = []

    def attach(self, observer):
        if observer not in self._observers:
            self._observers.append(observer)

    def detach(self, observer):
        if observer in self._observers:
            self._observers.remove(observer)

    def notify(self, drive, menu, eta):
        for observer in self._observers:
            if hasattr(observer, 'update'):
                observer.update(drive, menu, eta)