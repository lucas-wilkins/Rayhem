from PySide6.QtWidgets import QDockWidget, QTreeWidget, QAbstractItemView
from PySide6.QtGui import Qt
from PySide6 import QtCore

from gui.element_tree_root import ElementTreeRoot
from components.transformation import Transformation
from components.element import ElementTreeItem
from loadsave import DeserialisationError

# Lookup for deserialisation
_class_lookup: dict[str, type[ElementTreeItem]] = {cls.serialisation_name(): cls for cls in [ElementTreeRoot, Transformation]}

class ElementTree(QDockWidget):
    def __init__(self, parent):
        super().__init__(parent)

        self.parent = parent

        self.setAllowedAreas(Qt.DockWidgetArea.LeftDockWidgetArea | Qt.DockWidgetArea.RightDockWidgetArea)
        self.setWindowTitle("Elements")

        self.tree = QTreeWidget()
        self.tree.setHeaderHidden(True)
        self.tree.setDragDropMode(QAbstractItemView.InternalMove)
        self.tree.setDragEnabled(True)
        self.tree.setAcceptDrops(True)
        self.tree.setDropIndicatorShown(True)

        # TODO update scene on drag
        # self.tree.model().dataChanged.connect(self.onChangeStructure)
        # self.tree.model().layoutChanged.connect(self.onChangeStructure)

        self.sceneTreeRoot = ElementTreeRoot()

        self.tree.insertTopLevelItem(0, self.sceneTreeRoot)

        self.tree.setSelectionBehavior(QAbstractItemView.SelectItems)
        self.tree.selectionModel().selectionChanged.connect(self.onSelected)

        self.setWidget(self.tree)

    def onChangeStructure(self):
        print("Structure changed")
        self.onAnythingChanged()

    def onAnythingChanged(self):
        self.parent.onAnythingChanged()

    def onSelected(self):
        # Should only be one item
        for item in self.tree.selectedItems():
            self.parent.properties.setWidget(item.settingsWidget())

    def _selected_draggable(self):
        """ Get selected item, if nothing is selected return root """
        return_item = self.sceneTreeRoot
        for item in self.tree.selectedItems():
            if item.flags() & QtCore.Qt.ItemIsDragEnabled:
                return_item = item

        return return_item

    def selectRoot(self):
        self.parent.properties.setWidget(self.sceneTreeRoot.settingsWidget())

    def addElement(self, element: ElementTreeItem):
        self._selected_draggable().addChild(element)

        self.onAnythingChanged()

    def deserialise(self, data: dict):
        # Traverse the tree
        new_tree = self._deserialise(data)

        self.sceneTreeRoot = new_tree
        self.tree.clear()
        self.tree.insertTopLevelItem(0, new_tree)

        self.selectRoot()
        self.tree.expandAll()


    def _deserialise(self, data: dict):
        name = data["class"]

        if name in _class_lookup:

            try:
                obj_data = data["data"]


                obj = _class_lookup[name].deserialise(obj_data)

                children = data["children"]

                for child in children:

                    element = self._deserialise(child)
                    element.parentTree = self

                    obj.addChild(element)

                return obj

            except KeyError as ke:
                raise DeserialisationError(f"'{ke}' in {data}")

        else:
            raise DeserialisationError(f"Could not find object of matching: {name}")

    def serialise(self):
        # Turn the tree into a nested dict, serialising each element
        return self._serialise(self.sceneTreeRoot)

    def _serialise(self, element: ElementTreeItem):
        return {"class": element.serialisation_name(),
                "data": element.serialise(),
                "children": [self._serialise(child) for child in element.children]}
