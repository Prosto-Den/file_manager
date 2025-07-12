from models.translation_model import TranslationModel
from framework.utils.path_helper import PathHelper
from framework.utils.json_manip import JsonManip


class TranslationUtil:
    @staticmethod
    def get_translation_model(language_code: str) -> TranslationModel:
        filename = '.'.join([language_code, 'json'])
        path = PathHelper.join(PathHelper.translations_path(), filename)
        return JsonManip.read_file_as_model(path, TranslationModel)
