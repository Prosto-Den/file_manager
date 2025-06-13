import wx.dataview as dv
import wx
from typing import override, overload
from framework.utils.time_utils import TimeUtils
from settings.settings import settings
from settings.enums import Colours
from database_models.hash import HashModel
from collections import defaultdict, namedtuple
from pathlib import Path


class DuplicateResult(wx.Frame):
    def __init__(self, parent: wx.Window) -> None:
        super().__init__(parent)
        self.SetTitle('Результаты поиска')
        self.SetSize(wx.Size(1000, 400))
        panel = wx.Panel(self)
        sizer = wx.BoxSizer(wx.VERTICAL)

        self.__tree = dv.DataViewCtrl(panel, style=dv.DV_VERT_RULES | dv.DV_ROW_LINES | wx.BORDER_THEME)
        model = DataViewModel()
        self.__fill_tree()
        self.__tree.AssociateModel(model)

        sizer.Add(self.__tree, 1, wx.EXPAND)
        panel.SetSizer(sizer)
        self.Show()

    @override
    def Destroy(self) -> bool:
        self.GetParent().Enable()
        return super().Destroy()

    def __fill_tree(self) -> None:
        self.__tree.AppendTextColumn('Расположение', 0, width=500)
        self.__tree.AppendTextColumn('Дата изменения', 1, width=200)
        self.__tree.AppendTextColumn('Название', 2, width=200)
        #self.__tree.AppendTextColumn('Хеш-сумма', 3, width=200)


class OriginalFile:
    def __init__(self, filename: str, modification_date: int, filepath: str, hash_: str) -> None:
        self.filename = filename
        self.modification_date = TimeUtils.ns_to_datetime_as_string(modification_date, settings.settings().time_format)
        self.filepath = filepath
        self.hash = hash_
        self.duplicates = []


class DuplicateFile:
    def __init__(self, filename: str, modification_date: int, filepath: str, hash_: str) -> None:
        self.filename = filename
        self.modification_date = TimeUtils.ns_to_datetime_as_string(modification_date, settings.settings().time_format)
        self.filepath = filepath
        self.hash = hash_


class DataViewModel(dv.PyDataViewModel):
    def __init__(self) -> None:
        super().__init__()
        self.items = {}
        self.__prepare_data()

        self.Cleared()

    def GetColumnCount(self):
        return 4

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
                       3: node.hash
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
                else:
                    continue
            attr.SetBackgroundColour(colour)
            attr.SetBold(True)
            return True

        elif isinstance(node, DuplicateFile):
            parent: OriginalFile = self.ItemToObject(self.GetParent(item))
            index = parent.duplicates.index(node)
            if index % 2 != 0:
                attr.SetBackgroundColour(Colours.GREY)
            else:
                attr.SetBackgroundColour(Colours.WHITE)
            return True
        return False

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
            root_item = OriginalFile(root.name, root.date, root.filepath, root.hash)
            for i in range(1, len(item)):
                row = list(item)[i]
                row_item = DuplicateFile(row.name, row.date, row.filepath, row.hash)
                root_item.duplicates.append(row_item)
            self.items[id(root_item)] = root_item

        self.items = self.items.values()
