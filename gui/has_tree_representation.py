from PySide6.QtWidgets import QTreeWidgetItem
from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout

from gui.rendering.has_main_window_representation import HasMainWindowRepresentation

class ElementTreeItem(QTreeWidgetItem, HasMainWindowRepresentation):

    def __init__(self, name: str | None):
        self.debug_name = "<unnamed>" if name is None else name

        super().__init__([self.debug_name])

        print("Creating", name)

    def settingsWidget(self):
        widget = QWidget()
        label = QLabel(self.debug_name)
        layout = QVBoxLayout()

        layout.addWidget(label)

        widget.setLayout(layout)

        return widget
