import pytest

import numpy as np

from components.sources.source import Source
from components.transformation import Transformation
from tests.dummy_element import DummyElement

trans_list = [
    [0,0,0],
    [1,0,0],
    [0,1,0],
    [0,0,1],
    [1,1,0],
    [1,0,1],
    [1,0,-1],
    [1,-1,0],
    [1,1,1]]

angle_list = [np.pi*x/180 for x in [1, 22.5, 45, 90, 180, 270, 360]]

axis_list = []

@pytest.mark.parametrize("a", trans_list)
@pytest.mark.parametrize("b", trans_list)
def test_compound_two_translations(a, b):
    a = np.array(a)
    b = np.array(b)

    ta = Transformation(translation=a)
    tb = Transformation(translation=b)
    source = Source()
    element = DummyElement()

    ta.addChild(tb)
    tb.addChild(source)
    tb.addChild(element)

    comps = ta.transformed_components()
    srcs = ta.transformed_sources()

    assert len(comps) == 1
    assert len(srcs) == 1

    assert comps[0].forward_translation == pytest.approx(a + b)
    assert -comps[0].backward_translation == pytest.approx(a + b)
    assert srcs[0].forward_translation == pytest.approx(a + b)
    assert -srcs[0].backward_translation == pytest.approx(a + b)

@pytest.mark.parametrize("axis, expected", [
    [(1,0,0), (0,-1,1)],
    [(0,1,0), (1,0,1)],
    [(0,0,1), (0,0,2)]
])
def test_z_rot90_z(axis, expected):

    expected = np.array(expected)

    ta = Transformation(translation=[0,0,1], axis=np.array(axis), angle=np.pi/2)
    tb = Transformation(translation=[0,0,1])

    source = Source()
    element = DummyElement()

    ta.addChild(tb)
    tb.addChild(source)
    tb.addChild(element)

    comps = ta.transformed_components()
    srcs = ta.transformed_sources()

    assert len(comps) == 1
    assert len(srcs) == 1

    assert comps[0].forward_translation == pytest.approx(expected)
    assert srcs[0].forward_translation == pytest.approx(expected)

    # Don't test inverses at this point




# def test_inverses_1():
#     pass
#
# def test_inverses_2():
#     pass
#
# def test_inverses_3():
#     pass