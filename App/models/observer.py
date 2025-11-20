class Observer(ABC):
    @abstractmethod
    def update(self, subject: "Subject") -> None:
        pass