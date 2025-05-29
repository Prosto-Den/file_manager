from framework.utils.path_helper import PathHelper
from framework.singleton.singleton import Singleton
import logging
import os


class Logger(metaclass=Singleton):
    def __init__(self, format: str) -> None:
        self.__logger = logging.getLogger()
        self.__format = format

        log_path = os.path.join(PathHelper.root_path(), 'Log', 'log.log')

        if not os.path.exists(parent_dir := os.path.dirname(log_path)):
            os.mkdir(parent_dir)

        self.__logger.setLevel(logging.DEBUG)
        formatter = logging.Formatter(self.__format)

        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(formatter)
        stream_handler.setLevel(logging.DEBUG)

        file_handler = logging.FileHandler(log_path)
        file_handler.setFormatter(formatter)
        file_handler.setLevel(logging.DEBUG)

        self.__logger.addHandler(stream_handler)
        self.__logger.addHandler(file_handler)

    def info(self, message: str) -> None:
        self.__logger.info(message)
