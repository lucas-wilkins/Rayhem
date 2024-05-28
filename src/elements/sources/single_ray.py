import numpy as np

from elements.source_rays import SourceRays
from elements.sources.source import Source
from gui.reuse.spectral_distribution import SpectralDistributionCombo
from spectral_sampling.spectral_distribution_singleton import SpectralDistributionSpecification, distributions, default


class SingleRay(Source):

    def __init__(self, distribution_spec: SpectralDistributionSpecification = default):
        super().__init__()

        self.distribution_spec = distribution_spec

    @staticmethod
    def library_name() -> str:
        return "Single Ray"

    @staticmethod
    def library_description() -> str:
        return "Single ray."

    @staticmethod
    def serialisation_name() -> str:
        return "single_ray"

    def serialise(self):
        return {"spectral_distribution": self.distribution_spec.serialise()}

    @staticmethod
    def deserialise(data: dict):
        distribution_spec = SpectralDistributionSpecification.deserialise(data["spectral_distribution"])
        return SingleRay(distribution_spec=distribution_spec)

    def settingsWidget(self):
        widget = SpectralDistributionCombo(self.distribution_spec)
        def updateDistributionSpec():
            self.distribution_spec = widget.getSpectralDistributionSpec()
            self.onAnythingChanged()

        widget.onChanged.connect(updateDistributionSpec)

        return widget

    def create_rays(self) -> SourceRays:

        origin = np.zeros((1, 3), dtype=float)

        direction = np.zeros((1, 3), dtype=float)
        direction[:, 2] = 1.0

        intensity = np.ones((1,))

        distribution = distributions.get_distribution(self.distribution_spec)
        wavelengths = distribution.source_wavelengths(1)

        return SourceRays(
            origins=origin,
            directions=direction,
            wavelengths=wavelengths,
            intensities=intensity,
            distribution=distribution)