# -*- coding: utf-8 -*-
"""
    tests.types.p_date
    ~~~~~~~~~~~~~~~~~~

    A WSGI compliant REST micro-framework.

    :copyright: (c) 2016 Anomaly Software
    :license: Apache 2.0, see LICENSE for more details.
"""
from prestans3.types import Date


def test_can_create_date():
    Date()
