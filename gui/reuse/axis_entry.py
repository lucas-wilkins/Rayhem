from typing import Sequence

import numpy as np

from PySide6.QtWidgets import QWidget, QLabel, QGridLayout
from PySide6.QtCore import Signal

from gui.appearance import error_style, normal_style
from gui.reuse.spinboxes import SpatialSpinBox


class AxisEntry(QWidget):
    """ GUI representation of a rotation axis"""

    valueChanged = Signal()
    def __init__(self, parent=None, initial_value: Sequence[float] | None = None):
        super().__init__(parent)

        layout = QGridLayout()

        layout.addWidget(QLabel("X"), 0, 0)
        layout.addWidget(QLabel("Y"), 1, 0)
        layout.addWidget(QLabel("Z"), 2, 0)

        self.x = SpatialSpinBox()
        self.y = SpatialSpinBox()
        self.z = SpatialSpinBox()

        self.x.setSingleStep(0.01)
        self.y.setSingleStep(0.01)
        self.z.setSingleStep(0.01)

        self.x.valueChanged.connect(self._onSpinMove)
        self.y.valueChanged.connect(self._onSpinMove)
        self.z.valueChanged.connect(self._onSpinMove)

        layout.addWidget(self.x, 0, 1)
        layout.addWidget(self.y, 1, 1)
        layout.addWidget(self.z, 2, 1)

        self.setLayout(layout)

        # Initial state
        if initial_value is None:
            self.z.setValue(1.0)
            self._raw_value = np.array([0,0,1], dtype=float)

        else:
            self._raw_value = np.array(initial_value, dtype=float)
            self.x.setValue(initial_value[0])
            self.y.setValue(initial_value[1])
            self.z.setValue(initial_value[2])

    def _setBad(self):
        self.x.setStyleSheet(error_style)
        self.y.setStyleSheet(error_style)
        self.z.setStyleSheet(error_style)

    def _setGood(self):
        self.x.setStyleSheet(normal_style)
        self.y.setStyleSheet(normal_style)
        self.z.setStyleSheet(normal_style)

    def _onSpinMove(self):
        new_value = np.array([self.x.value(), self.y.value(), self.z.value()])
        norm = np.sum(new_value**2)

        if norm > 0:
            self._raw_value = new_value
            self._setGood()

        else:
            self._setBad()

        self.valueChanged.emit()
    @property
    def value(self):
        norm = np.sqrt(np.sum(self._raw_value**2))
        return self._raw_value / norm

def _test_window():
    from PySide6.QtWidgets import QApplication
    import sys

    app = QApplication([])

    window = AxisEntry(initial_value=[1,1,0])

    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    _test_window()