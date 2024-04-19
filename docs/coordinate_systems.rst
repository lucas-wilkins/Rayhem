Coordinate Systems
==================

There are three kinds coordinate systems, global, local, and internal, that are used in different contexts

Global
------

The base 3D cartesian coordinate system that is the same everywhere

Local
-----

Coordinate system from inside an element in the tree, rotated and translated from the global system

Internal
--------

These are used within the surface classes, representing a point on the surface, in whatever coordinate system is
most convenient (usually a projection onto a plane, but could be anything as long as its consistent)
