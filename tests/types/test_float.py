# -*- coding: utf-8 -*-
"""
    tests.types.test_float
    ~~~~~~~~~~~~~~~~~~~~~~

    A WSGI compliant REST micro-framework.

    :copyright: (c) 2016 Anomaly Software
    :license: Apache 2.0, see LICENSE for more details.
"""
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


def test_can_from_value_float():
    assert Float.from_value(1.2) == 1.2


def test_can_ne_float():
    assert Float(1.2) != 1.3
    assert Float(1.2) != Float(1.3)
    assert not Float(1.2) != Float(1.2)
    assert not Float(1.2) != Float(1.2)
