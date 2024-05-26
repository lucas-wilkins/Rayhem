from PySide6.QtGui import Qt
from PySide6.QtWidgets import QDockWidget, QLabel, QToolBar

from gui.rayhem_dock_window import RayhemDockWidget


class PathEditor(RayhemDockWidget):
    def __init__(self, parent):
        super().__init__(parent)

        self.setAllowedAreas(Qt.DockWidgetArea.LeftDockWidgetArea | Qt.DockWidgetArea.RightDockWidgetArea)
        self.setWindowTitle("Paths")



        self.setWidget(QLabel("Path Editor"))


class Node:
    pass

class Edge:
    pass