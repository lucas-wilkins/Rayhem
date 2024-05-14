from PySide6.QtWidgets import QWidget

from components.component import Component
from gui.element_tree_item import ElementTreeItem

class Element(ElementTreeItem):

    def __init__(self, parentTree, name: str = "Element"):
        super(ElementTreeItem, self).__init__(parentTree)



    def components(self) -> list[Component]:
        raise NotImplementedError(f"components not implemented for {self.__class__}")

    @staticmethod
    def material_surface_selection() -> QWidget:
        pass
