import wx
from windows.base_windows import TreeViewWindow
from typing import override
from framework.events import PathChosen
from settings.settings import settings


class ChoosePathWindow(TreeViewWindow):
    def __init__(self, parent: wx.Window = None, id: int = wx.ID_ANY, size: wx.Size = wx.DefaultSize,
                 pos: wx.Point = wx.DefaultPosition,
                 style=wx.DEFAULT_FRAME_STYLE, name: str = wx.EmptyString) -> None:
        super().__init__(parent=parent, id=id, size=size, pos=pos, style=style, name=name)
        self._init()
        self.SetTitle(settings.translation().choose_directory)

        self._set_current_file_label_text(settings.translation().current_directory)
        self._set_label_text(settings.translation().chosen_directory)
        self._set_perform_button_label(settings.translation().choose_label)

    @override
    def _perform(self) -> None:
        event = PathChosen(filepath=self.get_entered_value())
        parent: wx.Window = self.GetParent()
        wx.PostEvent(parent.GetEventHandler(), event)
        self.Destroy()
