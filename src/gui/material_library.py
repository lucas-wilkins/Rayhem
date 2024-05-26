from PySide6.QtWidgets import QVBoxLayout, QLabel

from gui.rayhem_dock_window import RayhemDockWidget


class MaterialLibrary(RayhemDockWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        layout = QVBoxLayout()

        layout.addWidget(QLabel("Material Library"))

        self.setLayout(layout)

