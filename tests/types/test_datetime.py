# -*- coding: utf-8 -*-
"""
    test.types.test_datetime
    ~~~~~~~~~~~~~~~~~~~~~~~~

    A WSGI compliant REST micro-framework.

    :copyright: (c) 2016 Anomaly Software
    :license: Apache 2.0, see LICENSE for more details.
"""
from datetime import datetime, tzinfo

import pytest
from prestans3.types import DateTime


class _UTC(tzinfo):
    def name(self):
        return 'UTC'

    def dst(self, dt):
        return 0

    def utcoffset(self, dt):
        return 0


utc = _UTC()


def test_can_create_date_time():
    my_datetime = DateTime(2000, 1, 1)
    assert isinstance(my_datetime, DateTime)


def test_can_init_date_time():
    my_datetime = DateTime(2000, 1, 2, 3, 4, 5, 6, utc)
    assert my_datetime.year == 2000
    assert my_datetime.month == 1
    assert my_datetime.day == 2
    assert my_datetime.hour == 3
    assert my_datetime.minute == 4
    assert my_datetime.second == 5
    assert my_datetime.microsecond == 6
    assert my_datetime.tzinfo is utc


def test_can_from_value():
    my_datetime = DateTime(2000, 1, 2, 3, 4, 5, 6, utc)
    assert DateTime.from_value(my_datetime) is my_datetime
    assert DateTime.from_value(datetime(2000, 12, 1, 1, 1, 1, 1, utc)) == datetime(2000, 12, 1, 1, 1, 1, 1, utc)
    with pytest.raises(TypeError) as error:
        DateTime.from_value("no")
    assert "{} of type {} not coercible to type {}".format("no", str.__name__, DateTime.__name__)
