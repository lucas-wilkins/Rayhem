Subsystems
==========

Geometric Structure
-------------------

How things are laid out. What shape are the elements, what are they made of etc

Paths
-----

Paths allow control over the simulation and visualisation, so that we can consider only interactions that
we care about.

Materials
---------

Different materials that can be applied to the interfaces. air to glass, mirror, etc

Captures dispersion and polarisation properties.

Lights
------

Description of the light produced by the various sources, spectra, polarisation, etc.


Geometric Structure
===================

Level 0: ElementTree
--------------------

  * only one class here

Level 1: ElementTreeItem
------------------------

Possible subclasses:

  * Transformation
  * Element
  * Source
  * Detector

Level 2: Element
----------------

Specific subclasses to represent optical elements, formed of potentially multiple components

Appears on the tree

Level 3: Component
------------------

Components are made of two things:

  * Surface
  * Material

This distinction is made because interactions

Does not directly appear on the tree

Serialisation
=============

SceneTree is the main entry point for the scene serialisation, each level is responsible for serialising
the next.

