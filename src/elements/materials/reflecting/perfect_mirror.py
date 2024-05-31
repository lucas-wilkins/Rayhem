from elements.material import Material


class PerfectMirror(Material):
    def __init__(self):
        pass

    @staticmethod
    def serialisation_name() -> str:
        return "perfect_mirror"

    def serialise(self) -> dict:
        return {}

    @staticmethod
    def deserialise(data: dict):
        return PerfectMirror()

    def is_dispersive(self):
        return False


