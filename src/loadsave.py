
class DeserialisationError(Exception):
    def __init__(self, msg):
        super().__init__(msg)


class Serialisable:

    def element_id(self) -> int:
        raise NotImplementedError(f"element_id not implemented for {self.__class__}")

    @staticmethod
    def serialisation_name() -> str:
        raise NotImplementedError(f"Class has no serialisation name")

    def serialise(self) -> dict:
        raise NotImplementedError(f"Serialisation not implemented for {self.__class__}")

    @staticmethod
    def deserialise(data: dict):
        raise NotImplementedError(f"Deserialisation not implemented")

