from typing import Final, overload
import os


class PathHelper:
    __MAIN_FILE_NAME: Final[str] = 'main.py'
    __ICONS_PATH: Final[str] = 'icons'
    __FILE_VIEWER_ICONS_DIRECTORY: Final[str] = 'file_viewer'
    __CONTROL_PANEL_ICONS_DIRECTORY: Final[str] = 'control_panel'
    __SYSTEM_ICONS_DIRECTORY: Final[str] = 'system'
    __TOOLBAR_ICONS_DIRECTORY: Final[str] = 'toolbar'
    __SETTINGS_PATH: Final[str] = 'settings'
    __TRANSLATION_PATH: Final[str] = 'settings/translations'
    __ICON_DIRECTORY_FORMAT: Final[str] = '{}x{}'
    __JARS_DIRECTORY: Final[str] = 'framework/jars'
    __DATABASE_FILE_NAME: Final[str] = 'database.db'
    __root_path: str = None

    @classmethod
    def root_path(cls) -> str:
        if cls.__root_path is None:
            cls.__root_path = cls.__find_root_path(os.path.dirname(__file__))
        return cls.__root_path

    @classmethod
    def icons_path(cls) -> str:
        return os.path.join(cls.root_path(), cls.__ICONS_PATH)

    @classmethod
    def settings_path(cls) -> str:
        return os.path.join(cls.root_path(), cls.__SETTINGS_PATH)

    @classmethod
    def translations_path(cls) -> str:
        return os.path.join(cls.root_path(), cls.__TRANSLATION_PATH)

    @classmethod
    def jars_path(cls) -> str:
        return os.path.join(cls.root_path(), cls.__JARS_DIRECTORY)

    @classmethod
    def database_path(cls) -> str:
        return os.path.join(cls.root_path(), cls.__SETTINGS_PATH, cls.__DATABASE_FILE_NAME)

    @classmethod
    def system_icons_path(cls) -> str:
        return os.path.join(cls.root_path(), cls.__ICONS_PATH, cls.__SYSTEM_ICONS_DIRECTORY)

    @classmethod
    def file_viewer_icons_path(cls, icon_size: int | str) -> str:
        if isinstance(icon_size, int):
            icon_size = str(icon_size)
        return os.path.join(cls.icons_path(), cls.__FILE_VIEWER_ICONS_DIRECTORY,
                            cls.__ICON_DIRECTORY_FORMAT.format(icon_size, icon_size))

    @classmethod
    def __find_root_path(cls, path: str) -> str:
        if cls.__MAIN_FILE_NAME in os.listdir(path):
            return path
        return cls.__find_root_path(os.path.dirname(path))

