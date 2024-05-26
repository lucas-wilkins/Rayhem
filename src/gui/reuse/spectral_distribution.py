from PySide6.QtCore import Signal
from PySide6.QtWidgets import QComboBox, QWidget, QHBoxLayout, QDoubleSpinBox, QPushButton, QLabel

from spectral_sampling.defaults import default_spectral_sampling_methods
from spectral_sampling.spectral_distribution import SpectralDistribution
from spectral_sampling.spectral_distribution_singleton import distributions, SpectralDistributionSpecification, default


class SpectralDistributionCombo(QWidget):
    """ Widget for selecting spectral distributions """

    onChanged = Signal()

    def __init__(self, sampling_distribution_spec: SpectralDistributionSpecification | None = None, parent=None):
        super().__init__(parent)

        if sampling_distribution_spec is None:
            sampling_distribution_spec = default

        self._initial_index = sampling_distribution_spec.index
        self._initial_wavelength = 500.0 if sampling_distribution_spec.wavelength is None else sampling_distribution_spec.wavelength

        self.mainLayout = QHBoxLayout()
        self.setLayout(self.mainLayout)

        self.combo = QComboBox()
        self.mainLayout.addWidget(self.combo)

        self.wavelength_spinbox = QDoubleSpinBox()
        self.wavelength_spinbox.setMinimum(200)
        self.wavelength_spinbox.setMaximum(1500)
        self.wavelength_spinbox.setValue(self._initial_wavelength)
        self.wavelength_spinbox.valueChanged.connect(self.onWavelengthChanged)

        self.wavelength_label = QLabel("nm")

        self.new_button = QPushButton("Custom")

        self.n_default = len(default_spectral_sampling_methods)

        self.mainLayout.addWidget(self.combo)
        self.mainLayout.addWidget(self.wavelength_spinbox)
        self.mainLayout.addWidget(self.wavelength_label)
        self.mainLayout.addWidget(self.new_button)

        for name in distributions.distribution_names():
            self.combo.addItem(name)


        if self._initial_index == 0:
            self.wavelength_spinbox.setVisible(True)
            self.wavelength_label.setVisible(True)
        else:
            self.wavelength_spinbox.setVisible(False)
            self.wavelength_label.setVisible(False)


        self.combo.setCurrentIndex(self._initial_index)

        self.combo.currentIndexChanged.connect(self.onSelected)

    def onSelected(self):
        """ Triggered when different sampling is selected"""
        index = self.combo.currentIndex()

        if index == 0:
            self.wavelength_spinbox.setVisible(True)
            self.wavelength_label.setVisible(True)
        else:
            self.wavelength_spinbox.setVisible(False)
            self.wavelength_label.setVisible(False)

        self.onChanged.emit()

    def onWavelengthChanged(self):
        """ Triggered when wavelength is changed"""
        self.onChanged.emit()

    def getSpectralDistributionSpec(self) -> SpectralDistributionSpecification:

        index = self.combo.currentIndex()
        wavelength = self.wavelength_spinbox.value() if index == 0 else None
        return SpectralDistributionSpecification(index, wavelength)

    def getDistribution(self) -> SpectralDistribution:
        """ Get the selected distribution """

        return distributions.get_distribution(self.getSpectralDistributionSpec())


