import datetime as dt


class TimeUtils:
    @staticmethod
    def ns_to_datetime(ns: int) -> dt.datetime:
        """Переводит наносекунды в дату
        :param ns: Наносекунды
        :return: Объект класса datetime
        """
        return dt.datetime.fromtimestamp(ns // 1_000_000_000)

    @classmethod
    def ns_to_datetime_as_string(cls, ns: int, format_: str) -> str:
        """Переводит наносекунды в дату
        :param ns: Наносекунды
        :param format_: Формат, с которым возвращается дата
        :return: Строку с датой указанного формата
        """
        time = cls.ns_to_datetime(ns)
        return time.strftime(format_)