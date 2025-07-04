from settings.settings import Settings
from framework.logger.logger import Logger
from framework.utils.path_helper import PathHelper
from settings.enums import IconManipulatorID
from settings.icon_manipulators import IconManipulators
from framework.database.database import Database
from database_models.hash import HashModel
import jpype
from wx import xrc
import wx


class AppManager:
    """
    Класс для управления приложением
    """
    __settings: Settings = None
    __logger: Logger = None
    __resources: xrc.XmlResource = None

    @classmethod
    def init(cls) -> None:
        cls.__settings = Settings()
        cls.__logger = Logger(cls.__settings.get_instance().logger_format)

        # подключаем иконки
        icon_size: int = cls.__settings.get_instance().icon_size
        IconManipulators.init_many(manipulator_ids=[IconManipulatorID.FILE_VIEWER,
                                                    IconManipulatorID.CONTROL_PANEL,
                                                    IconManipulatorID.TOOLBAR],
                                   icons_paths=[PathHelper.icons_path() + f'/file_viewer/{icon_size}x{icon_size}',
                                                PathHelper.icons_path() + f'/control_panel/{icon_size}x{icon_size}',
                                                PathHelper.icons_path() + f'/toolbar/{icon_size}x{icon_size}'],
                                   sizes=[icon_size] * 3,
                                   masks=[False] * 3)

    @classmethod
    def settings(cls) -> Settings:
        """
        Получить настройки приложения
        """
        return cls.__settings

    @classmethod
    def logger(cls) -> Logger:
        """
        Получить логгер
        """
        return cls.__logger

    @classmethod
    def resources(cls) -> xrc.XmlResource:
        """
        Получить ресурсы приложения
        """
        return cls.__resources

    @classmethod
    def connect_to_database(cls):
        """
        Установить подключение к БД
        """
        Database.establish_connection(PathHelper.database_path())
        HashModel.connect(Database.connection())

    @classmethod
    def close_connection(cls) -> None:
        Database.disconnect()

    @classmethod
    def start_JVM(cls) -> None:
        """
        Запустить Java Virtual Machine
        """
        jpype.startJVM(classpath=[PathHelper.join(PathHelper.jars_path(), 'HashTest-1.0-SNAPSHOT.jar')])

    @classmethod
    def shutdown_JVM(cls) -> None:
        """
        Выключить Java Virtual Machine
        """
        if jpype.isJVMStarted():
            jpype.shutdownJVM()
