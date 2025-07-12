from models.translation_model import TranslationModel as _TranslationModel
from framework.utils.json_manip import JsonManip as _JsonManip
from models.settings_model import SettingsModel as _SettingsModel
from framework.utils.path_helper import PathHelper as _PathHelper
from framework.singleton.singleton import Singleton as _Singleton
from framework.utils.classproperty import classproperty
from typing_extensions import deprecated
from typing import Final
import platform


class Translation:
    class _TranslationInstance:
        __TRANSLATION_FILENAME: Final[str] = ''


#TODO вынести переводы в отдельный класс
class Settings(metaclass=_Singleton):
    class _SettingsInstance:
        #TODO возможно стоит создать модель с именами всех файлов программы
        __SETTINGS_FILENAME: Final[str] = 'settings.json'

        def __init__(self) -> None:
            self.__model = _JsonManip.read_file_as_model(_PathHelper.join(_PathHelper.settings_path(),
                                                                          self.__SETTINGS_FILENAME), _SettingsModel)

        @property
        def buffer_size(self) -> int:
            return self.__model.buffer_size

        @buffer_size.setter
        def buffer_size(self, value: int) -> None:
            self.__model.buffer_size = value

        @property
        def current_language(self) -> str:
            return self.__model.current_language

        @current_language.setter
        def current_language(self, value: str) -> None:
            self.__model.current_language = value

        @property
        def time_format(self) -> str:
            return self.__model.time_format

        @property
        def logger_format(self) -> str:
            return self.__model.logger_format

        @property
        def icon_size(self) -> int:
            return self.__model.icon_size

        #TODO это на будущее
        #@icon_size.setter
        #def icon_size(self, value: int) -> None:
        #    self.__model.icon_size = value

        @property
        def left_panel_path(self) -> str:
            return self.__model.left_panel_path

        @left_panel_path.setter
        def left_panel_path(self, value: str) -> None:
            self.__model.left_panel_path = value

        @property
        def right_panel_path(self) -> str:
            return self.__model.right_panel_path

        @right_panel_path.setter
        def right_panel_path(self, value: str) -> None:
            self.__model.right_panel_path = value

        def save_settings(self) -> None:
            _JsonManip.write_file_from_model(_PathHelper.join(_PathHelper.settings_path(),
                                                              self.__SETTINGS_FILENAME), self.__model)

    Instance = _SettingsInstance()
    __translation_model: _TranslationModel = None #TODO удалить после удаления метода translation()

    @classmethod
    def __current_language_file(cls) -> str:
        return '.'.join([cls.Instance.current_language, 'json'])

    @classmethod
    @deprecated("Use Translation from AppManager instead", stacklevel=2)
    def translation(cls) -> _TranslationModel:
        if cls.__translation_model is None:
            cls.__translation_model = _JsonManip.read_file_as_model(_PathHelper.join(_PathHelper.translations_path(),
                                                                                     cls.__current_language_file()),
                                                                    _TranslationModel)
        return cls.__translation_model

    @classmethod
    def save_panel_path(cls, left_panel_path: str, right_panel_path: str) -> None:
        cls.Instance.left_panel_path = left_panel_path
        cls.Instance.right_panel_path = right_panel_path


    @classproperty
    def left_panel_path(cls) -> str:
        # при первом запуске программы в этом поле будет пусто, поэтому выставляем в качестве пути корень
        if not cls.Instance.left_panel_path:
            cls.Instance.left_panel_path = "C:/" if platform.system() == "Windows" else "/"
        return cls.Instance.left_panel_path

    @classproperty
    def right_panel_path(cls) -> str:
        # при первом запуске программы в этом поле будет пусто, поэтому выставляем в качестве пути корень
        if not cls.Instance.right_panel_path:
            cls.Instance.right_panel_path = "C:/" if platform.system() == "Windows" else "/"
        return cls.Instance.right_panel_path
