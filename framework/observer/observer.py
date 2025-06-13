from abc import abstractmethod

class Observer:
    """
    Класс наблюдатель. Следит за изменениями класса Observable
    """
    @abstractmethod
    def update(self, **kwargs) -> None:
        """
        Выполнить необходимые обновления
        :param kwargs: Необходимые аргументы
        """
        pass
