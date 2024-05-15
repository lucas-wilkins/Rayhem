from PySide6.QtWidgets import QWidget
from PySide6.QtCore import Qt

from components.component import Component
from gui.element_tree_item import ElementTreeItem


class Element(ElementTreeItem):

    def __init__(self):
        super().__init__(self.library_name())
        self.setFlags(self.flags() ^ Qt.ItemIsDropEnabled)


    @staticmethod
    def library_name() -> str:
        """ Name to use in the library """

    @staticmethod
    def library_description() -> str:
        """ Description to use in the library"""

    @staticmethod
    def docs() -> str:
        """ Docs to show when help is requested """

    def components(self) -> list[Component]:
        raise NotImplementedError(f"components not implemented for {self.__class__}")

    @staticmethod
    def material_surface_selection() -> QWidget:
        pass
