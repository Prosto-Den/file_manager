import wx
import hashlib as hl
import pathlib as pl
from widgets.fileViewer import FileViewer
from settings.enums import WidgetID
from settings.consts import DUPLICATE_WINDOW_STYLE


class FindDuplicateWindow(wx.Frame):
    def __init__(self, parent: wx.Window=None, id=wx.ID_ANY, size=wx.Size(400, 200),
                 pos: wx.Point= wx.DefaultPosition, title='Поиск дубликатов',
                 style=DUPLICATE_WINDOW_STYLE, name: str = wx.EmptyString) -> None:
        super().__init__(parent=parent, id=id, size=size, pos=pos, title=title, style=style, name=name)

        self.FindWindowById(WidgetID.MAIN_WINDOW).Disable()
        self.SetBackgroundColour(wx.Colour(255, 255, 255))
        self.__progress_bar = wx.Gauge(parent=self)
        self.__progress_bar.Center()
        self.__label = wx.StaticText(parent=self)
        self.__label.Center(wx.HORIZONTAL)
        self.__label.Show(True)
        self.Show(True)
        self.find_duplicates()

    def __del__(self):
        main_window: wx.Window = self.FindWindowById(WidgetID.MAIN_WINDOW)
        main_window.Enable()
        main_window.SetFocus()

    @staticmethod
    def __calc_checksum(file_path: str) -> str:
        algorithm = hl.sha1()

        with open(file_path, 'rb') as file:
            algorithm.update(file.read())

        return algorithm.hexdigest()

    def __get_checksums(self, file_viewer: FileViewer) -> dict[str, str]:
        self.__label.SetLabel('Вычисление контрольных сумм')
        self.__label.Center(wx.HORIZONTAL)
        files = file_viewer.file_system.listdir(True)
        result = dict()

        self.__progress_bar.SetRange(len(files))
        self.__progress_bar.SetValue(0)

        for index, file in enumerate(files, start=1):
            if pl.Path(file).is_file():
                result[self.__calc_checksum(file)] = file

            self.__progress_bar.SetValue(index)

        return result

    def __check_checksums(self, checksum_dict_1: dict[str, str], checksum_dict_2: dict[str, str]) -> list[str]:
        self.__label.SetLabel('Вычисление контрольных сумм')
        self.__label.Center(wx.HORIZONTAL)
        self.__progress_bar.SetRange(len(checksum_dict_1))
        self.__progress_bar.SetValue(0)
        result = []

        for index, (key1, value1) in enumerate(checksum_dict_1.items(), start=1):
            file_path1 = pl.Path(value1)
            for key2, value2 in checksum_dict_2.items():
                if key1 == key2 and file_path1.suffix == pl.Path(value2).suffix:
                    result.append(value1)
                    result.append(value2)

            self.__progress_bar.SetValue(index)

        return result

    def find_duplicates(self) -> None:
        file_viewer1: FileViewer = self.FindWindowById(WidgetID.LEFT_FILE_VIEWER)
        file_viewer2: FileViewer = self.FindWindowById(WidgetID.RIGHT_FILE_VIEWER)

        if file_viewer1.file_system.GetPath() == file_viewer2.file_system.GetPath():
            self.__progress_bar.Show(False)
            self.__label.SetLabel('Это одинаковые директории')
            self.__label.Center()
            return

        checksums1 = self.__get_checksums(file_viewer1)
        checksums2 = self.__get_checksums(file_viewer2)

        result = self.__check_checksums(checksums1, checksums2)

        self.__progress_bar.Show(False)
        self.__label.SetLabel('Найденные дубликаты')
        self.__label.Center(wx.HORIZONTAL)

        result_list = wx.ListCtrl(parent=self, pos=wx.Point(0, 50), size=wx.Size(400, 100),
                                  style=wx.LC_REPORT | wx.LC_NO_HEADER | wx.LC_HRULES)
        result_list.AppendColumn('', width=200)
        result_list.AppendColumn('', width=200)

        for file_index in range(0, len(result), 2):
            result_list.Append([result[file_index].split('/')[-1], result[file_index + 1].split('/')[-1]])

        result_list.Show(True)
