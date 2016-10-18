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


def test_boolean_defaults_to_false():
    assert Boolean() == False


def test_boolean_can_ne_other_boolean():
    assert Boolean(True) != Boolean(False)
    assert not Boolean(False) != Boolean(False)


def test_boolean_can_or_properly():
    assert Boolean(True) or False
    assert Boolean(True) or True
    assert Boolean(False) or True
    assert not (Boolean(False) or False)
    assert Boolean(True) or Boolean(False)
    assert Boolean(True) or Boolean(True)
    assert Boolean(False) or Boolean(True)
    assert not (Boolean(False) or Boolean(False))


def test_boolean_can_and_properly():
    assert not (Boolean(True) and False)
    assert Boolean(True) and True
    assert not (Boolean(False) and True)
    assert not (Boolean(False) and False)
    assert not (Boolean(True) and Boolean(False))
    assert Boolean(True) and Boolean(True)
    assert not (Boolean(False) and Boolean(True))
    assert not (Boolean(False) and Boolean(False))
