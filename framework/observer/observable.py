from framework.observer.observer import Observer
from abc import abstractmethod


class Observable:
    def __init__(self) -> None:
        self._observers = []

    def attach(self, observer: Observer) -> None:
        self._observers.append(observer)

    def detach(self, observer: Observer) -> None:
        try:
            self._observers.remove(observer)
        except ValueError:
            pass

    @abstractmethod
    def notify(self, **kwargs) -> None:
        pass
