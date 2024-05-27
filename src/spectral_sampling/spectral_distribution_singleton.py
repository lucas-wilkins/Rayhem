from dataclasses import dataclass

from PySide6.QtCore import QObject, Signal

from spectral_sampling.spectral_distribution import SpectralDistribution, Monochromatic
from spectral_sampling.defaults import default_spectral_sampling_methods

@dataclass
class SpectralDistributionSpecification:
    index: int
    wavelength: float | None = None

    def serialise(self):
        out = {"index": self.index}
        if self.wavelength is not None:
            out["wavelength"] = self.wavelength
        return out

    @staticmethod
    def deserialise(data):
        index = data["index"]
        if "wavelength" in data:
            return SpectralDistributionSpecification(index=index, wavelength=data["wavelength"])
        else:
            return SpectralDistributionSpecification(index=index)


class SpectralDistributionSingleton(QObject):
    """ Singleton that manages the spectral distributions """

    custom_distribution_updated = Signal()

    def __init__(self):
        super().__init__()

        self.custom_distributions: list[SpectralDistribution] = []

    def serialise(self) -> dict:
        return {"custom_distributions": [distro.serialise() for distro in self.custom_distributions]}


    def deserialise(self, data: list[dict], append=False):

        distros = [SpectralDistribution.deserialise(datum) for datum in data["custom_distributions"]]
        if append:
            self.custom_distributions += distros
        else:
            self.custom_distributions = distros

    def custom_distribution_names(self) -> list[str]:
        """ List containing names of custom distributions """
        return [distro.name for distro in self.custom_distributions]

    def default_distribution_names(self) -> list[str]:
        """ List containing names of default distributions """
        return ["Monochromatic"] + [distro.name for distro in default_spectral_sampling_methods]

    def distribution_names(self) -> list[str]:
        """ List containing the names of all distributions """
        return self.default_distribution_names() + self.custom_distribution_names()

    def is_custom(self, index):
        """ Is the spectrum with index `index` a custom spectrum """
        return index < len(default_spectral_sampling_methods) + 1

    def get_distribution(self, specification: SpectralDistributionSpecification) -> SpectralDistribution:
        """ Get a distribution with the specification (essentially an index, but with a
        wavelength specified for index 0)"""

        rel_index = specification.index

        if rel_index == 0:
            return Monochromatic(specification.wavelength)

        rel_index -= 1

        if rel_index < len(default_spectral_sampling_methods):
            return default_spectral_sampling_methods[rel_index]

        rel_index -= len(default_spectral_sampling_methods)

        if rel_index < len(self.custom_distributions):
            return self.custom_distributions[rel_index]

        raise IndexError(f"No distribution with index {specification.index}")


distributions = SpectralDistributionSingleton()

default = SpectralDistributionSpecification(1, None)  # First non-monochromatic
