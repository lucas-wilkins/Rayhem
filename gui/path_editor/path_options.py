from PySide6.QtCore import Signal
from PySide6.QtWidgets import QWidget, QPushButton, QComboBox, QHBoxLayout


class PathOptionsWidget(QWidget):
    """ Panel for showing options"""

    newPathRequested = Signal()
    pathChanged = Signal()

    def __init__(self, parent=None, pathLibrary=None):
        super().__init__(parent)

        layout = QHBoxLayout()
        self.setLayout(layout)

        path_choice = QComboBox()
        path_choice.addItem("Fully Connected")

        if pathLibrary is not None:
            pass # TODO: Path library contents list here

        new_path = QPushButton("New")

        layout.addWidget(path_choice)
        layout.addWidget(new_path)
