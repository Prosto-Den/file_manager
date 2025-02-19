# скорее всего уже не нужен
class FileSize:
    def __init__(self, file_size: str) -> None:
        if file_size == '':
            self.__size = 0
            self.__dimension = None
        else:
            file_size = file_size.split(' ')
            self.__size = float(file_size[0])
            self.__dimension = file_size[1]

    @property
    def size(self) -> float:
        return self.__size

    @property
    def dimension(self) -> str:
        return self.__dimension

    def __str__(self) -> str:
        return f"{self.__size} {self.__dimension}"