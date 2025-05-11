from windows.main_window import MainWindow
from settings.enums import WindowID, IconManipulatorID
from settings.consts import MAIN_WINDOW_SIZE, ICON_SIZE, ICONS_PATH
from settings.icon_manipulators import IconManipulators
from framework.utils.path_helper import PathHelper
import wx


# приложение
app = wx.App()

# подключаем иконки
IconManipulators.init_many(manipulator_ids=[IconManipulatorID.FILE_VIEWER,
                                            IconManipulatorID.CONTROL_PANEL,
                                            IconManipulatorID.TOOLBAR],
                           icons_paths=[PathHelper.icons_path() + f'/file_viewer/{ICON_SIZE}x{ICON_SIZE}',
                                        PathHelper.icons_path() + f'/control_panel/{ICON_SIZE}x{ICON_SIZE}',
                                        PathHelper.icons_path() + f'/toolbar/{ICON_SIZE}x{ICON_SIZE}'],
                           sizes=[ICON_SIZE] * 3,
                           masks=[False] * 3)

IconManipulators.init(IconManipulatorID.SYSTEM, ICONS_PATH + '/system', 100, False)

# окно приложения
frame = MainWindow(id=WindowID.MAIN_WINDOW, size=MAIN_WINDOW_SIZE, title='Prosto File Manager')

# показываем окно и запускаем основной цикл приложения
frame.show()
app.MainLoop()

# if __name__ == '__main__':
#     app = App()