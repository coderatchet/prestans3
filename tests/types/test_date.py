# -*- coding: utf-8 -*-
"""
    tests.types.p_date
    ~~~~~~~~~~~~~~~~~~

    A WSGI compliant REST micro-framework.

    :copyright: (c) 2016 Anomaly Software
    :license: Apache 2.0, see LICENSE for more details.
"""
from copy import copy

import pytest
from datetime import date

from prestans3.types import Date


def test_can_create_date():
    Date(2000, 1, 1)


def test_invalid_init_raises_error():
    with pytest.raises(TypeError):
        Date()
    with pytest.raises(TypeError):
        Date(2000, 1)
    with pytest.raises(TypeError):
        Date(2000, day=1)


def test_can_compare_dates():
    assert Date(2000, 1, 1) == date(2000, 1, 1)
    assert not Date(2000, 1, 2) == date(2000, 1, 1)
    assert not Date(2000, 2, 1) == date(2000, 1, 1)
    assert not Date(2001, 1, 1) == date(2000, 1, 1)


def test_can_fromtimestamp():
    fromtimestamp = Date.fromtimestamp(1476767396)
    assert fromtimestamp == Date(2016, 10, 18)
    assert issubclass(fromtimestamp.__class__, Date)


def test_from_value_works():
    my_date = Date(2000, 1, 1)
    Date.from_value(my_date) is my_date
    Date.from_value(date(2000, 1, 1)) == my_date
    with pytest.raises(TypeError) as error:
        Date.from_value('mango')
    assert "{} of type {} is not coercible to type {}".format('mango', str.__name__, Date.__name__) in str(error.value)


def test_can_copy_self():
    date1 = Date(2000, 1, 3)
    date2 = copy(date1)
    assert date1 == date2
    assert date1 is not date2


def test_native_value():
    assert Date(2000, 1, 1).native_value == date(2000, 1, 1)
