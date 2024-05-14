from PySide6.QtWidgets import QTreeWidgetItem, QWidget, QGridLayout, QLabel

from calculation.simulation_parameters import SimulationParameters
from components.element import ElementTreeItem
from gui.path_editor.path_options import PathOptionsWidget
from gui.reuse.spinboxes import MagnitudeSpinBox


class ElementTreeRoot(ElementTreeItem):

    def __init__(self, simulation_parameters: SimulationParameters | None = None):
        super().__init__("Scene")

        self.simulation_parameters = SimulationParameters() if simulation_parameters is None else simulation_parameters

    @staticmethod
    def serialisation_name() -> str:
        return "simulation"

    def serialise(self) -> dict:
        return {"parameters": self.simulation_parameters.serialise()}

    @staticmethod
    def deserialise(data) -> "ElementTreeRoot":
        parameters = SimulationParameters.deserialise(data["parameters"])
        return ElementTreeRoot()

    def settingsWidget(self):
        widget = QWidget()
        layout = QGridLayout()

        layout.addWidget(QLabel("Ray Pathing"), 0, 0)
        layout.addWidget(QLabel("Minimum Travel"), 1, 0)
        layout.addWidget(QLabel("Maximum Rays"), 2, 0)

        layout.addWidget(PathOptionsWidget(), 0, 1) # TODO: change none to path library reference
        layout.addWidget(MagnitudeSpinBox(self.simulation_parameters.minimum_distance, -6, -3), 1, 1)
        layout.addWidget(MagnitudeSpinBox(self.simulation_parameters.maximum_rays, 3, 12), 2, 1)

        widget.setLayout(layout)

        return widget