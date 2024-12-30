class Comparator:
    @staticmethod
    def is_point_in_rect(rect: tuple, point: tuple) -> bool:
        x = rect[0]
        y = rect[1]
        width = rect[2]
        height = rect[3]

        if x <= point[0] <= x + width and y <= point[1] <= y + height:
            return True

        return False