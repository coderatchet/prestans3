# -*- coding: utf-8 -*-
"""
    tests.types.test_integer
    ~~~~~~~~~~~~~~~~~~~~~~~~

    A WSGI compliant REST micro-framework.

    :copyright: (c) 2016 Anomaly Software
    :license: Apache 2.0, see LICENSE for more details.
"""

import pytest

from prestans3.types import Integer


def test_can_create_integer():
    Integer(1)


def test_integer_behaves_like_native_integer():
    my_int = Integer(3)
    assert my_int + 3 == 6
    assert my_int - 1 == 2
    assert my_int / 3 == 1
    assert my_int * 3 == 9
    my_int -= 2
    assert my_int == 1
    my_int += 2
    assert my_int == 3
    my_int /= 3
    assert my_int == 1
    my_int *= 3
    assert my_int == 3


def test_from_value_with_integer_instance_succeeds():
    integer = Integer(1)
    value = Integer.from_value(integer)
    assert value == integer


def test_from_value_with_native_int_succeeds():
    integer = 1
    value = Integer.from_value(integer)
    assert value == Integer(1)


def test_from_value_raises_value_error_on_non_int_subclass():
    with pytest.raises(ValueError):
        Integer.from_value('string')
    with pytest.raises(ValueError):
        Integer.from_value({})
    with pytest.raises(ValueError):
        Integer.from_value(0.3)




