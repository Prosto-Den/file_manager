from models.translation_model import TranslationModel as _TranslationModel
from framework.utils.json_reader import JsonReader as _JsonReader
from models.settings_model import SettingsModel as _SettingsModel
from framework.utils.path_helper import PathHelper as _PathHelper
from framework.utils.file_system import FileSystem as _FileSystem
from framework.singleton.singleton import Singleton as _Singleton
from framework.utils.classproperty import classproperty
from typing import Final
import os
from pathlib import Path




class Translation(metaclass=_Singleton):
    #TODO доделать
    class _Instance:
        pass


#TODO вынести переводы в отдельный класс
class Settings(metaclass=_Singleton):
    __SETTINGS_FILE: Final[str] = 'settings.json'
    __translation_model: _TranslationModel = None
    __settings_model: _SettingsModel = None
    __current_language: str = None
    __left_panel_path: str = None
    __right_panel_path: str = None

    @classmethod
    def get_instance(cls) -> _SettingsModel:
        if cls.__settings_model is None:
            cls.__settings_model = _JsonReader.read_file_as_model(_FileSystem.path_join(_PathHelper.settings_path(),
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
            cls.__translation_model = _JsonReader.read_file_as_model(_FileSystem.path_join(_PathHelper.translations_path(),
                                                                                           cls.current_language_file()),
                                                                     _TranslationModel)
        return cls.__translation_model

    @classproperty
    def left_panel_path(cls) -> str:
        if cls.__left_panel_path is None:
            if os.name == "nt":
                cls.__left_panel_path = "C:/"
            else:
                cls.__left_panel_path = "/"

        return cls.__left_panel_path

    @classproperty
    def right_panel_path(cls) -> str:
        if cls.__right_panel_path is None:
            cls.__right_panel_path = str(Path.home())

        return cls.__right_panel_path

