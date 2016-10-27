# -*- coding: utf-8 -*-
"""
    tests.types.test_boolean
    ~~~~~~~~~~~~~~~~~~~~~~~~

    A WSGI compliant REST micro-framework.

    :copyright: (c) 2016 Anomaly Software
    :license: Apache 2.0, see LICENSE for more details.
"""
import pytest

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


def test_can_create_boolean_from_value():
    boolean = Boolean(True)
    assert Boolean.from_value(True) == boolean
    assert Boolean.from_value(boolean) is boolean


def test_non_bool_value_raises_type_error():
    with pytest.raises(TypeError) as error:
        Boolean.from_value('cheese')
    assert "{} of type {} is not a subclass of {} or a bool".format('cheese', str.__name__, Boolean)


def test_native_value():
    assert Boolean(True).native_value == True
    assert Boolean(False).native_value == False


def test_to_from_value_invariant():
    my_bool = Boolean(True)
    assert my_bool == Boolean.from_value(my_bool.native_value)
    my_bool = Boolean(False)
    assert my_bool == Boolean.from_value(my_bool.native_value)
