import wx.dataview as dv
import wx


class DuplicateResult(wx.Frame):
    def __init__(self, parent: wx.Window) -> None:
        super().__init__(parent)
        self.SetTitle('Результаты поиска')
        sizer = wx.BoxSizer(wx.VERTICAL)

        self.__tree = dv.DataViewCtrl(self)
        self.__fill_tree()

        sizer.Add(self.__tree)

        self.SetSizer(sizer)
        self.Show()

    def __fill_tree(self) -> None:
        self.__tree.AppendTextColumn('Файл', 0)
        self.__tree.AppendTextColumn('Дата изменения', 1)
        self.__tree.AppendTextColumn('Расположение', 2)
