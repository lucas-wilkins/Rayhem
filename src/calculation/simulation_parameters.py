from dataclasses import dataclass

@dataclass
class SimulationParameters:
    minimum_distance: float = 1e-9
    maximum_rays: int = 1_000_000
    minimum_intensity: float = 1e-9
    maximum_iterations: int = 1000

    def serialise(self):
        return {
            "minimum_distance": self.minimum_distance,
            "maximum_rays": self.maximum_rays,
            "minimum_intensity": self.minimum_intensity,
            "maximum_iterations": self.maximum_iterations
        }

    @staticmethod
    def deserialise(data):
        return SimulationParameters(
            data["minimum_distance"],
            data["maximum_rays"],
            data["minimum_intensity"],
            data["maximum_iterations"]
        )
