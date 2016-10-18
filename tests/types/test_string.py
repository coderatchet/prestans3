# -*- coding: utf-8 -*-
"""
    tests.types.test_string
    ~~~~~~~~~~~~~~~~~~~~~~~

    A WSGI compliant REST micro-framework.

    :copyright: (c) 2016 Anomaly Software
    :license: Apache 2.0, see LICENSE for more details.
"""
import pytest
from prestans3.errors import ValidationException, PropertyConfigError
from prestans3.types import Model
from prestans3.types import String


def test_can_create_string():
    String()


def test_can_init_string():
    String("init")


def test_string_can_eq_native():
    assert String("special") == 'special'
    assert not String("no") == 'special'


def test_string_can_ne_native():
    assert String("no") != "yes"
    assert not String("yes") != "yes"


def test_string_can_call_startswith():
    assert String("yes").startswith("ye")
    assert not String("no").startswith("o")


def test_from_value_works():
    String.from_value('string') == 'string'
    string = String('string')
    String.from_value(string) == string


def test_from_value_does_not_accept_non_string():
    with pytest.raises(TypeError) as error:
        String.from_value(1)
    assert '{} of type {} is not coercible to {}'.format(1, int.__name__, String.__name__) in str(error.value)


def test_str_min_length_works():
    class _Model(Model):
        string = String.property(str_min_length=3)

    model = _Model.mutable()
    model.string = 'str'
    model.validate()
    model.string = 'no'
    with pytest.raises(ValidationException) as exception:
        model.validate()
    assert '{} str_min_length config is {} however len("{}") == {}'.format(String.__name__, 3, 'no', 2) \
           in str(exception)


def test_str_max_length_works():
    class _Model(Model):
        string = String.property(str_max_length=2)

    model = _Model.mutable()
    model.string = 'no'
    model.validate()
    model.string = 'str'
    with pytest.raises(ValidationException) as exception:
        model.validate()
    assert '{} str_max_length config is {} however len("{}") == {}'.format(String.__name__, 2, 'str', 3) \
           in str(exception)


# noinspection PyUnusedLocal
def test_str_max_and_min_are_compatible_values():
    class _Model(Model):
        string = String.property(str_min_length=3, str_max_length=3)

    with pytest.raises(PropertyConfigError) as error:
        class __Model(Model):
            string = String.property(str_min_length=3, str_max_length=2)
    assert 'invalid {} property configuration: ' + \
           'str_min_length config of {} is greater than str_max_length config of {}'.format(String.__name__, 3, 2)
