import wx
import os
from settings.consts import WHITE
from framework.utils import FileManipulator
from typing import Any


class MoveFileWindow(wx.Frame):
    def __init__(self, parent: wx.Window = None, id: int = wx.ID_ANY, size: wx.Size = wx.DefaultSize,
                 pos: wx.Point = wx.DefaultPosition, title: str = 'Переместить файл',
                 style=wx.DEFAULT_FRAME_STYLE, name: str = wx.EmptyString):
        super().__init__(parent=parent, id=id, size=size, pos=pos, title=title, style=style, name=name)

        self.__create_layout()

        # задаём реакцию на события
        self.__move_btn.Bind(wx.EVT_BUTTON, lambda _: self.__move_file())
        self.__cancel_btn.Bind(wx.EVT_BUTTON, lambda _: self.Destroy())
        self.__move_to_filepath.Bind(wx.EVT_TEXT, self.__open_nodes)
        self.__tree_view.Bind(wx.EVT_TREE_ITEM_EXPANDING, self.__add_node)
        self.__tree_view.Bind(wx.EVT_TREE_ITEM_COLLAPSED, lambda event: self.__collapse_and_reset_nodes(event.GetItem()))
        self.__tree_view.Bind(wx.EVT_TREE_SEL_CHANGED, self.__update_move_to)

    def __create_layout(self) -> None:
        """
        Создаём layout окна
        """
        # главный sizer. Нужен, чтобы создать отступы от края окна
        main_sizer = wx.BoxSizer(wx.VERTICAL)

        # создаём sizer для расположения виджетов
        sizer = wx.GridBagSizer(5, 5)

        # создаём виджеты
        self.__current_file = wx.TextCtrl(parent=self, style=wx.TE_READONLY)
        self.__current_file.SetBackgroundColour(WHITE)
        self.__move_to_filepath = wx.TextCtrl(parent=self)
        self.__move_to_filepath.SetBackgroundColour(WHITE)
        self.__tree_view = wx.TreeCtrl(parent=self, style=wx.TR_HIDE_ROOT | wx.TR_TWIST_BUTTONS | wx.TR_DEFAULT_STYLE)
        self.__move_btn = wx.Button(self, label='Переместить')
        self.__cancel_btn = wx.Button(self, label='Отмена')

        # наполняем tree view коренными узлами
        root = self.__tree_view.AddRoot('System')
        drives: list[str] = FileManipulator.get_logical_drives()
        for drive in drives:
            disk = self.__tree_view.AppendItem(root, drive, data=drive)
            files = os.listdir(self.__tree_view.GetItemText(disk))
            for file in files:
                path = os.path.join(drive, file)
                if FileManipulator.is_dir(path):
                    self.__tree_view.AppendItem(parent=disk, text=file, data=path)

        # создаём sizer для кнопок
        btn_sizer = wx.GridBagSizer(5, 5)
        btn_sizer.Add(self.__move_btn, (0, 0))
        btn_sizer.Add(self.__cancel_btn, (0, 1))

        # располагаем виджеты
        sizer.Add(wx.StaticText(self, label='Файл: '), (0, 0), flag=wx.ALIGN_CENTER)
        sizer.Add(self.__current_file, (0, 1), flag=wx.EXPAND)
        sizer.Add(wx.StaticText(self, label='Переместить в: '), (1, 0), flag=wx.ALIGN_CENTER)
        sizer.Add(self.__move_to_filepath, (1, 1), flag=wx.EXPAND)
        sizer.Add(self.__tree_view, (2, 0), span=wx.GBSpan(1, 2), flag=wx.EXPAND)
        sizer.Add(btn_sizer, (3, 1), flag=wx.ALIGN_RIGHT)

        # чтобы TreeView занял всё пространство, делаем ряд и колонки динамичными
        sizer.AddGrowableRow(2)
        sizer.AddGrowableCol(1)

        main_sizer.Add(sizer, 1, wx.ALL | wx.EXPAND, 5)

        self.SetBackgroundColour(WHITE)
        self.SetSizer(main_sizer)
        self.Layout()

    def __add_node(self, event: wx.TreeEvent) -> None:
        """
        Добавляет узлы дочерним элементам, если возможно
        :param event: Событие раскрытия узла
        """
        root: wx.TreeItemId = event.GetItem()
        child: wx.TreeItemId; cookie: Any
        child, cookie = self.__tree_view.GetFirstChild(root)

        # используем ChangeValue, так как SetValue провоцирует событие EVT_TEXT
        self.__move_to_filepath.ChangeValue(self.__tree_view.GetItemData(root))

        while child:
            child_data: str = self.__tree_view.GetItemData(child)

            try:
                files: list[str] = os.listdir(child_data)
                for file in files:
                    path = os.path.join(child_data, file)
                    if FileManipulator.is_dir(os.path.join(path)):
                        self.__tree_view.AppendItem(parent=child, text=file, data=path)

            except (FileNotFoundError, PermissionError):
                pass

            child, cookie = self.__tree_view.GetNextChild(child, cookie)

    def __collapse_and_reset_nodes(self, node: wx.TreeItemId) -> None:
        """
        Закрывает и удаляет у всех дочерних узлов их дочерние узлы
        :param node: Узел, для дочерних узлов которого нужно закрыть и удалить дочерние узлы (формулировка огонь)
        """
        child, cookie = self.__tree_view.GetFirstChild(node)

        while child:
            self.__tree_view.CollapseAndReset(child)
            child, cookie = self.__tree_view.GetNextChild(child, cookie)

    def __update_move_to(self, event: wx.TreeEvent) -> None:
        """
        Обновляем значение текстового поля "Переместить в"
        :param event: Событие выбора узла
        """
        # при закрытии окна появляется ошибка об удалённом виджете, потому сначала проверяем его существование
        if self.__tree_view:
            item_data = self.__tree_view.GetItemData(event.GetItem())
            self.__move_to_filepath.ChangeValue(item_data)

    def __open_nodes(self, event: wx.CommandEvent) -> None:
        """
        Откроет в списке нужный узел при вставке пути в поле
        :param event: Событие вставки в поле ввода
        """
        # приводим путь к нужному формату
        path: str = event.GetString()
        splitted_path = path.replace('\\', '/').split('/')

        splitted_path[0] += '/'

        # сюда будем сохранять найденный узел (поиск начинаем с корня дерева)
        temp: wx.TreeItemId = self.__tree_view.GetRootItem()

        # выполняем очистку, чтобы избежать дублирования узлов
        child, cookie = self.__tree_view.GetFirstChild(temp)
        while child:
            self.__collapse_and_reset_nodes(child)
            child, cookie = self.__tree_view.GetNextChild(child, cookie)

        # ищем улы с нужными именами
        for node in splitted_path:
            child, cookie = self.__tree_view.GetFirstChild(temp)

            while child:
                # если узел подходящий - раскрываем его и запоминаем
                if self.__tree_view.GetItemText(child) == node:
                    self.__tree_view.Expand(child)
                    temp = child
                    break
                else:
                    child, cookie = self.__tree_view.GetNextChild(child, cookie)

    def __move_file(self) -> None:
        """
        Перемещает файл по указанной директории
        """
        FileManipulator.move_file(self.__current_file.GetValue(), self.__move_to_filepath.GetValue())
        self.Destroy()

    def set_current_filepath(self, filepath: str) -> None:
        """
        Выставляет путь к выбранному для перемещения файлу
        :param filepath: Путь к файлу
        """
        self.__current_file.SetValue(filepath)
