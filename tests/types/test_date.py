# -*- coding: utf-8 -*-
"""
    tests.types.p_date
    ~~~~~~~~~~~~~~~~~~

    A WSGI compliant REST micro-framework.

    :copyright: (c) 2016 Anomaly Software
    :license: Apache 2.0, see LICENSE for more details.
"""
from datetime import date

from prestans3.types import Date


def test_can_create_date():
    Date(2000, 1, 1)


def test_can_init_date():
    Date(date(2000, 1, 1))
