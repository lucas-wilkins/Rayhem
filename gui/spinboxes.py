""" Nicely bounded spin boxes for certain data"""
from PySide6.QtWidgets import QDoubleSpinBox


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

