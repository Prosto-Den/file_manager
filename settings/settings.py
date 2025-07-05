from models.translation_model import TranslationModel as _TranslationModel
from framework.utils.json_manip import JsonManip as _JsonManip
from models.settings_model import SettingsModel as _SettingsModel
from framework.utils.path_helper import PathHelper as _PathHelper
from framework.utils.file_system import FileSystem as _FileSystem
from framework.singleton.singleton import Singleton as _Singleton
from framework.utils.classproperty import classproperty
from typing import Final
import os
import platform
from pathlib import Path


#TODO вынести переводы в отдельный класс
class Settings(metaclass=_Singleton):
    __SETTINGS_FILE: Final[str] = 'settings.json'
    __translation_model: _TranslationModel = None
    __settings_model: _SettingsModel = None
    __current_language: str = None

    @classmethod
    def get_instance(cls) -> _SettingsModel:
        if cls.__settings_model is None:
            cls.__settings_model = _JsonManip.read_file_as_model(_PathHelper.join(_PathHelper.settings_path(),
                                                                                       cls.__SETTINGS_FILE), _SettingsModel)
        return cls.__settings_model

    @classmethod
    def current_language_file(cls) -> str:
        if cls.__current_language is None:
            cls.__current_language = '.'.join([cls.get_instance().current_language, 'json'])
        return cls.__current_language

    @classmethod
    def translation(cls) -> _TranslationModel:
        if cls.__translation_model is None:
            cls.__translation_model = _JsonManip.read_file_as_model(_PathHelper.join(_PathHelper.translations_path(),
                                                                                          cls.current_language_file()),
                                                                    _TranslationModel)
        return cls.__translation_model

    @classmethod
    def save_panel_path(cls, left_panel_path: str, right_panel_path: str) -> None:
        cls.get_instance().left_panel_path = left_panel_path
        cls.get_instance().right_panel_path = right_panel_path

    @classproperty
    def left_panel_path(cls) -> str:
        if not cls.get_instance().left_panel_path:
            cls.get_instance().left_panel_path = "C:/" if platform.system() == "Windows" else "/"
        return cls.get_instance().left_panel_path

    @classproperty
    def right_panel_path(cls) -> str:
        if not cls.get_instance().right_panel_path:
            cls.get_instance().right_panel_path = "C:/" if platform.system() == "Windows" else "/"
        return cls.get_instance().right_panel_path

    @classmethod
    def save_settings(cls) -> None:
        _JsonManip.write_file_from_model(_PathHelper.join(_PathHelper.settings_path(), cls.__SETTINGS_FILE),
                                         cls.__settings_model)
