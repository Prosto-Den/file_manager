from settings.settings import Settings as _Settings
from framework.logger.logger import Logger as _Logger
from framework.utils.path_helper import PathHelper
from settings.enums import IconManipulatorID
from settings.icon_manipulators import IconManipulators
from framework.database.database import Database
from framework.utils.classproperty import classproperty
from typing_extensions import deprecated
from database_models.hash import HashModel
import jpype
from wx import xrc


class AppManager:
    """
    Класс для управления приложением
    """
    Settings: _Settings = None
    Logger: _Logger = None
    __resources: xrc.XmlResource = None

    @classmethod
    def init(cls) -> None:
        cls.Settings = _Settings()
        cls.Logger = _Logger(cls.Settings.get_instance().logger_format)

        # подключаем иконки
        icon_size: int = cls.Settings.get_instance().icon_size
        IconManipulators.init_many(manipulator_ids=[IconManipulatorID.FILE_VIEWER,
                                                    IconManipulatorID.CONTROL_PANEL,
                                                    IconManipulatorID.TOOLBAR],
                                   icons_paths=[PathHelper.icons_path() + f'/file_viewer/{icon_size}x{icon_size}',
                                                PathHelper.icons_path() + f'/control_panel/{icon_size}x{icon_size}',
                                                PathHelper.icons_path() + f'/toolbar/{icon_size}x{icon_size}'],
                                   sizes=[icon_size] * 3,
                                   masks=[False] * 3)

    @classmethod
    @deprecated("Use Settings instead", stacklevel=2)
    def settings(cls) -> _Settings:
        """
        Получить настройки приложения
        """
        return cls.Settings

    @classmethod
    @deprecated("Use Logger instead", stacklevel=2)
    def logger(cls) -> _Logger:
        """
        Получить логгер
        """
        return cls.Logger

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
