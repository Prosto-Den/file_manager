import wx
from windows.mainwindow import MainWindow
from settings.enums import WidgetID, IconManipulatorID
from settings.consts import MAIN_WINDOW_SIZE, ICON_SIZE, ICONS_PATH
from settings.iconManipulators import IconManipulators


app = wx.App()
IconManipulators.init_manipulator(manipulator_id=IconManipulatorID.FILE_VIEWER,
                                  icons_path=ICONS_PATH + f'/file_viewer/{ICON_SIZE}x{ICON_SIZE}',
                                  size=ICON_SIZE,
                                  mask=False)
IconManipulators.init_manipulator(manipulator_id=IconManipulatorID.TOOLBAR,
                                  icons_path=ICONS_PATH + f'/toolbar/{ICON_SIZE}x{ICON_SIZE}',
                                  size=ICON_SIZE,
                                  mask=False)
IconManipulators.init_manipulator(manipulator_id=IconManipulatorID.CONTROL_PANEL,
                                  icons_path=ICONS_PATH + f'/control_panel/{ICON_SIZE}x{ICON_SIZE}',
                                  size=ICON_SIZE,
                                  mask=False)

frame = MainWindow(id=WidgetID.MAIN_WINDOW, size=MAIN_WINDOW_SIZE, title='Prosto File Manager')

frame.show()
app.MainLoop()

# if __name__ == '__main__':
#     app = App()