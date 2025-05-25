from jpype import JString, JClass, JInt


class HashCalculator:
    """
    Обёртка над Java классом для вычисления контрольных сумм файлов
    """
    __JAVA_CLASS_NAME = 'org.hash.HashCalculator'
    __java_class: JClass = None

    @classmethod
    def __get_class(cls) -> JClass:
        if cls.__java_class is None:
            cls.__java_class = JClass(cls.__JAVA_CLASS_NAME)
        return cls.__java_class

    @classmethod
    def mapped_reader(cls, file_path: str, buffer_size: int) -> str:
        """
        Вычисляет контрольную сумму файла с помощью memory mapping.
        :param file_path: Путь к файлу
        :param buffer_size: Размер буфера
        :return: Хеш-сумма файла в 16-ричной системе счисления
        """
        return str(cls.__get_class().mappedReader(JString(file_path), JInt(buffer_size)))

    @classmethod
    def classic_reader(cls, file_path: str, buffer_size: int) -> str:
        """
        Вычисляет контрольную сумму файла простым считыванием частей файла в память
        :param file_path: Путь к файлу
        :param buffer_size: Размер буфера
        :return: Хеш-сумма файла в 16-ричной системе счисления
        """
        return str(cls.__get_class().classicReader(JString(file_path), JInt(buffer_size)))
