import wx
from typing import override
from windows.base_windows import TreeViewWindow
from framework.utils import FileUtils
from settings.settings import settings


class MoveFileWindow(TreeViewWindow):
    def __init__(self, parent: wx.Window = None, id: int = wx.ID_ANY, size: wx.Size = wx.DefaultSize,
                 pos: wx.Point = wx.DefaultPosition,
                 style=wx.DEFAULT_FRAME_STYLE, name: str = wx.EmptyString):
        super().__init__(parent=parent, id=id, size=size, pos=pos, style=style, name=name)
        self.SetTitle(settings.translation().move_window_title)

        self._init()

        self._set_label_text(settings.translation().move_to_label)
        self._set_perform_button_label(settings.translation().move_label)

    @override
    def _perform(self) -> None:
        """
        Переместить файл в указанную директорию
        """
        FileUtils.move_file(self._get_current_file_value(), self._get_entry_value())
        self.Destroy()
