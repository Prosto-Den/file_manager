import wx
from windows.mainwindow import MainWindow
from settings.enums import WidgetID, IconManipulatorID
from settings.consts import MAIN_WINDOW_SIZE, ICON_SIZE, ICONS_PATH
from settings.iconManipulators import IconManipulators
from warnings import simplefilter


app = wx.App()
simplefilter(action='always')

IconManipulators.init_many(manipulator_ids=[IconManipulatorID.FILE_VIEWER,
                                            IconManipulatorID.CONTROL_PANEL,
                                            IconManipulatorID.TOOLBAR],
                           icons_paths=[ICONS_PATH + f'/file_viewer/{ICON_SIZE}x{ICON_SIZE}',
                                        ICONS_PATH + f'/control_panel/{ICON_SIZE}x{ICON_SIZE}',
                                        ICONS_PATH + f'/toolbar/{ICON_SIZE}x{ICON_SIZE}'],
                           sizes=[ICON_SIZE,
                                  ICON_SIZE,
                                  ICON_SIZE],
                           masks=[False, False, False])

frame = MainWindow(id=WidgetID.MAIN_WINDOW, size=MAIN_WINDOW_SIZE, title='Prosto File Manager')
frame.show()
app.MainLoop()

# if __name__ == '__main__':
#     app = App()