from PySide6.QtWidgets import QWidget

class HasTreeRepresentation:
    def gui_tree_representation(self) -> QWidget:
        raise NotImplementedError(f"gui_tree_representation not implemented for {self.__class__}")