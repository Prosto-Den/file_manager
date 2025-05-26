from framework.utils.json_reader import JsonReader as _JsonReader
from models.translation_model import TranslationModel as _TranslationModel
from models.settings_model import SettingsModel as _SettingsModel
from framework.utils.path_helper import PathHelper as _PathHelper
from framework.utils.file_system import FileSystem as _FileSystem
from framework.singleton.singleton import Singleton as _Singleton
from typing import Final
import os


class Settings(metaclass=_Singleton):
    __SETTINGS_FILE: Final[str] = 'settings.json'
    __translation_model: _TranslationModel = None
    __settings_model: _SettingsModel = None
    __current_language: str = None

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

#TODO когда реализую файл app.py это нужно будет вынести туда
settings = Settings()
