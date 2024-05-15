from PySide6.QtWidgets import QTreeWidgetItem

from components.element import Element


class ElementLibraryEntry(QTreeWidgetItem):
    def __init__(self, cls: type[Element]):

        self.cls = cls
        super().__init__([cls.library_name(), cls.library_description()])

    def create(self):
        return self.cls()

