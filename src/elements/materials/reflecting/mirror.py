from elements.material import Material


class Mirror(Material):
    def __init__(self):
        pass

    @staticmethod
    def serialisation_name() -> str:
        return "mirror"

    def serialise(self) -> dict:
        return {}

    @staticmethod
    def deserialise(data: dict):
        return Mirror()

    def is_dispersive(self):
        return False


