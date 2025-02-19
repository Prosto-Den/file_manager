from __future__ import annotations
from settings.enums import WindowID
from settings.consts import DUPLICATE_WINDOW_STYLE
from typing import TYPE_CHECKING
import wx

if TYPE_CHECKING:
    from windows.mainwindow import MainWindow


class FindDuplicateWindow(wx.Frame):
    def __init__(self, parent: MainWindow, id=WindowID.DUPLICATE_WINDOW, size=wx.DefaultSize,
                 pos: wx.Point= wx.DefaultPosition, title='Поиск дубликатов',
                 style=DUPLICATE_WINDOW_STYLE, name: str = wx.EmptyString) -> None:
        super().__init__(parent=parent, id=id, size=size, pos=pos, title=title, style=style, name=name)

