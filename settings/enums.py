from enum import IntEnum, StrEnum, auto


class ToolID(IntEnum):
    FIND_DUPLICATES = 0


class WindowID(IntEnum):
    MAIN_WINDOW = 0
    DUPLICATE_WINDOW = auto()


class WidgetID(IntEnum):
    LEFT_MAIN_PANEL = 0
    RIGHT_MAIN_PANEL = auto()
    FILE_VIEWER = auto()
    CONTROL_PANEL = auto()
    POPUP_MENU = auto()


class ControlPanelWidgetID(IntEnum):
    pass


class FileViewerIconID(IntEnum):
    BACK_ICON = 0
    FILE_ICON = auto()
    FOLDER_ICON = auto()
    TEXT_FILE_ICON = auto()
    WORD_FILE_ICON = auto()


class ControlPanelIconID(IntEnum):
    ADD_ICON = 0
    BACK_ARROW = auto()
    DISK_ICON = auto()
    FORWARD_ARROW = auto()
    INSERT_ICON = auto()


class PopUpItemsID(IntEnum):
    DELETE_BTN = 0
    RENAME_BTN = auto()
    MOVE_INTO_BTN = auto()
    COPY_INTO_BTN = auto()
    COPY_BTN = auto()


class IconManipulatorID(IntEnum):
    FILE_VIEWER = 0
    CONTROL_PANEL = auto()
    TOOLBAR = auto()
    SYSTEM = auto()


class CreateItemsID(IntEnum):
    FOLDER = 0
    TEXT_FILE = auto()
    DOCX_FILE = auto()


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


class FileFormatID(StrEnum):
    TXT = '.txt'
    DOCX = '.docx'