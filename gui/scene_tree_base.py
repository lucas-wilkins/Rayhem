from PySide6.QtWidgets import QTreeWidgetItem

from components.element import ElementTreeItem

class SceneTreeBase(ElementTreeItem):
    def __init__(self):
        super().__init__("Scene")
