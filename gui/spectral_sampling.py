from PySide6.QtWidgets import QDockWidget, QWidget


class SpectralSamplingWindow(QDockWidget):

    def __init__(self):
        self.mainPanel = QWidget()

    def customDistributionNames(self) -> list[str]:
        return []

    def onAnythingChanged(self):
        pass

    def serialise(self) -> dict:
        pass

    def deserialise(self, data) -> dict:
        pass