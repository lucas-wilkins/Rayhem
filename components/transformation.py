import numpy as np

from gui.axis_entry import AxisEntry
from gui.has_gui_element import HasGuiElement
from gui.has_tree_representation import ElementTreeItem
from loadsave import SerialisableElement, DeserialisationError

from components.ids import unique_id

from scipy.spatial.transform import Rotation

from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QDoubleSpinBox, QCheckBox

class Transformation(SerialisableElement, HasGuiElement, ElementTreeItem):
    """ Translation used to specify the location of things"""

    def __init__(self, angle: float | None = None, axis: np.ndarray | None = None, translation: np.ndarray | None = None):
        self.debug_id = unique_id()

        ElementTreeItem.__init__(self, f"Transformation {self.debug_id}")

        self._angle = 0.0 if angle is None else angle
        self._axis = np.array([0.0, 0.0, 1.0]) if axis is None else axis
        self._translation = np.zeros((3,)) if translation is None else translation

        self.rotation = np.eye(3)
        self.inv_rotation = np.eye(3)

        self.visible = False # Show on GL window?

        self._update_matrices()

    def serialise(self):
        return {
            "rotation": {
                "angle": self._angle,
                "x": self._axis[0],
                "y": self._axis[1],
                "z": self._axis[2],
            },
            "translation": {
                "x": self._translation[0],
                "y": self._translation[1],
                "z": self._translation[2]
            }
        }

    @staticmethod
    def deserialise(data: dict):
        try:
            rotation = data["rotation"]
            translation = data["translation"]

            angle = float(rotation["angle"])
            axis = [float(rotation["x"]), float(rotation["y"]), float(rotation["z"])]

            xyz = [float(translation["x"]), float(translation["y"]), float(translation["z"])]

            return Transformation(angle, np.array(axis), np.array(xyz))

        except KeyError as e:
            raise DeserialisationError(f"Failed to deserialise: {data} - {e}")

    @property
    def angle(self):
        return self._angle

    @angle.setter
    def angle(self, angle):
        self._angle = angle
        self._update_matrices()

    @property
    def axis(self):
        return self._axis

    @axis.setter
    def axis(self, axis):
        self._axis = axis
        self._update_matrices()

    @property
    def translation(self):
        return self._translation

    @translation.setter
    def translation(self, translation):
        self._translation = translation


    def _update_matrices(self):
        r = Rotation.from_rotvec(self._angle * self._axis)
        self.rotation = r.as_matrix()
        self.inv_rotation = r.inv().as_matrix()

    def forward_point_transform(self, points: np.ndarray):
        """ Transform points from local frame to parent frame"""
        rotated = np.dot(points, self.rotation)
        return rotated + self.translation

    def reverse_point_transform(self, points: np.ndarray):
        """ Transform points from parent frame to local frame"""
        translated = points - self.translation
        return np.dot(translated, self.inv_rotation)

    def forward_direction_transform(self, directions: np.ndarray):
        """ Transform directions from local frame to parent frame"""
        return np.dot(directions, self.rotation)

    def reverse_direction_transform(self, directions: np.ndarray):
        """ Transform directions from parent frame to local frame"""
        return np.dot(directions, self.inv_rotation)

    def __repr__(self):
        return f"Transformation[{self.debug_id}]"

    def settingsWidget(self):

        main_widget = QWidget()
        main_layout = QVBoxLayout()
        main_widget.setLayout(main_layout)

        #
        # Rotation
        #

        angle_widget = QWidget()
        angle_layout = QHBoxLayout()
        angle_widget.setLayout(angle_layout)

        angle_label = QLabel("Angle")
        angle = QDoubleSpinBox()
        angle.setValue(self._angle)

        angle_layout.addWidget(angle_label)
        angle_layout.addWidget(angle)

        axis_widget = AxisEntry(initial_value=self.axis)

        main_layout.addWidget(QLabel("Rotation:"))
        main_layout.addWidget(angle_widget)
        main_layout.addWidget(axis_widget)

        #
        # Translation
        #

        translation_main_widget = QWidget()
        translation_labels = QWidget()
        translation_boxes = QWidget()

        translation_main_layout = QVBoxLayout()
        translation_labels_layout = QHBoxLayout()
        translation_boxes_layout = QHBoxLayout()

        translation_main_widget.setLayout(translation_main_layout)
        translation_labels.setLayout(translation_labels_layout)
        translation_boxes.setLayout(translation_boxes_layout)

        tx = QDoubleSpinBox()
        ty = QDoubleSpinBox()
        tz = QDoubleSpinBox()

        tx.setValue(self._translation[0])
        ty.setValue(self._translation[1])
        tz.setValue(self._translation[2])

        translation_labels_layout.addWidget(QLabel("X"))
        translation_labels_layout.addWidget(QLabel("Y"))
        translation_labels_layout.addWidget(QLabel("Z"))

        translation_boxes_layout.addWidget(tx)
        translation_boxes_layout.addWidget(ty)
        translation_boxes_layout.addWidget(tz)

        translation_main_layout.addWidget(translation_labels)
        translation_main_layout.addWidget(translation_boxes)

        main_layout.addWidget(QLabel("Translation:"))
        main_layout.addWidget(translation_main_widget)

        # Rendering options
        do_render = QCheckBox("Show Axes")
        do_render.setChecked(self.visible)

        main_layout.addWidget(do_render)


        # Return the main widget

        return main_widget
