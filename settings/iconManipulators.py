from framework.iconManipulator import IconManipulator as _IconManipulator
from .enums import IconManipulatorID
from framework.exceptions import InitException as _InitException


class IconManipulators:
    __file_viewer_icons_manipulator: _IconManipulator = None
    __control_panel_icons_manipulator: _IconManipulator = None
    __toolbar_icons_manipulator: _IconManipulator = None

    @classmethod
    def init(cls, *, file_viewer_icons: str, control_panel_icons: str, toolbar_icons: str, size: int, mask: bool) -> None:
        cls.init_file_viewer_manipulator(file_viewer_icons, size, mask)
        cls.init_control_panel_manipulator(control_panel_icons, size, mask)
        cls.init_toolbar_manipulator(toolbar_icons, size, mask)

    @classmethod
    def init_file_viewer_manipulator(cls, filepath: str, size: int, mask: bool) -> None:
        if cls.__file_viewer_icons_manipulator is None:
            cls.__file_viewer_icons_manipulator = _IconManipulator(icons_path=filepath, size=size, mask=mask)

    @classmethod
    def init_control_panel_manipulator(cls, filepath: str, size: int, mask: bool) -> None:
        if cls.__control_panel_icons_manipulator is None:
            cls.__control_panel_icons_manipulator = _IconManipulator(icons_path=filepath, size=size, mask=mask)

    @classmethod
    def init_toolbar_manipulator(cls, filepath: str, size: int, mask: bool) -> None:
        if cls.__toolbar_icons_manipulator is None:
            cls.__toolbar_icons_manipulator = _IconManipulator(icons_path=filepath, size=size, mask=mask)

    @classmethod
    def get_icon_manipulator(cls, manipulator_id: int) -> _IconManipulator:
        match manipulator_id:
            case IconManipulatorID.FILE_VIEWER:
                if cls.__file_viewer_icons_manipulator is not None:
                    return cls.__file_viewer_icons_manipulator
                raise _InitException(cls.__file_viewer_icons_manipulator)
            case IconManipulatorID.CONTROL_PANEL:
                if cls.__control_panel_icons_manipulator is not None:
                    return cls.__control_panel_icons_manipulator
                raise _InitException(cls.__control_panel_icons_manipulator)
            case IconManipulatorID.TOOLBAR:
                if cls.__toolbar_icons_manipulator is not None:
                    return cls.__toolbar_icons_manipulator
                raise _InitException(cls.__toolbar_icons_manipulator)
            case _:
                raise ValueError('Не допустимый ID манипулятора!')