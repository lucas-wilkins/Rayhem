
"""

Nodes define a finite state machine that controls how to search the scene

Path nodes and components are different things

Each node references multiple components which are to be checked
Each component maps to a single next node, which will be transitioned to if a ray collides
Escape is an absorbing state which all nodes can transition to if no component has a collision

On every step there is a transition to a linked node (it could have a self link)

But, nodes can map to themselves (if not a source node), and there can be cycles

Sources are represented by nodes that cannot be mapped to


For usability, we probably want the following options for mapping:
 * Any component -> single output
 * single component -> single output
 * completely general: map of component to any node


The basic internal structure passed to the simulation can just be a nodes-long list of components-long lists
The inner list gives the next node for each component, each component then mapping to the next node

Or better still, a n_nodes x n_components int array, -1 can represent the escaped state

For example, the basic fully connected graph with one source at index 0 would be of the form

0 ---[everything]----> 1

[[1,1,1,1,1,1....]
 [1,1,1,1,1,1....]]

A two component system with a map like

0 ---------------[component 0]--------------> 1 --[anything]---> escape
 \                                         /
  `--[component 1]---> 2 --[component 0]--'

[[ 1  2]
 [-1 -1]
 [ 1 -1]]

"""
import numpy as np

from elements.simulation_data import InterfaceAndTransform, SourceAndTransform


class Path:
    def __init__(self):
        pass

    def create_map(self, interfaces: list[InterfaceAndTransform], sources: list[SourceAndTransform]) -> np.ndarray:
        pass


class FullyConnected(Path):
    pass