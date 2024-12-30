from enum import IntEnum


class ToolID(IntEnum):
    FIND_DUPLICATES = 0


class WidgetID(IntEnum):
    MAIN_WINDOW = 0
    LEFT_FILE_VIEWER = 1
    RIGHT_FILE_VIEWER = 2


class IconID(IntEnum):
    FOLDER_ICON = 0
    FILE_ICON = 1


class PopUpItemsID(IntEnum):
    DELETE_BTN = 0