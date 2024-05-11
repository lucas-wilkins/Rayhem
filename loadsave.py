
class DeserialisationError(Exception):
    def __init__(self, msg):
        super().__init__(msg)


class SerialisableElement:
    def serialise(self) -> dict:
        raise NotImplementedError(f"Serialisation not implemented for {self.__class__}")

    @staticmethod
    def deserialise(data: dict):
        raise NotImplementedError(f"Deserialisation not implemented")