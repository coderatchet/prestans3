# -*- coding: utf-8 -*-
"""
    test.types.test_datetime
    ~~~~~~~~~~~~~~~~~~~~~~~~

    A WSGI compliant REST micro-framework.

    :copyright: (c) 2016 Anomaly Software
    :license: Apache 2.0, see LICENSE for more details.
"""
from datetime import timezone, datetime

from prestans3.types import DateTime


def test_can_create_date_time():
    my_datetime = DateTime(2000, 1, 1)
    assert isinstance(my_datetime, DateTime)


def test_can_init_date_time():
    tz = timezone.utc
    my_datetime = DateTime(2000, 1, 2, 3, 4, 5, 6, tz)
    assert my_datetime.year == 2000
    assert my_datetime.month == 1
    assert my_datetime.day == 2
    assert my_datetime.hour == 3
    assert my_datetime.minute == 4
    assert my_datetime.second == 5
    assert my_datetime.microsecond == 6
    assert my_datetime.tzinfo is tz


def test_can_from_value():
    my_datetime = DateTime(2000, 1, 2, 3, 4, 5, 6, timezone.utc)
    assert DateTime.from_value(my_datetime) is my_datetime
    assert DateTime.from_value(datetime(2000, 12, 1, 1, 1, 1, 1, timezone.utc)) == datetime(2000, 12, 1, 1, 1, 1, 1,
                                                                                            timezone.utc)
