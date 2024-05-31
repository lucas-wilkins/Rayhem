import sys
from PySide6.QtWidgets import QApplication

import numpy as np

from elements.generic_interface import GenericInterface
from elements.materials.reflecting.ideal_mirror import IdealMirror
from elements.sources.point import PointSource
from elements.sources.single_ray import SingleRay
from elements.transformation import Transformation
from gui.main_window import MainWindow


app = QApplication([])
window = MainWindow()

# For the moment, the new_template is just the normal initial state
window.save("new_template.ray")

# Transformation tree test data
testNode1 = Transformation()
testNode2 = Transformation()
testNode3 = Transformation()

testNode21 = Transformation()
testNode22 = Transformation()

window.element_tree.sceneTreeRoot.addChild(testNode1)
window.element_tree.sceneTreeRoot.addChild(testNode2)
window.element_tree.sceneTreeRoot.addChild(testNode3)

testNode2.addChild(testNode21)
testNode2.addChild(testNode22)

window.save("transform_test.ray")

# Create point source and mirror test file

window.new()

mirror = GenericInterface()
point_source = PointSource()

transform = Transformation()
transform.parentTree = window.element_tree
transform.translation = np.array([0, 0, -2], dtype=float)
transform.addChild(mirror)

window.element_tree.sceneTreeRoot.addChild(transform)
window.element_tree.sceneTreeRoot.addChild(point_source)

window.save("point_source_mirror.ray")

# Multi-element

window.new()

mirror = GenericInterface()


transform = Transformation()
transform.parentTree = window.element_tree
transform.translation = np.array([0, 0, 3], dtype=float)
transform.axis = np.array([0,1,0], dtype=float)
transform.angle_deg = 45
transform.addChild(mirror)

window.element_tree.sceneTreeRoot.addChild(transform)
window.element_tree.sceneTreeRoot.addChild(SingleRay())

window.save("mirror_system.ray")


#
window.new()

window.show()

sys.exit(app.exec())