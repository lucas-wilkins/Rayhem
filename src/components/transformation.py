import numpy as np
from scipy.spatial.transform import Rotation

from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QCheckBox

from OpenGL.GL import glTranslate, glRotate, glPushMatrix, glPopMatrix, glBegin, glEnd, glVertex, glColor
from OpenGL import GL

from components.simulation_data import ComponentAndTransform, SourceAndTransform
from gui.reuse.axis_entry import AxisEntry
from gui.element_tree_item import ElementTreeItem
from gui.reuse.spinboxes import AngleSpinBox
from gui.reuse.translation_entry import TranslationEntry
from loadsave import DeserialisationError
from components.ids import unique_id

from media.icons import icons

_180_over_pi = 180/np.pi
_pi_over_180 = np.pi / 180

class Transformation(ElementTreeItem):
    """ Translation used to specify the location of things"""

    def __init__(self, angle: float | None = None, axis: np.ndarray | None = None, translation: np.ndarray | None = None):
        self.debug_id = unique_id()

        ElementTreeItem.__init__(self,f"Transformation {self.debug_id}")
        self.setIcon(0, icons["transform"])

        self._angle = 0.0 if angle is None else angle
        self._axis = np.array([0.0, 0.0, 1.0]) if axis is None else axis
        self._translation = np.zeros((3,)) if translation is None else translation

        self.rotation = np.eye(3)
        self.inv_rotation = np.eye(3)

        self._visible = False # Show on GL window?

        self._update_matrices()



    @staticmethod
    def serialisation_name() -> str:
        return "transformation"

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

        self.onAnythingChanged()

    @property
    def angle_deg(self):
        return self.angle * _pi_over_180

    @angle_deg.setter
    def angle_deg(self, value):
        self.angle = value * _180_over_pi

    @property
    def axis(self):
        return self._axis

    @axis.setter
    def axis(self, axis):
        self._axis = axis
        self._update_matrices()

        self.onAnythingChanged()

    @property
    def translation(self):
        return self._translation

    @translation.setter
    def translation(self, translation):
        self._translation = translation

        self.onAnythingChanged()


    @property
    def visible(self):
        return self._visible

    @visible.setter
    def visible(self, value: bool):
        self._visible = value

        self.onAnythingChanged()

    def _update_matrices(self):
        r = Rotation.from_rotvec(self._angle * self._axis)
        self.rotation = r.as_matrix()
        self.inv_rotation = r.inv().as_matrix()


    def gl_in(self):

        axis = self.axis
        translation = self.translation

        glPushMatrix()

        glTranslate(translation[0], translation[1], translation[2])
        glRotate(self.angle_deg, axis[0], axis[1], axis[2])

    def gl_out(self):
        glPopMatrix()

    def render(self):
        """ Render: show a representation of the local x,y,z coordinate system """
        if True:# self.visible:

            # X - red
            glBegin(GL.GL_LINES)
            glColor(1,0,0)
            glVertex(0,0,0)
            glVertex(1,0,0)
            glEnd()

            # Y - green
            glBegin(GL.GL_LINES)
            glColor(0, 1, 0)
            glVertex(0, 0, 0)
            glVertex(0, 1, 0)
            glEnd()

            # X - red
            glBegin(GL.GL_LINES)
            glColor(0, 0, 1)
            glVertex(0, 0, 0)
            glVertex(0, 0, 1)
            glEnd()

    def __repr__(self):
        return f"Transformation[{self.debug_id}]"

    def transformed_components(self) -> list[ComponentAndTransform]:
        output = []
        for child_node in self.children:
            for child_component in child_node.transformed_components():
                # Forward, apply rotation to child first, then translation
                rotation = np.dot(self.rotation, child_component.forward_rotation)
                translation = self.translation + np.dot(self.rotation, child_component.forward_translation)

                # Forward, apply inverse translation to child first, then inverse rotation
                inv_rotation = np.dot(child_component.backward_rotation, self.inv_rotation)
                inv_translation = np.dot(child_component.backward_rotation, child_component.backward_translation - self.translation)

                output.append(ComponentAndTransform(child_component.component, rotation, inv_rotation, translation, inv_translation))

        return output

    def transformed_sources(self) -> list[SourceAndTransform]:
        output = []
        for child_node in self.children:
            for child_source in child_node.transformed_sources():
                rotation = np.dot(self.rotation, child_source.forward_rotation)
                translation = self.translation + np.dot(self.rotation, child_source.forward_translation)
                inv_rotation = np.dot(child_source.backward_rotation, self.inv_rotation)
                inv_translation = np.dot(child_source.backward_rotation,
                                         child_source.backward_translation - self.translation)

                output.append(SourceAndTransform(child_source.source, rotation, inv_rotation, translation,
                                                    inv_translation))

        return output

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
        angle = AngleSpinBox()
        angle.setValue(self.angle_deg)

        angle_layout.addWidget(angle_label)
        angle_layout.addWidget(angle)

        axis_widget = AxisEntry(initial_value=self.axis)

        main_layout.addWidget(QLabel("Rotation:"))
        main_layout.addWidget(angle_widget)
        main_layout.addWidget(axis_widget)

        #
        # Translation
        #
        main_layout.addWidget(QLabel("Translation:"))
        translation = TranslationEntry(initial_value=self._translation)
        main_layout.addWidget(translation)

        # Rendering options
        do_render = QCheckBox("Show Axes")
        do_render.setChecked(self.visible)

        main_layout.addWidget(do_render)

        # Callbacks
        def onAngleChanged():
            self.angle_deg = angle.value()

        def onAxisChanged():
            self.axis = axis_widget.value

        def onTranslationChanged():
            self.translation = translation.value

        def onVisibleChanged():
            self.visible = do_render.isChecked()


        angle.valueChanged.connect(onAngleChanged)
        axis_widget.valueChanged.connect(onAxisChanged)
        translation.valueChanged.connect(onTranslationChanged)
        do_render.stateChanged.connect(onVisibleChanged)

        # Return the main widget

        return main_widget
