import wx
import wx.dataview as dv
from framework.events import ChangeOriginal


#TODO в разработке
class PopUpDataViewWindow(wx.PopupTransientWindow):
    def __init__(self, parent: wx.Window, flags: int = wx.BORDER_NONE):
        super().__init__(parent, flags)

        self.__menu = wx.ListCtrl(self, style=wx.LC_REPORT | wx.LC_NO_HEADER | wx.LC_HRULES)
        self.__menu.AppendColumn('', width=100)
        self.__menu.InsertItem(0, 'Отметить как оригинал')
        self.__event = None

        self.Bind(wx.EVT_LIST_ITEM_SELECTED, self.__perform, self.__menu)

    def set_event(self, event: dv.DataViewEvent) -> None:
        self.__event = event

    def __perform(self, event: wx.ListEvent) -> None:
        match event.GetId():
            case 0:
                event = ChangeOriginal(item=self.__event.GetItem())
                wx.PostEvent(self.GetParent().GetEventHandler(), event)
        self.Hide()
