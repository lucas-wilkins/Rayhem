from dataclasses import dataclass

@dataclass
class SpectralDistribution:
    """ Represents the spectral distributions used for converting 'white' light into its components """
    name: str
    description: str
    components: list[list[float, float]]

    @property
    def wavelengths(self):
        return [wl for wl, _ in self.components]

    @property
    def intensities(self):
        return [i for _, i in self.components]

    def serialise(self):
        return {
            "name": self.name,
            "description": self.description,
            "components": self.components
        }

    @staticmethod
    def deserialise(data: dict):
        return SpectralDistribution(
            name=data["name"],
            description=data["description"],
            components=data["components"]
        )

class Monochromatic(SpectralDistribution):
    def __init__(self, wavelength):
        super().__init__(
            f"Monochromatic ({wavelength}nm)"
            f"Monochromatic distribution at {wavelength}nm",
            [(wavelength, 1.0)])
