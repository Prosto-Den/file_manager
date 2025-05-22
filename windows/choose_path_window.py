import wx
from framework.base_windows.treeview_window import TreeViewWindow
from typing import override
from framework.events import PathChosen


class ChoosePathWindow(TreeViewWindow):
    def __init__(self, parent: wx.Window = None, id: int = wx.ID_ANY, size: wx.Size = wx.DefaultSize,
                 pos: wx.Point = wx.DefaultPosition, title: str = 'Выбрать директорию',
                 style=wx.DEFAULT_FRAME_STYLE, name: str = wx.EmptyString) -> None:
        super().__init__(parent=parent, id=id, size=size, pos=pos, title=title, style=style, name=name)
        self._init()

        self._set_current_file_label_text('Текущая директория: ')
        self._set_label_text('Выбранная директория: ')
        self._set_perform_button_label('Выбрать')

    @override
    def _perform(self) -> None:
        event = PathChosen(filepath=self.get_entered_value())
        parent: wx.Window = self.GetParent()
        wx.PostEvent(parent.GetEventHandler(), event)
        self.Destroy()
