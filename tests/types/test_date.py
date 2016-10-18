# -*- coding: utf-8 -*-
"""
    tests.types.p_date
    ~~~~~~~~~~~~~~~~~~

    A WSGI compliant REST micro-framework.

    :copyright: (c) 2016 Anomaly Software
    :license: Apache 2.0, see LICENSE for more details.
"""
from datetime import date, time

import pytest
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
    assert Date.fromtimestamp(1476767396) == Date(2016, 10, 18)
