from PySide6.QtWidgets import QWidget

class HasGuiElement:
    def gui_element(self) -> QWidget:
        raise NotImplementedError(f"gui_element not implemented in {self.__class__}")