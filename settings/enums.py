from enum import IntEnum, auto


class ToolID(IntEnum):
    FIND_DUPLICATES = 0


class WidgetID(IntEnum):
    MAIN_WINDOW = 0
    LEFT_MAIN_PANEL = auto()
    LEFT_FILE_VIEWER = auto()
    LEFT_CONTROL_PANEL = auto()
    RIGHT_MAIN_PANEL = auto()
    RIGHT_FILE_VIEWER = auto()
    POPUP_MENU = auto()
    RIGHT_CONTROL_PANEL = auto()


class ControlPanelWidgetID(IntEnum):
    pass


class FileViewerIconID(IntEnum):
    BACK_ICON = 0
    FILE_ICON = auto()
    FOLDER_ICON = auto()


class ControlPanelIconID(IntEnum):
    ADD_ICON = 0
    BACK_ARROW = auto()
    DISK_ICON = auto()
    FORWARD_ARROW = auto()


class PopUpItemsID(IntEnum):
    DELETE_BTN = 0
    RENAME_BTN = auto()
    CREATE_BTN = auto()


class IconManipulatorID(IntEnum):
    FILE_VIEWER = 0
    CONTROL_PANEL = auto()
    TOOLBAR = auto()


class CreateItemsID(IntEnum):
    FOLDER = 0
    TEXT_FILE = auto()


class FileViewerColumns(IntEnum):
    NAME = 0
    SIZE = auto()
    CHANGE_DATE = auto()


class SortFlags(IntEnum):
    BY_NAME = 0
    BY_NAME_DESCENDING = auto()
    BY_SIZE = auto()
    BY_SIZE_DESCENDING = auto()
    BY_DATE = auto()
    BY_DATE_DESCENDING = auto()