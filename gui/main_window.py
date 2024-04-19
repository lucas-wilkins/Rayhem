import sys
from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtOpenGLWidgets import QOpenGLWidget
from PySide6.QtGui import Qt


from gui.tree import ElementsTree
from gui.properties import Properties

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__(None)

        self.setWindowTitle("Optics Simulator")

        # Main GUI Components
        self.elementsTree = ElementsTree(self)
        self.properties = Properties(self)
        self.glWidget = QOpenGLWidget(self)


        self.setCentralWidget(self.glWidget)
        self.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, self.elementsTree)
        self.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, self.properties)

        # Make full screen
        self.showMaximized()


def run_gui():
    app = QApplication([])

    window = MainWindow()

    window.show()

    sys.exit(app.exec())



if __name__ == "__main__":
    run_gui()