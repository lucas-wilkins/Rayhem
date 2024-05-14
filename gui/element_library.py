from PySide6.QtWidgets import QDockWidget, QTreeWidget, QAbstractItemView, QTreeWidgetItem, QStyle
from PySide6.QtGui import Qt

from components.element import ElementTreeItem
from loadsave import DeserialisationError

class ElementLibraryGroup(QTreeWidgetItem):
    def __init__(self, name: str):
        super().__init__([name])

        self.name = name


class ElementLibrary(QDockWidget):
    def __init__(self, parent):
        super().__init__(parent)

        self.parent = parent

        self.setAllowedAreas(Qt.DockWidgetArea.LeftDockWidgetArea | Qt.DockWidgetArea.RightDockWidgetArea)
        self.setWindowTitle("Elements")

        self.tree = QTreeWidget()
        self.tree.setHeaderHidden(True)

        self.sources = ElementLibraryGroup("Sources")
        self.lenses = ElementLibraryGroup("Lenses")
        self.mirrors = ElementLibraryGroup("Mirrors")
        self.detectors = ElementLibraryGroup("Detectors")
        self.other = ElementLibraryGroup("Other")

        self.tree.insertTopLevelItem(0, self.sources)
        self.tree.insertTopLevelItem(1, self.lenses)
        self.tree.insertTopLevelItem(2, self.mirrors)
        self.tree.insertTopLevelItem(3, self.detectors)
        self.tree.insertTopLevelItem(4, self.other)

        self.tree.setSelectionBehavior(QAbstractItemView.SelectItems)
        self.tree.selectionModel().selectionChanged.connect(self.onSelected)


        self.setWidget(self.tree)



    def onAnythingChanged(self):
        self.parent.onAnythingChanged()

    def onSelected(self):
        # Should only be one item
        for item in self.tree.selectedItems():
            self.parent.properties.setWidget(item.settingsWidget())

    def selectRoot(self):
        self.parent.properties.setWidget(self.sceneTreeRoot.settingsWidget())


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
