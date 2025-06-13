from windows.main_window import MainWindow
from settings.enums import WindowID, IconManipulatorID
from settings.consts import ICON_SIZE
from settings.settings import settings
from settings.icon_manipulators import IconManipulators
from framework.utils.path_helper import PathHelper
from framework.utils.file_system import FileSystem
from framework.database.database import Database
from database_models.hash import HashModel
import multiprocessing as mp
import jpype
import wx
import os


if __name__ == '__main__':
    mp.set_start_method('spawn')
    # приложение
    wx.DisableAsserts()
    app = wx.App()
    jpype.startJVM(classpath=[FileSystem.path_join(PathHelper.jars_path(), 'HashTest-1.0-SNAPSHOT.jar')])
    #TODO чёт много методов, может быть сделаю попроще
    Database.establish_connection(PathHelper.database_path())
    HashModel.connect(Database.connection())
    HashModel.create()

    # подключаем иконки
    IconManipulators.init_many(manipulator_ids=[IconManipulatorID.FILE_VIEWER,
                                                IconManipulatorID.CONTROL_PANEL,
                                                IconManipulatorID.TOOLBAR],
                               icons_paths=[PathHelper.icons_path() + f'/file_viewer/{ICON_SIZE}x{ICON_SIZE}',
                                            PathHelper.icons_path() + f'/control_panel/{ICON_SIZE}x{ICON_SIZE}',
                                            PathHelper.icons_path() + f'/toolbar/{ICON_SIZE}x{ICON_SIZE}'],
                               sizes=[ICON_SIZE] * 3,
                               masks=[False] * 3)

    #IconManipulators.init(IconManipulatorID.SYSTEM, PathHelper.icons_path() + '/system', 100, False)

    # окно приложения
    frame = MainWindow(id=WindowID.MAIN_WINDOW)

    # показываем окно и запускаем основной цикл приложения
    frame.show()
    app.MainLoop()

    #TODO потом вынести в класс app
    clipboard = wx.Clipboard.Get()
    clipboard.Flush()
    jpype.shutdownJVM()

# if __name__ == '__main__':
#     app = App()
