class Path:
    """ Representation of a path through the scene """
    def __init__(self):
        pass

    def update(self):
        pass

    def serialise(self) -> tuple[dict[int, int], dict[int, list[int]]]:
        pass

    @staticmethod
    def deserialise(data: tuple[dict[int, int], dict[int, list[int]]]):
        pass