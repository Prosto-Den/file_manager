from framework.utils.json_reader import JsonReader as _JsonReader
from models.translation_model import TranslationModel as _TranslationModel
from models.settings_model import SettingsModel as _SettingsModel
from framework.utils.path_helper import PathHelper as _PathHelper
from framework.utils.file_system import FileSystem as _FileSystem
from framework.singleton.singleton import Singleton as _Singleton
from typing import Final
import os
from pathlib import Path


class ClassProperty:
    """
    поскольку в питоне класс проперти начиная с версии 3.11 считаются deprecated,
    вот кастомный класспроперти, по сути использование как с обычными @property,
    чтобы это управление полями класса Settings было более pythonic way (вайя)
    """
    def __init__(self, fget=None, fset=None):
        self.__fget = fget
        self.__fset = fset

    def __get__(self, instance, owner):
        if not self.__fget:
            raise AttributeError("can't get attribute")
        return self.__fget(owner)

    def __set__(self, instance, value):
        if not self.__fset:
            raise AttributeError("can't set attribute")
        return self.__fset(type(instance) if instance else instance, value)

    def setter(self, fset):
        self.__fset = fset
        return self

def classproperty(func):
    return ClassProperty(fget=func)


class Settings(metaclass=_Singleton):
    __SETTINGS_FILE: Final[str] = 'settings.json'
    __translation_model: _TranslationModel | None = None
    __settings_model: _SettingsModel | None = None
    __current_language: str | None = None
    __left_panel_path: str | None = None
    __right_panel_path: str | None = None

    #TODO вынести настройки в json файл, создать модель
    @classmethod
    def settings(cls) -> _SettingsModel:
        if cls.__settings_model is None:
            cls.__settings_model = _JsonReader.read_file_as_model(_FileSystem.path_join(_PathHelper.settings_path(),
                                                                               cls.__SETTINGS_FILE), _SettingsModel)
        return cls.__settings_model

    @classmethod
    def current_language(cls) -> str:
        if cls.__current_language is None:
            cls.__current_language = '.'.join([cls.settings().current_language, 'json'])
        return cls.__current_language

    @classmethod
    def translation(cls) -> _TranslationModel:
        if cls.__translation_model is None:
            cls.__translation_model = _JsonReader.read_file_as_model(_FileSystem.path_join(_PathHelper.translations_path(),
                                                                                 cls.current_language()),
                                                                                 _TranslationModel)
        return cls.__translation_model

    @classproperty
    def left_panel_path(cls) -> str:
        if cls.__left_panel_path is None:
            if os.name == "nt":
                cls.__left_panel_path = "C:"
            else:
                cls.__left_panel_path = "/"

        return cls.__left_panel_path

    @classproperty
    def right_panel_path(cls) -> str:
        if cls.__right_panel_path is None:
            cls.__right_panel_path = str(Path.home())

        return cls.__right_panel_path


#TODO когда реализую файл app.py это нужно будет вынести туда
settings = Settings()
