import wx.dataview as dv
import wx
from typing import override
from framework.utils.time_utils import TimeUtils
from app_manager import AppManager
from settings.enums import Colours
from database_models.hash import HashModel
from collections import defaultdict, namedtuple
from pathlib import Path
from windows.popup_dataview_window import PopUpDataViewWindow


class DuplicateResult(wx.Frame):
    def __init__(self, parent: wx.Window) -> None:
        super().__init__(parent)
        self.SetTitle('Результаты поиска')
        self.SetSize(wx.Size(1000, 400))
        sizer = wx.BoxSizer(wx.VERTICAL)
        btn_sizer = wx.BoxSizer(wx.HORIZONTAL)

        self.__tree = dv.DataViewCtrl(self, style=dv.DV_VERT_RULES | dv.DV_ROW_LINES | wx.BORDER_THEME)
        self.__popup_menu = PopUpDataViewWindow(self)
        model = DataViewModel()
        self.__fill_tree()
        self.__tree.AssociateModel(model)

        sizer.Add(self.__tree, 1, wx.EXPAND)
        self.SetSizer(sizer)
        self.Show()

        self.Bind(dv.EVT_DATAVIEW_ITEM_CONTEXT_MENU, self.__swap_items, self.__tree)

    def __swap_items(self, event: dv.DataViewEvent) -> None:
        #TODO по хорошему бы вызывать контекстное меню, но пока так
        model: DataViewModel = self.__tree.GetModel()
        node = model.ItemToObject(event.GetItem())

        if isinstance(node, DuplicateFile):
            parent = node.parent
            model.swap_items(parent, node)
            model.ItemChanged(model.ObjectToItem(parent))
            model.ItemChanged(model.ObjectToItem(node))


    @override
    def Destroy(self) -> bool:
        self.GetParent().Enable()
        return super().Destroy()

    def __fill_tree(self) -> None:
        self.__tree.AppendTextColumn('Расположение', 0, width=500)
        self.__tree.AppendTextColumn('Дата изменения', 1, width=200)
        self.__tree.AppendTextColumn('Название', 2, width=200)
        self.__tree.AppendToggleColumn('Выбрать', 3, width=200, mode=dv.DATAVIEW_CELL_ACTIVATABLE)


class OriginalFile:
    def __init__(self, filename: str, modification_date: str, filepath: str, hash_: str) -> None:
        self.filename = filename
        self.modification_date = modification_date
        self.filepath = filepath
        self.hash = hash_
        self.duplicates = []


class DuplicateFile:
    def __init__(self, filename: str, modification_date: str, filepath: str, hash_: str, chosen: bool = False,
                 parent: OriginalFile = None) -> None:
        self.filename = filename
        self.modification_date = modification_date
        self.filepath = filepath
        self.chosen = chosen
        self.hash = hash_
        self.parent = parent


class DataViewModel(dv.PyDataViewModel):
    def __init__(self) -> None:
        super().__init__()
        self.items = {}
        self.__prepare_data()
        self.Cleared()

    def GetColumnCount(self):
        return 5

    @override
    def GetChildren(self, item, children) -> int:
        if not item:
            for original in self.items:
                children.append(self.ObjectToItem(original))
            return len(self.items)

        node = self.ItemToObject(item)
        if isinstance(node, OriginalFile):
            for duplicate in node.duplicates:
                children.append(self.ObjectToItem(duplicate))
            return len(node.duplicates)
        return 0

    @override
    def IsContainer(self, item) -> bool:
        if not item:
            return True
        node = self.ItemToObject(item)
        return isinstance(node, OriginalFile)

    @override
    def GetParent(self, item):
        if not item:
            return dv.NullDataViewItem

        node = self.ItemToObject(item)
        if isinstance(node, OriginalFile):
            return dv.NullDataViewItem
        elif isinstance(node, DuplicateFile):
            for original in self.items:
                if original.hash == node.hash:
                    return self.ObjectToItem(original)

    @override
    def SetValue(self, variant, item, col):
        node = self.ItemToObject(item)
        if isinstance(node, DuplicateFile):
            if col == 3:
                node.chosen = variant
        return True

    @override
    def GetValue(self, item, col):
        node = self.ItemToObject(item)

        if isinstance(node, OriginalFile):
            mapper = { 0: node.filepath,
                       1: node.modification_date,
                       2: node.filename,
                       3: node.hash
                       }
            return mapper[col]
        elif isinstance(node, DuplicateFile):
            mapper = { 0: node.filepath,
                       1: node.modification_date,
                       2: node.filename,
                       3: node.chosen,
                       4: node.hash
                       }
            return mapper[col]
        else:
            raise RuntimeError('Unknown node type')

    @override
    def GetAttr(self, item, col, attr) -> bool:
        node = self.ItemToObject(item)
        if isinstance(node, OriginalFile):
            for index, value in enumerate(self.items):
                if node == value:
                    colour = Colours.LIGHT_GREEN if index % 2 != 0 else Colours.DARK_GREEN
                    attr.SetBackgroundColour(colour)
                    attr.SetBold(True)
                    break
            return True

        elif isinstance(node, DuplicateFile):
            parent: OriginalFile = self.ItemToObject(self.GetParent(item))
            index = parent.duplicates.index(node)
            colour = Colours.GREY if index % 2 != 0 else Colours.WHITE
            attr.SetBackgroundColour(colour)
            return True

        return False

    def swap_items(self, parent: OriginalFile, child: DuplicateFile) -> None:
        parent.filepath, child.filepath = child.filepath, parent.filepath
        parent.filename, child.filename = child.filename, parent.filename
        parent.modification_date, child.modification_date = child.modification_date, parent.modification_date


    def __prepare_data(self) -> None:
        data = HashModel.select_all_duplicates()
        Row = namedtuple('Row', ['hash', 'name', 'date', 'filepath'])
        data_dict = defaultdict(set[Row])

        # итерируем по полученным данным и собираем файлы по группам
        # будем считать первый элемент в каждом множестве оригинальным файлом
        for item in data:
            data_dict[item.hash].add(Row(item.hash, Path(item.file_path).name, item.modification_date, item.file_path))
            data_dict[item.hash].add(Row(item.hash, Path(item.duplicate_filepath).name, item.duplicate_modification_date,
                                         item.duplicate_filepath))

        # превращаем эти данные в item для дерева
        for item in data_dict.values():
            root = list(item)[0]
            modification_date = TimeUtils.ns_to_datetime_as_string(root.date,
                                                                   AppManager.settings().get_instance().time_format)
            root_item = OriginalFile(root.name, modification_date, root.filepath, root.hash)
            for i in range(1, len(item)):
                row = list(item)[i]
                modification_date = TimeUtils.ns_to_datetime_as_string(row.date,
                                                                       AppManager.settings().get_instance().time_format)
                row_item = DuplicateFile(row.name, modification_date, row.filepath, row.hash, False, root_item)
                root_item.duplicates.append(row_item)
            self.items[id(root_item)] = root_item

        self.items = self.items.values()
