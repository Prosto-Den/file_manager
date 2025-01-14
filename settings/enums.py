from enum import IntEnum, auto


class ToolID(IntEnum):
    FIND_DUPLICATES = 0


class WidgetID(IntEnum):
    MAIN_WINDOW = 0
    LEFT_FILE_VIEWER = auto()
    RIGHT_FILE_VIEWER = auto()
    POPUP_MENU = auto()


class FileViewerIconID(IntEnum):
    FILE_ICON = 0
    FOLDER_ICON = auto()


class ControlPanelIconID(IntEnum):
    ADD_ICON = 0
    DISK_ICON = auto()


class PopUpItemsID(IntEnum):
    DELETE_BTN = 0
    RENAME_BTN = auto()
    #CREATE_BTN = 2


class IconManipulatorID(IntEnum):
    FILE_VIEWER = 0
    CONTROL_PANEL = auto()
    TOOLBAR = auto()