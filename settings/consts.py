import wx
import os
from typing import TypeVar


# paths
PROJECT_PATH = os.path.dirname(os.path.abspath('main.py'))
ICONS_PATH = os.path.abspath('icons')

# time format
TIME_FORMAT = "%d.%m.%Y %H:%M"

# sizes
ICON_SIZE = 24
MAIN_WINDOW_SIZE = wx.Size(1095, 900)
PANEL_SIZE = wx.Size(MAIN_WINDOW_SIZE.GetWidth() // 2, MAIN_WINDOW_SIZE.GetHeight())
CONTROL_PANEL_SIZE = wx.Size(MAIN_WINDOW_SIZE.GetWidth() // 2, 60)
FILE_VIEWER_SIZE = wx.Size(PANEL_SIZE.GetWidth(), PANEL_SIZE.GetHeight() - 110)
POPUP_MENU_SIZE = wx.Size(100, 200)
DUPLICATE_WINDOW_SIZE = wx.Size(400, 200)
WARNING_WINDOW_SIZE = wx.Size(400, 200)

# styles
FILE_VIEWER_STYLE = wx.LC_REPORT | wx.LC_HRULES | wx.LC_EDIT_LABELS #| wx.LC_NO_HEADER
DUPLICATE_WINDOW_STYLE = wx.DEFAULT_FRAME_STYLE ^ wx.RESIZE_BORDER ^ wx.MAXIMIZE_BOX
MAIN_WINDOW_STYLE = wx.DEFAULT_FRAME_STYLE ^ wx.RESIZE_BORDER ^ wx.MAXIMIZE_BOX
RENAME_WINDOW_STYLE = wx.DEFAULT_FRAME_STYLE ^ wx.RESIZE_BORDER ^ wx.MAXIMIZE_BOX

# colours
WHITE = wx.Colour(255, 255, 255)

# нужен, чтобы IDE не ругалась на несоответствие типов
WIDGET = TypeVar('WIDGET', bound=wx.Window)