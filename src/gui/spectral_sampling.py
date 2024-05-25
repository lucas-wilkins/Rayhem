from PySide6.QtWidgets import QDockWidget, QWidget, QHBoxLayout, QComboBox, QPushButton, QVBoxLayout, QSpacerItem, \
    QSizePolicy
import matplotlib
matplotlib.use('QtAgg')

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt


from spectral_sampling.spectral_distribution_singleton import distributions, SpectralDistributionSpecification


class SpectralSamplingWindow(QDockWidget):
    """ Window to display the spectral sampling settings """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Spectral Distribution")


        self.controlPanel = QWidget()

        self.controlLayout = QHBoxLayout()
        self.selection = QComboBox()
        for element in distributions.distribution_names()[1:]: # Ignore monochromatic
            self.selection.addItem(element)
        self.selection.currentIndexChanged.connect(self.onSelection)

        self.edit_button = QPushButton("Edit")
        self.edit_button.clicked.connect(self.edit)

        self.new_button = QPushButton("New")
        self.new_button.clicked.connect(self.new)

        self.delete_button = QPushButton("Delete")
        self.delete_button.clicked.connect(self.delete)

        self.controlLayout.addWidget(self.selection)
        self.controlLayout.addWidget(self.edit_button)
        self.controlLayout.addWidget(self.new_button)
        self.controlLayout.addWidget(self.delete_button)

        self.controlPanel.setLayout(self.controlLayout)

        self.mainPanel = QWidget()
        self.mainLayout = QVBoxLayout()
        self.mainPanel.setLayout(self.mainLayout)

        self.mainLayout.addWidget(self.controlPanel)

        self.figure = Figure(figsize=(5, 3))
        self.figure_canvas = FigureCanvas(self.figure)

        # layout.addWidget(NavigationToolbar(static_canvas, self))
        # layout.addWidget(static_canvas)

        self.mainLayout.addWidget(self.figure_canvas)

        self.mainLayout.addSpacerItem(QSpacerItem(0, 0, QSizePolicy.Minimum, QSizePolicy.Expanding))

        self.setWidget(self.mainPanel)

        self.updatePlot()

    def updatePlot(self):
        index = self.selection.currentIndex() + 1 # add 1 because no monochromatic entry
        distro = distributions.get_distribution(SpectralDistributionSpecification(index))

        self.figure.clf()
        axes = self.figure.gca()

        axes.scatter(distro.wavelengths, distro.intensities)

        axes.set_xlabel("Wavelength")
        axes.set_ylabel("Intensity")


        self.figure.tight_layout()


        self.figure.canvas.draw()

    def onAnythingChanged(self):
        pass

    def onSelection(self):
        self.updatePlot()

    def new(self):
        """ Make a new entry, based on the currently selected one"""
        pass

    def edit(self):
        pass

    def delete(self):
        pass