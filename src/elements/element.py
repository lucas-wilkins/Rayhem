from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QWidget
from PySide6.QtCore import Qt

from gui.element_tree_item import ElementTreeItem


class Element(ElementTreeItem):

    def __init__(self):
        super().__init__(self.library_name())
        self.setFlags(self.flags() & ~Qt.ItemIsDropEnabled)

        icon = self.library_icon()
        if icon is not None:
            self.setIcon(0, icon)


    @staticmethod
    def library_name() -> str:
        """ Name to use in the library """

    @staticmethod
    def library_description() -> str:
        """ Description to use in the library"""

    @staticmethod
    def library_icon() -> QIcon | None:
        """ Icon to show in the library """
        return None

    @staticmethod
    def docs() -> str:
        """ Docs to show when help is requested """


    def __repr__(self):
        return self.__class__.__name__