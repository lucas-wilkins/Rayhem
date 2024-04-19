from PySide6.QtWidgets import QDockWidget, QLabel
from PySide6.QtGui import Qt

class ElementsTree(QDockWidget):
    def __init__(self, parent):
        super().__init__(parent)

        self.setAllowedAreas(Qt.DockWidgetArea.LeftDockWidgetArea | Qt.DockWidgetArea.RightDockWidgetArea)
        self.setWindowTitle("Elements")

        self.setWidget(QLabel("Test Widget"))