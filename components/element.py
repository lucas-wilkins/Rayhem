from PySide6.QtWidgets import QWidget

from components.component import Component
from gui.has_tree_representation import ElementTreeItem

class Element(ElementTreeItem):

    def __init__(self, name: str = "Element"):
        super(ElementTreeItem, self).__init__()

        self.component_id = 0

    def update_component_id(self):
        pass

    def components(self) -> list[Component]:
        raise NotImplementedError(f"components not implemented for {self.__class__}")

    @staticmethod
    def material_surface_selection() -> QWidget:
        pass
