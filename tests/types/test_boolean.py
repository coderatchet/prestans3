# -*- coding: utf-8 -*-
"""
    tests.types.test_boolean
    ~~~~~~~~~~~~~~~~~~~~~~~~

    A WSGI compliant REST micro-framework.

    :copyright: (c) 2016 Anomaly Software
    :license: Apache 2.0, see LICENSE for more details.
"""
from prestans3.types import Boolean


def test_can_create_boolean():
    Boolean()


def test_boolean_can_accept_default_value():
    Boolean(True)


def test_boolean_can_eq_native_boolean():
    assert Boolean(True) == True
    assert not Boolean(False) == True


def test_boolean_can_eq_other_boolean():
    assert Boolean(True) == Boolean(True)
    assert not Boolean(False) == Boolean(True)


def test_boolean_can_ne_native_boolean():
    assert Boolean(True) != False
    assert not Boolean(False) != False
