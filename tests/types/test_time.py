# -*- coding: utf-8 -*-
"""
    test.types.test_time
    ~~~~~~~~~~~~~~~~~~~~

    A WSGI compliant REST micro-framework.

    :copyright: (c) 2016 Anomaly Software
    :license: Apache 2.0, see LICENSE for more details.
"""
from datetime import timezone, time

from prestans3.types import Time


def test_can_create_time():
    the_time = Time(1, 2, 3, 4, timezone.utc)
    assert isinstance(the_time, Time)


def can_from_value_create_time():
    the_time = Time(1, 2, 3, 4)
    assert Time.from_value(the_time) is the_time
    assert Time.from_value(time(1, 2, 3, 4, timezone.utc)) == the_time
