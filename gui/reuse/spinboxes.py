""" Nicely bounded spin boxes for certain data"""
from PySide6.QtCore import Signal
from PySide6.QtWidgets import QDoubleSpinBox, QWidget, QHBoxLayout, QLabel, QSpinBox

from numpy import log10

class SpatialSpinBox(QDoubleSpinBox):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMaximum(1e12)
        self.setMinimum(-1e12)
        self.setSingleStep(0.1)

class AngleSpinBox(QDoubleSpinBox):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMaximum(1e12)
        self.setMinimum(-1e12)
        self.setSingleStep(1.0)


class MagnitudeSpinBox(QWidget):

    valueChanged = Signal()
    def __init__(self, initial: float, low: float, high: float, parent=None):
        super().__init__(parent)

        layout = QHBoxLayout()
        layout.addWidget(QLabel("10^"))

        self.spinbox = QDoubleSpinBox()
        self.spinbox.setValue(float(log10(initial)))
        self.spinbox.setMinimum(low)
        self.spinbox.setMaximum(high)
        self.spinbox.setSingleStep(1)

        layout.addWidget(self.spinbox)



    def _onValueChanged(self):
        self.valueChanged.emit()
    def value(self):
        return 10.0**self.spinbox.value()

