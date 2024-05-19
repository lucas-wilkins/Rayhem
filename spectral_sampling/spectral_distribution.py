from dataclasses import dataclass

@dataclass
class SpectralDistribution:
    """ Represents the spectral distributions used for converting 'white' light into its components """
    name: str
    description: str
    components: list[tuple[float, float]]

    def serialise(self):
        pass

    @staticmethod
    def deserialise(data: dict):
        pass

class Monochromatic(SpectralDistribution):
    def __init__(self, wavelength):
        super().__init__(
            f"Monochromatic ({wavelength}nm)"
            f"Monochromatic distribution at {wavelength}nm",
            [(wavelength, 1.0)])
