import wx
from widgets.fileViewer import FileViewer
from widgets.controlPanel import ControlPanel
from windows.mainwindow import MainWindow
from settings.enums import WidgetID
from settings.consts import (MAIN_WINDOW_SIZE, LEFT_PANEL_SIZE, RIGHT_PANEL_SIZE,
                             ICON_SIZE, ICONS_PATH, CONTROL_PANEL_SIZE)
from settings.iconManipulators import IconManipulators, IconManipulatorID


app = wx.App()
IconManipulators.init(file_viewer_icons=ICONS_PATH + f'/file_viewer/{ICON_SIZE}x{ICON_SIZE}',
                      control_panel_icons=ICONS_PATH + f'/control_panel/{ICON_SIZE}x{ICON_SIZE}',
                      toolbar_icons=ICONS_PATH + f'/toolbar/{ICON_SIZE}x{ICON_SIZE}',
                      size=ICON_SIZE,
                      mask=False)
file_viewer_icons = IconManipulators.get_icon_manipulator(IconManipulatorID.FILE_VIEWER)
frame = MainWindow(id=WidgetID.MAIN_WINDOW, size=MAIN_WINDOW_SIZE, title='Prosto File Manager')
sizer = wx.FlexGridSizer(rows=2, cols=2, hgap=0, vgap=0)
frame.Center(wx.BOTH)
toolbar_height = frame.GetToolBar().GetSize().GetHeight() // 2 - 9

left_control_panel = ControlPanel(parent=frame, id=WidgetID.LEFT_CONTROL_PANEL, size=CONTROL_PANEL_SIZE)
right_control_panel = ControlPanel(parent=frame, id=WidgetID.RIGHT_CONTROL_PANEL,size=CONTROL_PANEL_SIZE)
control_panel_height = CONTROL_PANEL_SIZE.GetHeight()
left_panel = wx.Panel(parent=frame, size=LEFT_PANEL_SIZE)
right_panel = wx.Panel(parent=frame, size=RIGHT_PANEL_SIZE)

file_viewer1 = FileViewer(parent=left_panel, id=WidgetID.LEFT_FILE_VIEWER)
                          #filepath=r'C:\Users\Prosto_Den\Desktop')
file_viewer2 = FileViewer(parent=right_panel, id=WidgetID.RIGHT_FILE_VIEWER,
                          filepath=r'C:\Users\Prosto_Den\Desktop')
file_viewer1.SetImageList(file_viewer_icons, wx.IMAGE_LIST_SMALL)
file_viewer2.SetImageList(file_viewer_icons, wx.IMAGE_LIST_SMALL)

sizer.Add(left_control_panel)
sizer.Add(right_control_panel)
sizer.Add(left_panel, flag=wx.EXPAND)
sizer.Add(right_panel, flag=wx.EXPAND)

sizer.Fit(frame)
frame.SetSizer(sizer)
frame.Layout()
frame.show()
app.MainLoop()

# if __name__ == '__main__':
#     app = App()