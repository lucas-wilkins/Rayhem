from dataclasses import dataclass

@dataclass
class SimulationParameters:
    minimum_distance: float = 1e-9
    maximum_rays: int = 10_000_000

    def serialise(self):
        return {
            "minimum_distance": self.minimum_distance,
            "maximum_rays": self.maximum_rays
        }

    @staticmethod
    def deserialise(data):
        return SimulationParameters(
            data["minimum_distance"],
            data["maximum_rays"]
        )   
