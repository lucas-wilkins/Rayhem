from PySide6.QtWidgets import QWidget, QGridLayout, QLabel, QCheckBox, QSpinBox

from calculation.simulation_parameters import SimulationParameters
from elements.element import ElementTreeItem
from gui.path_editor.path_options import PathOptionsWidget
from gui.rendering.rendering_parameters import RenderingParameters
from gui.reuse.spinboxes import MagnitudeSpinBox, DistanceSpinBox


class ElementTreeRoot(ElementTreeItem):

    def __init__(self,
                 simulation_parameters: SimulationParameters | None = None,
                 rendering_parameters: RenderingParameters | None = None):

        super().__init__("Scene")

        self.simulation_parameters = SimulationParameters() if simulation_parameters is None else simulation_parameters

        self.rendering_parameters = RenderingParameters() if rendering_parameters is None else rendering_parameters

    @staticmethod
    def serialisation_name() -> str:
        return "simulation"

    def serialise(self) -> dict:
        return {"simulation_parameters": self.simulation_parameters.serialise(),
                "rendering_parameters": self.rendering_parameters.serialise()
                }

    @staticmethod
    def deserialise(data) -> "ElementTreeRoot":
        simulation_parameters = SimulationParameters.deserialise(data["simulation_parameters"])
        rendering_parameters = RenderingParameters.deserialise(data["rendering_parameters"])
        return ElementTreeRoot(simulation_parameters, rendering_parameters)

    def transformed_interfaces(self) -> list["ComponentAndTransform"]:
        return [comp for child in self.children for comp in child.transformed_interfaces()]

    def transformed_sources(self) -> list["SourceAndTransform"]:
        return [comp for child in self.children for comp in child.transformed_sources()]

    def settingsWidget(self):
        widget = QWidget()
        layout = QGridLayout()

        layout.addWidget(QLabel("Ray Pathing"), 0, 0)
        layout.addWidget(QLabel("Minimum Intensity"), 1, 0)
        layout.addWidget(QLabel("Minimum Travel"), 2, 0)
        layout.addWidget(QLabel("Maximum Rays"), 3, 0)
        layout.addWidget(QLabel("Maximum Iterations"), 4, 0)
        layout.addWidget(QLabel("Show Escaped Rays"), 5, 0)
        layout.addWidget(QLabel("Escaped Ray Length"), 6, 0)

        min_distance = MagnitudeSpinBox(self.simulation_parameters.minimum_distance, -6, -3)
        min_intensity = MagnitudeSpinBox(self.simulation_parameters.maximum_rays, 3, 12)
        max_rays = MagnitudeSpinBox(self.simulation_parameters.minimum_intensity, -15, 0)
        max_iters = QSpinBox()

        max_iters.setMinimum(1)
        max_iters.setMaximum(100000)
        max_iters.setValue(self.simulation_parameters.maximum_iterations)

        show_escaped = QCheckBox()
        show_escaped.setChecked(self.rendering_parameters.show_escaped)

        escaped_length = DistanceSpinBox()
        escaped_length.setValue(self.rendering_parameters.escaped_length)

        layout.addWidget(PathOptionsWidget(), 0, 1) # TODO: change none to path library reference
        layout.addWidget(min_intensity, 1, 1)
        layout.addWidget(min_distance, 2, 1)
        layout.addWidget(max_rays, 3, 1)
        layout.addWidget(max_iters, 4, 1)
        layout.addWidget(show_escaped, 5, 1)
        layout.addWidget(escaped_length, 6, 1)

        #TODO Add callbacks

        widget.setLayout(layout)

        return widget