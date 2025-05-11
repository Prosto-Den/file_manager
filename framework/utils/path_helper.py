from typing import Final
import os


class PathHelper:
    __MAIN_FILE_NAME: Final[str] = 'main.py'
    __ICONS_PATH: Final[str] = 'icons'
    __TRANSLATION_PATH: Final[str] = 'settings/translations'
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
    def translations_path(cls) -> str:
        return os.path.join(cls.root_path(), cls.__TRANSLATION_PATH)

    #TODO придумать, как получать размер иконок
    @classmethod
    def file_viewer_icons_path(cls) -> str:
        pass

    @classmethod
    def __find_root_path(cls, path: str) -> str:
        if cls.__MAIN_FILE_NAME in os.listdir(path):
            return path
        return cls.__find_root_path(os.path.dirname(path))

