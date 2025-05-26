import wx
import wx.adv
from settings.settings import settings
from settings.enums import Colours
from framework.utils.threads_handler import HashCalculatorThread
from framework.utils.path_helper import PathHelper
from framework.utils.file_system import FileSystem
from typing import override
from windows.duplicate_result_window import DuplicateResult
import os


class HashCalculatorWindow(wx.Frame):
    def __init__(self, parent: wx.Window) -> None:
        super().__init__(parent=parent)
        self.SetSize(wx.Size(400, 150))
        self.SetTitle(settings.translation().hash_window_title)

        sizer = wx.BoxSizer(wx.VERTICAL)

        self.__stop_btn = wx.Button(self, label=settings.translation().cancel_label)
        self.__timer = wx.Timer(self)
        self.__paths = []
        self.__is_recursive = False

        gif_image = wx.adv.AnimationCtrl(self)
        gif_image.LoadFile(FileSystem.path_join(PathHelper.system_icons_path(), 'loading.gif'),
                           wx.adv.ANIMATION_TYPE_GIF)

        gif_image.SetBackgroundColour(Colours.WHITE)
        gif_image.Play()

        sizer.Add(gif_image, flag=wx.ALIGN_CENTER | wx.UP, border=5)
        sizer.Add(wx.StaticText(self, label='Производится поиск, пожалуйста, подождите'),
                  flag=wx.ALIGN_CENTER)
        sizer.Add(self.__stop_btn, flag=wx.ALIGN_RIGHT | wx.UP | wx.RIGHT, border=5)

        self.__stop_btn.Bind(wx.EVT_BUTTON, lambda _: self.__on_end())
        self.Bind(wx.EVT_TIMER, lambda _: self.__check_process(), self.__timer)

        self.SetBackgroundColour(Colours.WHITE)
        self.SetSizer(sizer)

    @override
    def Destroy(self) -> bool:
        DuplicateResult(self.GetParent())
        return super().Destroy()

    @override
    def Show(self, show: bool = True):
        super().Show(show)
        self.__start_calculation()
        return True

    def add_path(self, path: str) -> None:
        self.__paths.append(path)

    def set_recursive_value(self, value: bool) -> None:
        self.__is_recursive = value

    def __start_calculation(self):
        if len(self.__paths) is None:
            self.__cleanup()
            return

        for path in self.__paths:
            HashCalculatorThread.create_thread(path, settings.settings().buffer_size, self.__is_recursive)
        HashCalculatorThread.start()
        self.__timer.Start(100)

    def __on_end(self):
        self.__cleanup()

    def __check_process(self) -> None:
        if not HashCalculatorThread.is_alive():
            self.__timer.Stop()
            self.__cleanup()

    def __cleanup(self) -> None:
        HashCalculatorThread.join(0.5)
        self.Destroy()
