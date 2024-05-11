from PySide6.QtWidgets import QDockWidget, QTreeWidget, QAbstractItemView
from PySide6.QtGui import Qt

from gui.scene_tree_base import SceneTreeBase
from components.transformation import Transformation


class ElementsTree(QDockWidget):
    def __init__(self, parent):
        super().__init__(parent)

        self.parent = parent

        self.setAllowedAreas(Qt.DockWidgetArea.LeftDockWidgetArea | Qt.DockWidgetArea.RightDockWidgetArea)
        self.setWindowTitle("Elements")

        self.tree = QTreeWidget()
        self.sceneTreeBase = SceneTreeBase()

        self.testNode1 = Transformation()
        self.testNode2 = Transformation()
        self.testNode3 = Transformation()

        self.testNode21 = Transformation()
        self.testNode22 = Transformation()


        self.tree.insertTopLevelItem(0, self.sceneTreeBase)

        self.sceneTreeBase.addChild(self.testNode1)
        self.sceneTreeBase.addChild(self.testNode2)
        self.sceneTreeBase.addChild(self.testNode3)

        self.testNode2.addChild(self.testNode21)
        self.testNode2.addChild(self.testNode22)

        self.tree.setSelectionBehavior(QAbstractItemView.SelectItems)
        self.tree.selectionModel().selectionChanged.connect(self.onSelected)


        self.setWidget(self.tree)

    def onSelected(self):
        # Should only be one item
        for item in self.tree.selectedItems():
            self.parent.properties.setWidget(item.settingsWidget())