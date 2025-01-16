import hashlib as _hl


class DuplicateFinder:
    @staticmethod
    def calc_checksum(filepath: str) -> str:
        algorithm = _hl.sha1()

        with open(filepath, 'rb') as file:
            algorithm.update(file.read())

        return algorithm.hexdigest()
