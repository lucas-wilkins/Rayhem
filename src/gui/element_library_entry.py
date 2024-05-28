from PySide6.QtWidgets import QTreeWidgetItem

from elements.element import Element


class ElementLibraryEntry(QTreeWidgetItem):
    def __init__(self, cls: type[Element]):

        self.cls = cls
        super().__init__([cls.library_name(), cls.library_description()])
        self.setIcon(0, cls.library_icon())

    def create(self):
        return self.cls()

