from framework.observer.observer import Observer
from abc import abstractmethod


class Observable:
    """
    Наблюдаемый класс. Нужен для сообщения наблюдателям об изменениях
    """
    def __init__(self) -> None:
        self._observers = []

    def attach(self, observer: Observer) -> None:
        """
        Добавить наблюдателя
        :param observer: Класс наблюдатель
        """
        self._observers.append(observer)

    def detach(self, observer: Observer) -> None:
        """
        Отписать наблюдателя от обновлений
        :param observer: Наблюдатель, привязанный к классу
        """
        try:
            self._observers.remove(observer)
        except ValueError:
            pass

    @abstractmethod
    def notify(self, **kwargs) -> None:
        """
        Уведомить наблюдателей об изменении. Абстрактный класс
        :param kwargs: Аргументы, необходимые для наблюдателей
        """
        pass
