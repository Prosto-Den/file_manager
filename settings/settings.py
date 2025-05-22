from framework.utils.json_reader import JsonReader as _JsonReader
from models.translation_model import TranslationModel as _TranslationModel
from framework.utils.path_helper import PathHelper as _PathHelper
from framework.singleton.singleton import Singleton as _Singleton
from settings.consts import CURRENT_LANGUAGE
import os


class Settings(metaclass=_Singleton):
    __translation_model: _TranslationModel = None
    #TODO вынести настройки в json файл, создать модель

    @classmethod
    def translation(cls) -> _TranslationModel:
        if cls.__translation_model is None:
            cls.__translation_model = _JsonReader.read_file_as_model(os.path.join(_PathHelper.translations_path(),
                                                                                 CURRENT_LANGUAGE), _TranslationModel)
        return cls.__translation_model
