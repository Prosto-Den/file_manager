import wx
from settings.enums import PopUpItemsID
from .renamewindow import RenameWindow
from settings.consts import ICON_SIZE
from framework.utils import FileManipulator


class PopUpMenu(wx.PopupTransientWindow):
    def __init__(self, parent: wx.Window, filepath: str, event: wx.ListEvent,
                 flags: int = wx.BORDER_NONE) -> None:
        super().__init__(parent=parent, flags=flags)
        self.__filepath = filepath
        self.__menu = wx.ListCtrl(parent=self, style=wx.LC_REPORT | wx.LC_NO_HEADER)
        #self.__menu.GetNextSelected()
        self.__event: wx.ListEvent = event.Clone()
        self.__menu.AppendColumn('', width=100)
        self.__menu.InsertItem(PopUpItemsID.DELETE_BTN, 'Удалить')
        self.__menu.InsertItem(PopUpItemsID.RENAME_BTN, 'Переименовать')
        #self.__menu.InsertItem(PopUpItemsID.CREATE_BTN, 'Создать')

        self.__menu.Bind(event=wx.EVT_LIST_ITEM_SELECTED, handler=self.__perform)


    def __perform(self, event: wx.ListEvent) -> None:
        list_ctrl: wx.ListCtrl = self.GetParent()

        match event.GetIndex():
            # удаление файла
            case PopUpItemsID.DELETE_BTN:
                item_id: int = list_ctrl.GetFirstSelected()
                while item_id != -1:
                    item_text: str = list_ctrl.GetItem(item_id).GetText()
                    item_filepath = self.__filepath + fr'/{item_text}'
                    FileManipulator.delete_file(item_filepath)
                    item_id = self.Parent.GetNextSelected(item_id)
            # переименование файла
            case PopUpItemsID.RENAME_BTN:
                # получаем положение item на экране
                item_position = list_ctrl.GetItemPosition(self.__event.GetIndex())
                position: wx.Point = list_ctrl.ClientToScreen(item_position)
                # смещаем вправо на размер иконки
                position = wx.Point(position[0] + ICON_SIZE, position[1])
                RenameWindow(self.GetParent(), position, self.__filepath + '/' + self.__event.GetText())

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
