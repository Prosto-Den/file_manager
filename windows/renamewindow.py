from typing import override
from framework.utils import FileManipulator
import wx


class RenameWindow(wx.PopupTransientWindow):
    def __init__(self, parent: wx.Window, pos: wx.Point, filepath: str,
                 flags: int = wx.PU_CONTAINS_CONTROLS) -> None:
        super().__init__(parent=parent, flags=flags)
        self.__entry = wx.TextCtrl(parent=self, style=wx.TE_PROCESS_ENTER)
        self.__filepath = filepath

        text = filepath.split('/')[-1]
        if FileManipulator.is_file(self.__filepath):
            suffix = FileManipulator.get_suffix(self.__filepath)
            text = text.replace(suffix, '')

        self.__entry.AppendText(text)
        self.__entry.SetSelection(0, len(text))
        self.__entry.SetFocus()
        self.SetPosition(pos)
        self.SetSize(self.__entry.GetSize())
        self.__entry.Bind(event=wx.EVT_TEXT_ENTER, handler=lambda _: self.Dismiss())
        self.Show(True)

    @override
    def OnDismiss(self) -> None:
        if not self.__entry.IsEmpty():
            new_filepath = self.__filepath.split('/')
            if FileManipulator.is_file(self.__filepath):
                file_suffix = FileManipulator.get_suffix(self.__filepath)
            else:
                file_suffix = ''
            new_filepath.pop(-1)
            new_filepath = '/'.join(new_filepath) + '/' + self.__entry.GetLineText(0) + file_suffix
            FileManipulator.rename_file(self.__filepath, new_filepath)