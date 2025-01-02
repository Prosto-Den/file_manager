import hashlib as hl


class DuplicateFinder:
    @staticmethod
    def calc_checksum(filepath: str) -> str:
        algorithm = hl.sha1()

        with open(filepath, 'rb') as file:
            algorithm.update(file.read())

        return algorithm.hexdigest()
