from framework.utils.file_system import FileSystem
from framework.utils.file_utils import FileUtils
from settings.consts import WHITE
from typing import Any, TypeVar
import wx
import os


#TODO этот класс не кроссплатформенный, работает только на Windows
class TreeViewWindow(wx.Frame):
    """
    Базовый класс для окон перемещения и копирования. \n
    Класс содержит метод _perform без тела. Предполагается, что логика для метода прописывается в дочернем классе.
    Если же метод не будет определён, при его вызове будет выкинуто исключение NotImplementedError
    """
    def _init(self) -> None:
        """
        Инициализация базовых элементов интерфейса
        """
        self._create_layout()

        # задаём реакцию на события
        self.__perform_btn.Bind(wx.EVT_BUTTON, lambda _: self._perform())
        self.__cancel_btn.Bind(wx.EVT_BUTTON, lambda _: self.Destroy())
        self.__entry.Bind(wx.EVT_TEXT, self.__open_nodes)
        self.__tree_view.Bind(wx.EVT_TREE_ITEM_EXPANDING, self.__add_node)
        self.__tree_view.Bind(wx.EVT_TREE_ITEM_COLLAPSED,
                              lambda event: self.__collapse_and_reset_nodes(event.GetItem()))
        self.__tree_view.Bind(wx.EVT_TREE_SEL_CHANGED, self.__update_entry)

    def _perform(self) -> None:
        """
        Метод вызывается при нажатии на кнопку. По умолчанию не определён и поднимает ошибку NotImplementedError
        """
        raise NotImplementedError('Метод не определён')

    def _create_layout(self) -> None:
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
        self.__entry = wx.TextCtrl(parent=self)
        self.__entry.SetBackgroundColour(WHITE)
        self.__tree_view = wx.TreeCtrl(parent=self, style=wx.TR_HIDE_ROOT | wx.TR_TWIST_BUTTONS | wx.TR_DEFAULT_STYLE)
        self.__perform_btn = wx.Button(self)
        self.__cancel_btn = wx.Button(self, label='Отмена')
        self.__label = wx.StaticText(self)

        # наполняем tree view коренными узлами
        root = self.__tree_view.AddRoot('System')
        drives: list[str] = FileSystem.get_logical_drives()
        for drive in drives:
            disk = self.__tree_view.AppendItem(root, drive, data=drive)
            files = os.listdir(self.__tree_view.GetItemText(disk))
            for file in files:
                path = os.path.join(drive, file)
                if FileUtils.is_dir(path):
                    self.__tree_view.AppendItem(parent=disk, text=file, data=path)

        # создаём sizer для кнопок
        btn_sizer = wx.GridBagSizer(5, 5)
        btn_sizer.Add(self.__perform_btn, (0, 0))
        btn_sizer.Add(self.__cancel_btn, (0, 1))

        # располагаем виджеты
        sizer.Add(wx.StaticText(self, label='Файл: '), (0, 0), flag=wx.ALIGN_CENTER)
        sizer.Add(self.__current_file, (0, 1), flag=wx.EXPAND)
        sizer.Add(self.__label, (1, 0), flag=wx.ALIGN_CENTER)
        sizer.Add(self.__entry, (1, 1), flag=wx.EXPAND)
        sizer.Add(self.__tree_view, (2, 0), span=wx.GBSpan(1, 2), flag=wx.EXPAND)
        sizer.Add(btn_sizer, (3, 1), flag=wx.ALIGN_RIGHT)

        # чтобы TreeView занял всё пространство, делаем ряд и колонки динамичными
        sizer.AddGrowableRow(2)
        sizer.AddGrowableCol(1)

        main_sizer.Add(sizer, 1, wx.ALL | wx.EXPAND, 5)

        self.SetBackgroundColour(WHITE)
        self.SetSizer(main_sizer)
        self.Layout()

    def _set_perform_button_label(self, label: str) -> None:
        """
        Установить надпись на кнопку выполнения операции
        :param label: Текст, который будет показан на кнопке
        """
        self.__perform_btn.SetLabel(label)

    def _set_label_text(self, text: str) -> None:
        """
        Установить поясняющую надпись для поля ввода
        :param text: Текст, который будет отображён
        """
        self.__label.SetLabel(text)

    def __add_node(self, event: wx.TreeEvent) -> None:
        """
        Добавляет узлы дочерним элементам, если возможно
        :param event: Событие раскрытия узла
        """
        root: wx.TreeItemId = event.GetItem()
        child: wx.TreeItemId; cookie: Any
        child, cookie = self.__tree_view.GetFirstChild(root)

        while child:
            child_data: str = self.__tree_view.GetItemData(child)

            try:
                files: list[str] = os.listdir(child_data)
                for file in files:
                    path = os.path.join(child_data, file)
                    if FileUtils.is_dir(os.path.join(path)):
                        self.__tree_view.AppendItem(parent=child, text=file, data=path)

            #TODO заменить pass на запись в логи
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

    def __update_entry(self, event: wx.TreeEvent) -> None:
        """
        Обновляем значение текстового поля "Переместить в"
        :param event: Событие выбора узла
        """
        # при закрытии окна появляется ошибка об удалённом виджете, потому сначала проверяем его существование
        if self.__tree_view:
            item_data = self.__tree_view.GetItemData(event.GetItem())
            self.__entry.ChangeValue(item_data)

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

    def _get_current_file_value(self) -> str:
        """
        Получить путь к файлу, над которым выполняется операция
        """
        return self.__current_file.GetValue()

    def _get_entry_value(self) -> str:
        """
        Получить выбранный путь
        """
        return self.__entry.GetValue()

    def set_current_filepath(self, filepath: str) -> None:
        """
        Выставляет путь к выбранному для перемещения файлу
        :param filepath: Путь к файлу
        """
        self.__current_file.SetValue(filepath)

TreeViewType = TypeVar('TreeViewType', bound=TreeViewWindow)