# -*- coding: utf-8 -*-
"""
    tests.http.test_request_handler
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    A WSGI compliant REST micro-framework.

    :copyright: (c) 2016 Anomaly Software
    :license: Apache 2.0, see LICENSE for more details.
"""

from prestans3.wsgi.request_handler import request
from inspect import isfunction


def test_request_decorator_returns_function():
    func = request(lambda x: None)
    assert isfunction(func)
