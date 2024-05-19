from PySide6.QtCore import Signal
from PySide6.QtWidgets import QComboBox, QWidget, QHBoxLayout, QDoubleSpinBox, QPushButton, QLabel

from spectral_sampling.defaults import default_spectral_sampling_methods
from spectral_sampling.spectral_distribution import SpectralDistribution, Monochromatic


class SpectralDistributionCombo(QWidget):
    """ Widget for selecting spectral distributions """

    onChanged = Signal()

    def __init__(self, parent=None, spectral_sampling_window=None):
        super().__init__(parent)

        self._spectral_sampling_window = spectral_sampling_window

        self.mainLayout = QHBoxLayout()
        self.setLayout(self.mainLayout)

        self.combo = QComboBox()
        self.mainLayout.addWidget(self.combo)

        self.wavelength = QDoubleSpinBox()
        self.wavelength.setMinimum(200)
        self.wavelength.setMaximum(1500)
        self.wavelength.setValue(500)

        self.wavelength_label = QLabel("nm")

        self.new_button = QPushButton("Custom")

        self.n_default = len(default_spectral_sampling_methods)

        self.combo.addItem("Monochromatic")

        self.mainLayout.addWidget(self.combo)
        self.mainLayout.addWidget(self.wavelength)
        self.mainLayout.addWidget(self.wavelength_label)
        self.mainLayout.addWidget(self.new_button)

        for item in default_spectral_sampling_methods:
            self.combo.addItem(item.name)

        if self._spectral_sampling_window is not None:
            for item in self._spectral_sampling_window.customDistributionNames():
                self.combo.addItem(item.name)

        self.combo.currentIndexChanged.connect(self.onSelected)

    def onSelected(self):
        index = self.combo.currentIndex()

        if index == 0:
            self.wavelength.setVisible(True)
            self.wavelength_label.setVisible(True)
        else:
            self.wavelength.setVisible(False)
            self.wavelength_label.setVisible(False)

        self.onChanged.emit()

    def getDistribution(self) -> SpectralDistribution:
        """ Get the selected distribution """

        index = self.combo.currentIndex()
        if index == 0:
            return Monochromatic(self.wavelength.value())
        elif 0 < index < self.n_default + 1:
            return default_spectral_sampling_methods[index-1]
        else:
            raise NotImplementedError("Custom distributions not supported yet")