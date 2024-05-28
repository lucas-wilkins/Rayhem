from PySide6.QtWidgets import QDockWidget, QTreeWidget, QAbstractItemView, QWidget, QVBoxLayout, QSizePolicy, \
    QSpacerItem
from PySide6.QtGui import Qt
from PySide6 import QtCore

from elements.simulation_data import SimulationData
from elements.sources.point import PointSource
from elements.sources.single_ray import SingleRay
from gui.element_tree_root import ElementTreeRoot
from elements.transformation import Transformation
from elements.element import ElementTreeItem
from gui.rayhem_dock_window import RayhemDockWidget
from loadsave import DeserialisationError

# Lookup for deserialisation
_classes = [ElementTreeRoot, Transformation, PointSource, SingleRay]
_class_lookup: dict[str, type[ElementTreeItem]] = {cls.serialisation_name(): cls for cls in _classes}

class ElementTree(RayhemDockWidget):
    def __init__(self, parent):
        super().__init__(parent)

        # self.parent = parent

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
        """ General update """
        self.parent().onAnythingChanged()

    def onSelected(self):
        """ Actions to happen when a new selection is made in the tree"""

        # Should only be one item
        for item in self.tree.selectedItems():
            new_widget = QWidget()
            new_layout = QVBoxLayout()
            new_widget.setLayout(new_layout)

            new_layout.addWidget(item.settingsWidget())
            new_layout.addSpacerItem(QSpacerItem(0,0,QSizePolicy.Minimum, QSizePolicy.Expanding))

            self.parent().properties.setWidget(new_widget)

            return

    def singleSelectedItem(self):
        """ First of multiple selected items"""
        for item in self.tree.selectedItems():
            return item
    def closestBranchNode(self):
        """ Find closest not leaf node to the current selection"""
        item = self.singleSelectedItem()
        if item is None:
            return self.sceneTreeRoot
        else:
            return self._closestBranchNode(item)

    def _closestBranchNode(self, node: ElementTreeItem):
        """ Internal method for finding non-leaf node"""
        if node.flags() & QtCore.Qt.ItemIsDropEnabled:
            return node
        else:
            return self._closestBranchNode(node.parent())

    def selectRoot(self):
        self.parent().properties.setWidget(self.sceneTreeRoot.settingsWidget())

    def addElement(self, element: ElementTreeItem):
        """ Add to the tree """
        self.closestBranchNode().addChild(element)
        element.parentTree = self
        self.onAnythingChanged()

    def simulation_data(self) -> SimulationData:
        """ Gather all components together as a simulation data object """

        sources = self.sceneTreeRoot.transformed_sources()
        components = self.sceneTreeRoot.transformed_interfaces()

        return SimulationData(sources=sources, components=components)

    def deserialise(self, data: dict):
        """ Deserialise tree data and set """

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
