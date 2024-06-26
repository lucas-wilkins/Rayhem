from PySide6.QtWidgets import QDockWidget, QTreeWidget, QAbstractItemView, QTreeWidgetItem, QWidget, \
    QVBoxLayout, QPushButton, QHBoxLayout
from PySide6.QtGui import Qt

from elements.transformation import Transformation
from gui.element_library_entry import ElementLibraryEntry
from gui.rayhem_dock_window import RayhemDockWidget
from media.icons import icons


class ElementLibraryGroup(QTreeWidgetItem):
    def __init__(self, name: str):
        super().__init__([name, ""])

        self.name = name

class TransformEntry(ElementLibraryEntry):
    def __init__(self):

        QTreeWidgetItem.__init__(self, ["Transformation", "Rotates and translates child elements"])
        self.setIcon(0, icons["transform"])

    def create(self):
        return Transformation()


class ElementLibrary(RayhemDockWidget):
    def __init__(self, parent):
        super().__init__(parent)

        # self.parent = parent

        self.setAllowedAreas(Qt.DockWidgetArea.LeftDockWidgetArea | Qt.DockWidgetArea.RightDockWidgetArea)
        self.setWindowTitle("Elements")

        self.main_panel = QWidget()
        layout = QVBoxLayout()
        self.main_panel.setLayout(layout)

        self.tree = QTreeWidget()
        self.tree.setHeaderHidden(True)

        self.sources = ElementLibraryGroup("Sources")
        self.lenses = ElementLibraryGroup("Lenses")
        self.mirrors = ElementLibraryGroup("Mirrors")
        self.chromatic = ElementLibraryGroup("Chromatic")
        self.detectors = ElementLibraryGroup("Detectors")
        self.other = ElementLibraryGroup("Other")

        self.tree.insertTopLevelItem(0, TransformEntry())

        self.tree.insertTopLevelItem(1, self.sources)
        self.tree.insertTopLevelItem(2, self.lenses)
        self.tree.insertTopLevelItem(3, self.mirrors)
        self.tree.insertTopLevelItem(4, self.detectors)
        self.tree.insertTopLevelItem(5, self.other)

        self.tree.setSelectionBehavior(QAbstractItemView.SelectItems)
        self.tree.selectionModel().selectionChanged.connect(self.onSelected)
        self.tree.setColumnHidden(1, False)

        layout.addWidget(self.tree)

        # Buttons

        self.button_panel = QWidget()
        button_layout = QHBoxLayout()
        self.button_panel.setLayout(button_layout)

        self.add_button = QPushButton("Add")
        self.add_button.clicked.connect(self.onAdd)

        self.about_button = QPushButton("Details")
        self.about_button.clicked.connect(self.onAbout)

        button_layout.addWidget(self.add_button)
        button_layout.addWidget(self.about_button)

        layout.addWidget(self.button_panel)

        # Add to self

        self.setWidget(self.main_panel)

        self.fill_library()

        self.tree.expandAll()

        self._update_button_states()

    def fill_library(self):
        """ Fill the library widget with possibilities """

        # Sources

        from elements.sources.point import PointSource
        from elements.sources.single_ray import SingleRay

        self.sources.addChild(ElementLibraryEntry(PointSource))
        self.sources.addChild(ElementLibraryEntry(SingleRay))

        # Other
        from elements.generic_interface import GenericInterface

        self.other.addChild(ElementLibraryEntry(GenericInterface))



    def onAnythingChanged(self):
        self.parent().onAnythingChanged()


    def onSelected(self):
        # Should only be one item
        self._update_button_states()

    def _update_button_states(self):

        self.add_button.setEnabled(False)
        self.about_button.setEnabled(False)

        for item in self.tree.selectedItems():
            if isinstance(item, ElementLibraryEntry):
                self.add_button.setEnabled(True)
                self.about_button.setEnabled(True)

    def onAdd(self):
        for item in self.tree.selectedItems():
            if isinstance(item, ElementLibraryEntry):
                element = item.create()
                self.parent().element_tree.addElement(element)


    def onAbout(self):
        pass