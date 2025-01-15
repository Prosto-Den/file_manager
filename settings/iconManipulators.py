from framework.iconManipulator import IconManipulator as _IconManipulator


class IconManipulators:
    __icon_manipulators = dict()

    @classmethod
    def init_manipulator(cls, manipulator_id: int, icons_path: str, size: int, mask: bool) -> None:
        if manipulator_id in cls.__icon_manipulators.keys():
            return
        cls.__icon_manipulators[manipulator_id] = _IconManipulator(icons_path=icons_path, size=size, mask=mask)


    @classmethod
    def get_icon_manipulator(cls, manipulator_id: int) -> _IconManipulator:
        if manipulator_id in cls.__icon_manipulators.keys():
            return cls.__icon_manipulators[manipulator_id]
        raise ValueError('Манипулятор с таким ID не найден')
