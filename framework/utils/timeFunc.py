import datetime as dt


def ns_to_datetime(ns: int) -> dt.datetime:
    """Переводит наносекунды в дату
    :param ns: Наносекунды
    :return: Объект класса datetime
    """
    return dt.datetime.fromtimestamp(ns // 1_000_000_000)

def ns_to_datetime_as_string(ns: int, format: str) -> str:
    """Переводит наносекунды в дату
    :param ns: Наносекунды
    :param format: Формат, с которым возвращается дата
    :return: Строку с датой указанного формата
    """
    time = ns_to_datetime(ns)
    return time.strftime(format)