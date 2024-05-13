from PySide6.QtWidgets import QTreeWidgetItem

from components.element import ElementTreeItem

class SceneTreeRoot(ElementTreeItem):

    def __init__(self):
        super().__init__("Scene")

    @staticmethod
    def serialisation_name() -> str:
        return "root"

    def serialise(self) -> dict:
        return {}

    @staticmethod
    def deserialise(data) -> "SceneTreeRoot":
        return SceneTreeRoot()

