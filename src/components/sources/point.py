import numpy as np
from PySide6.QtWidgets import QWidget, QGridLayout, QLabel, QSpinBox

from components.source_rays import SourceRays
from components.sources.source import Source
from gui.reuse.spectral_distribution import SpectralDistributionCombo
from spectral_sampling.spectral_distribution_singleton import distributions, default, SpectralDistributionSpecification
from util.geodesic import Geodesic

class PointSource(Source):
    def __init__(self, distribution: SpectralDistributionSpecification = default, density=2):
        super().__init__()
        self.distribution = distribution
        self.density = density

    @staticmethod
    def library_name() -> str:
        return "Point Source"

    @staticmethod
    def library_description() -> str:
        return "Simple point source."

    @staticmethod
    def serialisation_name() -> str:
        return "point_source"

    def serialise(self):
        return {
            "spectral_distribution": self.distribution.serialise(),
            "density": self.density
        }

    @staticmethod
    def deserialise(data: dict):
        return PointSource(
            distribution=SpectralDistributionSpecification.deserialise(data["spectral_distribution"]),
            density=int(data["density"]))

    def settingsWidget(self):
        widget = QWidget()
        layout = QGridLayout()
        widget.setLayout(layout)

        combo = SpectralDistributionCombo(self.distribution)

        def samplingChanged():
            self.distribution = combo.getSpectralDistributionSpec()
            self.onAnythingChanged()

        combo.onChanged.connect(samplingChanged)

        n_rays = QSpinBox()
        n_rays.setMaximum(1)
        n_rays.setMaximum(10)
        n_rays.setValue(2)

        def densityChanged():
            self.density = n_rays.value()
            self.onAnythingChanged()

        n_rays.valueChanged.connect(densityChanged)

        layout.addWidget(QLabel("Color"), 0, 0)
        layout.addWidget(QLabel("Ray Density"), 1, 0)

        layout.addWidget(combo, 0, 1)
        layout.addWidget(n_rays, 1, 1)

        return widget

    def create_rays(self) -> SourceRays:
        directions, intensities = Geodesic.by_divisions(self.density)
        origins = np.zeros_like(directions)
        distribution = distributions.get_distribution(self.distribution)
        wavelengths = distribution.source_wavelengths(len(intensities))

        return SourceRays(
            origins=origins,
            directions=directions,
            intensities=intensities,
            wavelengths=wavelengths,
            distribution=distribution)

