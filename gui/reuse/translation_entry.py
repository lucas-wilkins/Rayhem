from typing import Sequence

import numpy as np

from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel
from PySide6.QtCore import Signal

from gui.reuse.spinboxes import SpatialSpinBox


class TranslationEntry(QWidget):
    """ GUI element representing a 3D translation"""

    valueChanged = Signal()
    def __init__(self, parent=None, initial_value: Sequence[float] | None = None):
        super().__init__(parent)

        self.labels = QWidget()
        self.boxes = QWidget()

        self.main_layout = QVBoxLayout()
        self.labels_layout = QHBoxLayout()
        self.boxes_layout = QHBoxLayout()

        self.setLayout(self.main_layout)
        self.labels.setLayout(self.labels_layout)
        self.boxes.setLayout(self.boxes_layout)

        self.tx = SpatialSpinBox()
        self.ty = SpatialSpinBox()
        self.tz = SpatialSpinBox()

        self.tx.setValue(initial_value[0])
        self.ty.setValue(initial_value[1])
        self.tz.setValue(initial_value[2])

        self.labels_layout.addWidget(QLabel("X"))
        self.labels_layout.addWidget(QLabel("Y"))
        self.labels_layout.addWidget(QLabel("Z"))

        self.boxes_layout.addWidget(self.tx)
        self.boxes_layout.addWidget(self.ty)
        self.boxes_layout.addWidget(self.tz)

        self.main_layout.addWidget(self.labels)
        self.main_layout.addWidget(self.boxes)

        self.tx.valueChanged.connect(self.onValueChanged)
        self.ty.valueChanged.connect(self.onValueChanged)
        self.tz.valueChanged.connect(self.onValueChanged)

    @property
    def value(self):
        return np.array([self.tx.value(), self.ty.value(), self.tz.value()])

    def onValueChanged(self):
        self.valueChanged.emit()