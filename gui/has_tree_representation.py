from PySide6.QtWidgets import QTreeWidgetItem
from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout

from gui.rendering.has_main_window_representation import HasMainWindowRepresentation
from loadsave import Serialisable


class ElementTreeItem(Serialisable, QTreeWidgetItem, HasMainWindowRepresentation):

    def __init__(self, name: str | None):

        self._parentTree = None # It's going to be very easy to forget to set this

        self.debug_name = "<unnamed>" if name is None else name
        super().__init__([self.debug_name])

    @property
    def parentTree(self):
        if self._parentTree is None:

            # What's the right exception for this?
            raise AttributeError(f"Element {self.name} does not have a parentTree set")

        return self._parentTree

    @parentTree.setter
    def parentTree(self, parentTree: "ElementsTree"):
        self._parentTree = parentTree

    def onAnythingChanged(self):
        """ Notification that something has changed somewhere"""
        self.parentTree.onAnythingChanged()

    @property
    def children(self) -> list["ElementTreeItem"]:
        """ Children of this object """
        return [self.child(i) for i in range(self.childCount())]

    def settingsWidget(self):
        widget = QWidget()
        label = QLabel(self.debug_name)
        layout = QVBoxLayout()

        layout.addWidget(label)

        widget.setLayout(layout)

        return widget
