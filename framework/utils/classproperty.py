class ClassProperty:
    """
    поскольку в питоне класс проперти начиная с версии 3.11 считаются deprecated,
    вот кастомный класспроперти, по сути использование как с обычными @property,
    чтобы это управление полями класса Settings было более pythonic way (вайя)
    """
    def __init__(self, fget=None, fset=None):
        self.__fget = fget
        self.__fset = fset

    def __get__(self, instance, owner):
        if not self.__fget:
            raise AttributeError("can't get attribute")
        return self.__fget(owner)

    def __set__(self, instance, value):
        if not self.__fset:
            raise AttributeError("can't set attribute")
        return self.__fset(type(instance) if instance else instance, value)

    def setter(self, fset):
        self.__fset = fset
        return self

def classproperty(func):
    return ClassProperty(fget=func)
