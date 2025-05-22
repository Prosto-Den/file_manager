import wx
import os
from settings.enums import PopUpItemsID
from windows.rename_window import RenameWindow
from windows.move_file_window import MoveFileWindow
from windows.copy_file_window import CopyFileWindow
from settings.consts import ICON_SIZE, MOVE_WINDOW_SIZE
from framework.utils.file_system import FileSystem
from framework.utils.file_utils import FileUtils
from windows.base_windows import TreeViewType
from settings.settings import settings


class PopUpMenu(wx.PopupTransientWindow):
    def __init__(self, parent: wx.Window, event: wx.ListEvent,
                 flags: int = wx.BORDER_NONE) -> None:
        super().__init__(parent=parent, flags=flags)
        self.__menu = wx.ListCtrl(parent=self, style=wx.LC_REPORT | wx.LC_NO_HEADER | wx.LC_HRULES)
        self.__event: wx.ListEvent = event.Clone()
        self.__filepath = None
        self.__menu.AppendColumn('', width=100)
        self.__menu.InsertItem(PopUpItemsID.DELETE_BTN, settings.translation().delete_label)
        self.__menu.InsertItem(PopUpItemsID.RENAME_BTN, settings.translation().rename_label)
        self.__menu.InsertItem(PopUpItemsID.MOVE_INTO_BTN, settings.translation().move_to_popup_label)
        self.__menu.InsertItem(PopUpItemsID.COPY_INTO_BTN, settings.translation().copy_to_popup_label)
        self.__menu.InsertItem(PopUpItemsID.COPY_BTN, settings.translation().copy_label)

        self.__menu.Bind(event=wx.EVT_LIST_ITEM_SELECTED, handler=self.__perform)


    def __perform(self, event: wx.ListEvent) -> None:
        # вынесем общую инициализацию для окон копирования и переноса в отдельную функцию
        def init_tree_view_window(window: TreeViewType) -> None:
            item_id = list_ctrl.GetFirstSelected()
            window.set_current_filepath(self.__filepath + list_ctrl.GetItem(item_id).GetText())
            window.Show()

        list_ctrl: wx.ListCtrl = self.GetParent()

        match event.GetIndex():
            # удаление файла
            case PopUpItemsID.DELETE_BTN:
                item_id: int = list_ctrl.GetFirstSelected()
                while item_id != -1:
                    item_text: str = list_ctrl.GetItem(item_id).GetText()
                    item_filepath = os.path.join(self.__filepath, item_text)
                    FileUtils.delete_file(item_filepath)
                    item_id = self.Parent.GetNextSelected(item_id)

            # переименование файла
            case PopUpItemsID.RENAME_BTN:
                # получаем положение item на экране
                item_position = list_ctrl.GetItemPosition(self.__event.GetIndex())
                position: wx.Point = list_ctrl.ClientToScreen(item_position)
                # смещаем вправо на размер иконки
                position = wx.Point(position[0] + ICON_SIZE, position[1])
                RenameWindow(self.GetParent(), position, os.path.join(self.__filepath, self.__event.GetText()))

            # перемещение файла
            case PopUpItemsID.MOVE_INTO_BTN:
                move_file = MoveFileWindow(parent=self.GetParent(), size=MOVE_WINDOW_SIZE)
                init_tree_view_window(move_file)

            # копирование файла
            case PopUpItemsID.COPY_INTO_BTN:
                copy_file = CopyFileWindow(parent=self.GetParent(), size=MOVE_WINDOW_SIZE)
                init_tree_view_window(copy_file)

            # копирование файла в буфер обмена
            case PopUpItemsID.COPY_BTN:
                item_id: int = list_ctrl.GetFirstSelected()
                files = []
                while item_id != -1:
                    item_text: str = list_ctrl.GetItem(item_id).GetText()
                    item_filepath = os.path.join(self.__filepath, item_text)
                    files.append(item_filepath)
                    item_id = self.Parent.GetNextSelected(item_id)

                FileSystem.copy_to_clipboard(r'\?\\'.join(files))

        self.Destroy()

    def set_position(self, pos: wx.Point) -> None:
        self.SetPosition(pos)

    def set_size(self, size: wx.Size) -> None:
        self.SetSize(size)
        self.__menu.SetSize(size)

    def set_filepath(self, filepath: str) -> None:
        self.__filepath = filepath

