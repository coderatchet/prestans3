# -*- coding: utf-8 -*-
"""
    test.types.test_time
    ~~~~~~~~~~~~~~~~~~~~

    A WSGI compliant REST micro-framework.

    :copyright: (c) 2016 Anomaly Software
    :license: Apache 2.0, see LICENSE for more details.
"""
from prestans3.types import Time


def can_create_time():
    the_time = Time(1, 2, 3)
    assert isinstance(the_time, Time)
