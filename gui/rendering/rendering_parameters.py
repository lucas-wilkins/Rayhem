from dataclasses import dataclass

@dataclass
class RenderingParameters:
    show_escaped: float = False
    escaped_length: bool = 10

    def serialise(self):
        return {
            "show_escaped": self.show_escaped,
            "escaped_length": self.escaped_length
        }

    @staticmethod
    def deserialise(data):
        return RenderingParameters(
            show_escaped=data["show_escaped"],
            escaped_length=data["escaped_length"]
        )