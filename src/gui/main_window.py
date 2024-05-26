import os
import sys

import json
import logging

from PySide6.QtWidgets import QApplication, QMainWindow, QFileDialog, QMessageBox
from PySide6.QtGui import Qt, QKeySequence, QStyleHints

from gui import appearance
from gui.element_library import ElementLibrary
from gui.element_tree import ElementTree
from gui.material_library import MaterialLibrary
from gui.properties import Properties
from gui.path_editor.path_editor import PathEditor
from gui.rendering.GL.scene import Scene
from gui.rendering.tree_rendering import TreeRenderer
from gui.spectral_sampling import SpectralSamplingWindow
from media.icons import icons
from spectral_sampling.spectral_distribution_singleton import distributions


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__(None)

        # Main window appearance
        self.setWindowIcon(icons["logo"])

        # Main GUI Components
        # Create
        self.library = ElementLibrary(self)
        self.element_tree = ElementTree(self)
        self.properties = Properties(self)

        self.spectral_distributions = SpectralSamplingWindow(self)
        self.material_library = MaterialLibrary(self)
        self.path_editor = PathEditor(self)

        # Central display
        self.glWidget = Scene(self)
        self.setCentralWidget(self.glWidget)

        # Dock widgets
        self.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, self.library)
        self.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, self.element_tree)
        self.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, self.properties)

        self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, self.spectral_distributions)
        self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, self.material_library)
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

        self.window_menu_element_tree = window_menu.addAction("Scene Tree")
        self.window_menu_element_tree.setCheckable(True)
        self.window_menu_element_tree.triggered.connect(self.toggle_element_tree)

        self.window_menu_properties = window_menu.addAction("Properties")
        self.window_menu_properties.setCheckable(True)
        self.window_menu_properties.triggered.connect(self.toggle_properties)

        self.window_menu_library = window_menu.addAction("Component Library")
        self.window_menu_library.setCheckable(True)
        self.window_menu_library.triggered.connect(self.toggle_element_library)

        self.window_menu_materials = window_menu.addAction("Material Library")
        self.window_menu_materials.setCheckable(True)
        self.window_menu_materials.triggered.connect(self.toggle_materials)

        self.window_menu_spectra = window_menu.addAction("Spectral Sampling")
        self.window_menu_spectra.setCheckable(True)
        self.window_menu_spectra.triggered.connect(self.toggle_spectra)

        self.window_menu_paths = window_menu.addAction("Paths")
        self.window_menu_paths.setCheckable(True)
        self.window_menu_paths.triggered.connect(self.toggle_paths)


        # Current file stuff
        self._loaded_file: str | None = None
        self._changes_made = False
        self.updateTitle() # Has to have _loaded_file and _changes_made defined to work

        # Set up rendering links
        self.glWidget.add(TreeRenderer(self.element_tree))

        # Make full screen
        self.showMaximized()

        # hide RHS docks
        self.spectral_distributions.setVisible(False)
        self.material_library.setVisible(False)
        self.path_editor.setVisible(False)

        # Set up menu checkmarks
        self.update_window_check_states()

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

    def updateMenus(self):
        """ Called when something in the gui, not the simulation has changed"""
        self.update_window_check_states()

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
            "scene": self.element_tree.serialise(),
            "spectral_distributions": distributions.serialise()
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

                distributions.deserialise(data["spectral_distributions"])
                self.element_tree.deserialise(data["scene"])

            self._loaded_file = None if forget_origin else filename
            self._changes_made = False
            self.updateEverything()

        except Exception as e:
            log = logging.getLogger(self.__class__.__name__)
            log.error(f"Failed to load file '{filename}'")
            log.exception(e)

    def update_window_check_states(self):
        """ Update the window check states"""
        self.window_menu_library.setChecked(self.library.isVisible())
        self.window_menu_element_tree.setChecked(self.element_tree.isVisible())
        self.window_menu_properties.setChecked(self.properties.isVisible())

        self.window_menu_paths.setChecked(self.path_editor.isVisible())
        self.window_menu_spectra.setChecked(self.spectral_distributions.isVisible())
        self.window_menu_materials.setChecked(self.material_library.isVisible())

    def toggle_element_tree(self):

        self.element_tree.setVisible(not self.element_tree.isVisible())
        self.update_window_check_states()

    def toggle_element_library(self):
        self.library.setVisible(not self.library.isVisible())
        self.update_window_check_states()


    def toggle_properties(self):
        self.properties.setVisible(not self.properties.isVisible())
        self.update_window_check_states()


    def toggle_paths(self):
        self.path_editor.setVisible(not self.path_editor.isVisible())
        self.update_window_check_states()

    def toggle_spectra(self):
        self.spectral_distributions.setVisible(not self.spectral_distributions.isVisible())
        self.update_window_check_states()

    def toggle_materials(self):
        self.material_library.setVisible(not self.material_library.isVisible())
        self.update_window_check_states()