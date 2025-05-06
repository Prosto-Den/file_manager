from typing import override, LiteralString
from framework.utils import FileUtils
import wx


class RenameWindow(wx.PopupTransientWindow):
    def __init__(self, parent: wx.Window, pos: wx.Point, filepath: LiteralString | str | bytes,
                 flags: int = wx.PU_CONTAINS_CONTROLS) -> None:
        super().__init__(parent=parent, flags=flags)
        self.__entry = wx.TextCtrl(parent=self, style=wx.TE_PROCESS_ENTER)
        self.__filepath = filepath
        text = filepath.split('/')[-1]
        self.__entry.AppendText(text)
        x, _ = self.__entry.GetTextExtent(text)
        self.__entry.SetSize(wx.Size(x + 20, -1))

        if FileUtils.is_file(filepath):
            for i in range(len(text) - 1, 0, -1):
                if text[i] == '.':
                    self.__entry.SetSelection(0, i)
                    break
        else:
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
            old_file_name = new_filepath.pop(-1)
            new_file_name = self.__entry.GetLineText(0)

            if old_file_name == new_file_name:
                return

            new_filepath = '/'.join(new_filepath) + '/' + new_file_name
            FileUtils.rename_file(self.__filepath, new_filepath)