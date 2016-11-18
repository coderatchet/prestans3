# -*- coding: utf-8 -*-
"""
    tests.http.test_request_handler
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    A WSGI compliant REST micro-framework.

    :copyright: (c) 2016 Anomaly Software
    :license: Apache 2.0, see LICENSE for more details.
"""
import inspect

import prestans3.utils as utils
from prestans3.wsgi.request_handler import request
from inspect import isfunction


def test_request_decorator_returns_callable():
    deco = request()
    func = deco(lambda x: x is True)
    assert callable(func)
    assert func(True)


def test_inspect_decorated_methods_have__request_flag():
    class _Handler(object):
        @request
        def my_get(self):
            pass

    handler_method = utils.get_user_attributes(_Handler)[0][1]
    assert hasattr(handler_method, 'prestans_handler') and handler_method.prestans_handler


def test_decorated_request_methods_have_http_verb_setting():
    class _Handler(object):
        @request(http_method='GET')
        def my_get_method(self):
            pass

    handler_method = utils.get_user_attributes(_Handler)[0][1]
    assert hasattr(handler_method, 'http_method') and handler_method.http_method == 'GET'
