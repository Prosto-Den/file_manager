from database_models.hash import HashModel
from framework.utils.file_system import FileSystem
from framework.utils.file_utils import FileUtils
from threading import Thread
import os


class HashCalculatorThread:
    """
    Класс, отвечающий за управление потоками для вычисления контрольных сумм
    """
    __threads: list[Thread] = []

    @classmethod
    def create_thread(cls, path: str, buffer_size: int, is_recursive: bool = False) -> None:
        """
        Создаёт поток для вычисления контрольных сумм
        :param path: Путь к директории, для файлов которой вычисляем контрольные суммы
        :param buffer_size: Размер буфера для чтения данных
        :param is_recursive: True - вычислять контрольные суммы и для файлов поддиректорий. False - только
        для файлов этой директории
        :return:
        """
        cls.__threads.append(Thread(target=cls.__calc_hash, args=(path, buffer_size, is_recursive), daemon=True))

    @classmethod
    def __calc_hash(cls, path: str, buffer_size: int, is_recursive: bool = False) -> None:
        """
        Функция, вызываемая потоком. Отвечает за вычисление контрольных сумм. Результаты записываются в БД
        :param path: Путь к директории, для файлов которой вычисляем контрольные суммы
        :param buffer_size: Размер буфера для чтения данных
        :param is_recursive: True - вычислять контрольные суммы и для файлов поддиректорий. False - только
        для файлов этой директории
        :return:
        """
        # обходим по всему, что есть в директории (игнорируем папки)
        for current, _, files in os.walk(path):
            for file in files:
                filepath = os.path.join(current, file)
                modification_date = FileUtils.get_modification_date(filepath)
                data = HashModel.select_by_filepath(filepath)

                # если в БД нет данных о файле, или у них не совпадают даты изменения, то вычисляем новую хеш-сумму
                if data is None or data.modification_date != modification_date:
                    HashModel.insert(*FileUtils.calc_hash(filepath, buffer_size))

            # выходим, если не нужны рекурсивные вычисления
            if not is_recursive:
                break

    @classmethod
    def start(cls) -> None:
        """
        Запускает все созданные потоки на выполнение
        :return:
        """
        for thread in cls.__threads:
            thread.start()

    @classmethod
    def join(cls, timeout: float | None = None) -> None:
        """
        Ожидание завершений потоков
        :param timeout: None - ожидаем, пока поток закончит работу. float - даём потоку столько
        времени на завершение задач. После этого завершаем выполнение потока
        :return:
        """
        for thread in cls.__threads:
            thread.join(timeout)
        cls.__threads = []

    @classmethod
    def is_alive(cls) -> bool:
        """
        Проверяем, заняты ли потоки выполнением задачи. Вернёт True, если хотя бы один поток ещё занят
        :return:
        """
        if len(cls.__threads) == 0:
            return False
        return any([thread.is_alive() for thread in cls.__threads])
