import os
import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QFileDialog
from PySide6.QtOpenGLWidgets import QOpenGLWidget
from PySide6.QtGui import Qt, QKeySequence

from gui import appearance

from gui.tree import ElementsTree
from gui.properties import Properties
from gui.path_editor.path_editor import PathEditor
from gui.rendering.GL.scene import Scene

import json
import logging

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__(None)

        # Main GUI Components
        self.elementsTree = ElementsTree(self)
        self.properties = Properties(self)
        self.path_editor = PathEditor(self)
        self.glWidget = Scene(self)

        # Show something in the GL renderer - temporary
        from gui.rendering.GL.color import uniform_coloring
        from gui.rendering.GL.icosahedron import Icosahedron
        self.glWidget.add(Icosahedron(edge_colors=uniform_coloring(1, 1, 1), colors=uniform_coloring(0.7, 0, 0.7)))


        self.setCentralWidget(self.glWidget)
        self.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, self.elementsTree)
        self.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, self.properties)

        self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, self.path_editor)

        # Menu

        menu = self.menuBar()

        menu_file = menu.addMenu("&File")
        menu_load = menu_file.addAction("&Load")
        menu_load.triggered.connect(self.onLoad)

        menu_file.addSeparator()
        menu_save = menu_file.addAction("&Save")
        menu_save.setShortcut(QKeySequence("Ctrl+s"))
        menu_save.triggered.connect(self.onSave)

        menu_saveas = menu_file.addAction("Save &As")
        menu_saveas.triggered.connect(self.onSaveAs)

        self._loaded_file: str | None = None
        self._changes_made = False

        self.updateTitle() # Has to have _loaded_file and _changes_made defined to work

        # Make full screen
        self.showMaximized()

    def onLoad(self):

        if self._loaded_file is None:
            open_directory = os.getcwd()
        else:
            open_directory = os.path.dirname(self._loaded_file)

        filename, file_type = QFileDialog.getOpenFileName(
            self,
            "Load Scene",
            open_directory,
            "Ray Simulations (*.ray)")

        if filename == "":
            return

        else:
            self.load(filename)

    def updateTitle(self):
        title_string = appearance.program_name

        if self._loaded_file is not None:
            title_string += f" [{os.path.basename(self._loaded_file)}]"

        if self._changes_made:
            title_string += " *"

        self.setWindowTitle(title_string)

    def onAnythingChanged(self):
        """ Called when there has been a change to anything at all"""
        self._changes_made = True
        self.updateTitle()


    def onSave(self):
        if self._loaded_file is None:
            self.onSaveAs()
        else:
            self.save(self._loaded_file)

    def onSaveAs(self):
        if self._loaded_file is None:
            open_directory = os.getcwd()
        else:
            open_directory = os.path.dirname(self._loaded_file)

        filename, file_type = QFileDialog.getSaveFileName(
            self,
            "Save Scene",
            open_directory,
            "Ray Simulations (*.ray)")

        if filename == "":
            return

        else:
            self.save(filename)


    def save(self, filename: str):
        """ Save the program state"""

        data = {
            "scene": self.elementsTree.serialise()
        }

        try:
            with open(filename, 'w') as fid:
                json.dump(data, fid, indent=2)

            self._loaded_file = filename
            self._changes_made = False
            self.updateTitle()

        except Exception as e:
            log = logging.getLogger(self.__class__.__name__)
            log.error(f"Failed to write to {filename}")
            log.exception(e)


    def load(self, filename: str):
        """ Load the program state"""

        try:
            with open(filename, 'r') as fid:
                data = json.load(fid)

                self.elementsTree.deserialise(data["scene"])

            self._loaded_file = filename
            self._changes_made = False
            self.updateTitle()

        except Exception as e:
            log = logging.getLogger(self.__class__.__name__)
            log.error(f"Failed to load file '{filename}'")
            log.exception(e)

def run_gui():
    app = QApplication([])

    window = MainWindow()

    window.load("test.ray")

    window.show()

    sys.exit(app.exec())



if __name__ == "__main__":
    run_gui()