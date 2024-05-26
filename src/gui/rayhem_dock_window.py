from PySide6.QtGui import QCloseEvent
from PySide6.QtWidgets import QDockWidget

class RayhemDockWidget(QDockWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

    def closeEvent(self, event: QCloseEvent):
        self.setVisible(False)
        self.parent().updateMenus()
        event.ignore()

