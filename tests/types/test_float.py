# -*- coding: utf-8 -*-
"""
    tests.types.test_float
    ~~~~~~~~~~~~~~~~~~~~~~

    A WSGI compliant REST micro-framework.

    :copyright: (c) 2016 Anomaly Software
    :license: Apache 2.0, see LICENSE for more details.
"""
import pytest

from prestans3.types import Float


def test_can_create_float():
    Float()


def test_can_initialize_float():
    Float(1.2)


def test_can_eq_float():
    assert Float(1.2) == 1.2
    assert Float(1.2) == Float(1.2)
    assert not Float(1.2) == 1.3
    assert not Float(1.2) == Float(1.3)


def test_can_ne_float():
    assert Float(1.2) != 1.3
    assert Float(1.2) != Float(1.3)
    assert not Float(1.2) != Float(1.2)
    assert not Float(1.2) != Float(1.2)


def test_can_from_value_float():
    assert Float.from_value(1.2) == 1.2
    with pytest.raises(TypeError) as error:
        Float.from_value('no')
    assert "{} of type {} not coercible to {}".format("no", "no".__class__.__name__, Float.__name__) in str(error.value)


def test_native_value():
    assert Float(1.7).native_value == 1.7
    assert Float(-930.2435).native_value == -930.2435