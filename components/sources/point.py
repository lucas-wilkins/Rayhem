from PySide6.QtWidgets import QWidget, QVBoxLayout, QGridLayout, QLabel, QSpinBox

from components.sources.source import Source
from gui.reuse.spectral_distribution import SpectralDistributionCombo


class PointSource(Source):
    def __init__(self):
        super().__init__()

    @staticmethod
    def library_name() -> str:
        return "Point Source"

    @staticmethod
    def library_description() -> str:
        return "Simple point source."

    def settingsWidget(self):
        widget = QWidget()
        layout = QGridLayout()
        widget.setLayout(layout)

        n_rays = QSpinBox()
        n_rays.setMaximum(1)
        n_rays.setMaximum(10)
        n_rays.setValue(2)

        layout.addWidget(QLabel("Color"), 0, 0)
        layout.addWidget(QLabel("Ray Density"), 1, 0)

        layout.addWidget(SpectralDistributionCombo(), 0, 1)
        layout.addWidget(n_rays, 1, 1)

        return widget

