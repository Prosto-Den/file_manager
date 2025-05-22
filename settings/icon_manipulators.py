from framework.utils.icon_manipulator import IconManipulator as _IconManipulator
from framework.utils.path_helper import PathHelper
from typing import Sequence


class IconManipulators:
    __icon_manipulators = dict()

    @classmethod
    def init(cls, manipulator_id: int, icons_path: str, size: int, mask: bool) -> None:
        """
        Инициализирует один манипулятор, если манипулятор с таким id_ ещё не был инициализирован
        :param manipulator_id: Id манипулятора
        :param icons_path: Путь к иконкам, которыми будет владеть манипулятор
        :param size: Размер иконки (иконки квадратные)
        :param mask: Использовать ли маску для иконок
        """
        if manipulator_id in cls.__icon_manipulators.keys():
            return
        cls.__icon_manipulators[manipulator_id] = _IconManipulator(icons_path=icons_path, size=size, mask=mask)

    @classmethod
    def init_many(cls, manipulator_ids: Sequence[int],
                  icons_paths: Sequence[str],
                  sizes: Sequence[int],
                  masks: Sequence[bool]) -> None:
        """Метод для удобной инициализации нескольких манипуляторов. Также, как и метод init() не инициализирует уже
        инициализированные манипуляторы"""
        for manipulator_id, icon_path, size, mask in zip(manipulator_ids, icons_paths, sizes, masks):
            cls.init(manipulator_id, icon_path, size, mask)

    @classmethod
    def get_icon_manipulator(cls, manipulator_id: int) -> _IconManipulator:
        """
        Получить манипулятор по его ID
        :param manipulator_id: ID манипулятора
        :return: Манипулятор иконок
        """
        return cls.__icon_manipulators[manipulator_id]
