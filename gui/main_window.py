import os
import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QFileDialog, QMessageBox
from PySide6.QtGui import Qt, QKeySequence

from gui import appearance
from gui.element_library import ElementLibrary

from gui.element_tree import ElementTree
from gui.element_tree_item import ElementTreeItem
from gui.properties import Properties
from gui.path_editor.path_editor import PathEditor
from gui.rendering.GL.scene import Scene

import json
import logging

from gui.rendering.tree_rendering import TreeRenderer

from media import icons

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__(None)

        # Main window appearance
        self.setWindowIcon(icons.transform)

        # Main GUI Components
        self.elementsTree = ElementTree(self)
        self.properties = Properties(self)

        self.library = ElementLibrary(self)
        self.path_editor = PathEditor(self)

        self.glWidget = Scene(self)


        self.setCentralWidget(self.glWidget)
        self.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, self.library)
        self.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, self.elementsTree)
        self.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, self.properties)

        self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, self.path_editor)

        #
        # Menus
        #

        menu = self.menuBar()

        # File Menu

        menu_file = menu.addMenu("&File")

        file_new = menu_file.addAction("&New")
        file_new.triggered.connect(self.onNew)

        file_load = menu_file.addAction("&Load")
        file_load.triggered.connect(self.onLoad)

        menu_file.addSeparator()

        file_save = menu_file.addAction("&Save")
        file_save.setShortcut(QKeySequence("Ctrl+s"))
        file_save.triggered.connect(self.onSave)

        file_save_as = menu_file.addAction("Save As")
        file_save_as.triggered.connect(self.onSaveAs)

        window_menu = menu.addMenu("&View")

        window_menu.addAction("Scene Tree")
        window_menu.addAction("Properties")
        window_menu.addAction("Component Library")
        window_menu.addAction("Material Library")
        window_menu.addAction("Paths")



        self._loaded_file: str | None = None
        self._changes_made = False

        self.updateTitle() # Has to have _loaded_file and _changes_made defined to work

        # Set up rendering links
        self.glWidget.add(TreeRenderer(self.elementsTree))


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
        display_name = "" if self._loaded_file is None else f" [{self._loaded_file}]"
        star = " *" if self._changes_made else ""

        title_string = appearance.program_name + display_name + star


        self.setWindowTitle(title_string)

    def updateEverything(self):
        self.glWidget.update()
        # self.elementsTree
        self.updateTitle()

    def onAnythingChanged(self):
        """ Called when there has been a change to anything at all"""
        self._changes_made = True
        self.updateEverything()

    def onNew(self):
        if self._changes_made:
            msgBox = QMessageBox()
            msgBox.setText("The simulation has been modified.")
            msgBox.setInformativeText("Do you want to save your changes?")
            msgBox.setStandardButtons(QMessageBox.Save | QMessageBox.Discard | QMessageBox.Cancel)
            msgBox.setDefaultButton(QMessageBox.Save)
            ret = msgBox.exec()

            if ret == QMessageBox.Save:
                if self.onSave():
                    self.new()
                else:
                    return

            elif ret == QMessageBox.Discard:
                self.new()

            elif ret == QMessageBox.Cancel:
                return

            else:
                raise RuntimeError("Oh dear! This has never happened to me before!")

        else:
            self.new()

    def onSave(self) -> bool:
        if self._loaded_file is None:
            return self.onSaveAs()
        else:
            self.save(self._loaded_file)
            return True

    def onSaveAs(self) -> bool:
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
            return False

        else:
            self.save(filename)
            return True

    def new(self):
        self.load("new_template.ray", forget_origin=True)


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
            self.updateEverything()

        except Exception as e:
            log = logging.getLogger(self.__class__.__name__)
            log.error(f"Failed to write to {filename}")
            log.exception(e)


    def load(self, filename: str, forget_origin: bool=False):
        """ Load the program state

        :param forget_origin: load, but forget where the data came from (makes new files configurable easily)
        """

        try:
            with open(filename, 'r') as fid:
                data = json.load(fid)

                self.elementsTree.deserialise(data["scene"])

            self._loaded_file = None if forget_origin else filename
            self._changes_made = False
            self.updateEverything()

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