from elements.material import Material

class GeneralMirror:
    """ Generalised Mirror - adds partial reflection """
    def __init__(self, transmission: float = 0.5):
        super().__init__()

        self.transmission = transmission

    @staticmethod
    def serialisation_name() -> str:
        return "general_mirror"

    def serialise(self) -> dict:
        return {"transmission": self.transmission}

    @staticmethod
    def deserialise(data: dict):
        return GeneralMirror(data["transmission"])

