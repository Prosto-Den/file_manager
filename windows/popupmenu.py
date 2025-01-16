import wx
from settings.enums import PopUpItemsID
from .renamewindow import RenameWindow
from settings.consts import ICON_SIZE


class PopUpMenu(wx.PopupTransientWindow):
    def __init__(self, parent: wx.Window, filepath: str, event: wx.ListEvent,
                 flags: int = wx.BORDER_NONE) -> None:
        super().__init__(parent=parent, flags=flags)
        self.__filepath = filepath
        self.__menu = wx.ListCtrl(parent=self, style=wx.LC_REPORT | wx.LC_NO_HEADER)
        self.__event = event.Clone()
        self.__menu.AppendColumn('', width=100)
        self.__menu.InsertItem(PopUpItemsID.DELETE_BTN, 'Удалить')
        self.__menu.InsertItem(PopUpItemsID.RENAME_BTN, 'Переименовать')
        self.__menu.InsertItem(PopUpItemsID.CREATE_BTN, 'Создать')

        self.__menu.Bind(event=wx.EVT_LIST_ITEM_SELECTED, handler=self.__perform)


    def __perform(self, event: wx.ListEvent) -> None:
        match event.GetIndex():
            # удаление файла
            case PopUpItemsID.DELETE_BTN:
                self.Parent.file_system.delete_file(self.__filepath)
            # переименование файла
            case PopUpItemsID.RENAME_BTN:
                list_ctrl: wx.ListCtrl = self.GetParent()
                # получаем положение item на экране
                item_position = list_ctrl.GetItemPosition(self.__event.GetIndex())
                position: wx.Point = list_ctrl.ClientToScreen(item_position)
                # смещаем вправо на размер иконки
                position = wx.Point(position[0] + ICON_SIZE, position[1])
                RenameWindow(self.GetParent(), position, self.__filepath)

        self.destroy()


    def destroy(self) -> None:
        self.Show(False)
        self.Destroy()
        self.__filepath = None
        self.__menu = None
        self.__event = None


    def set_position(self, pos: wx.Point) -> None:
        self.SetPosition(pos)


    def set_size(self, size: wx.Size) -> None:
        self.SetSize(size)
        self.__menu.SetSize(size)
