# -*- coding: utf-8 -*-
"""
    tests.http.test_request_router
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    A WSGI compliant REST micro-framework.

    :copyright: (c) 2016 Anomaly Software
    :license: Apache 2.0, see LICENSE for more details.
"""
import os
import wsgiref.util

from prestans3.http.request_router import RequestRouter


def test_router_is_a_callable_with_two_args():
    assert callable(RequestRouter(routes=[]))
    func = RequestRouter.__call__
    var_names = func.__code__.co_varnames
    assert len(var_names) == 2 or (len(var_names) == 3 and (var_names[0] == 'self' or var_names[0] == 'cls'))


def test_router_accepts_a_list_of_routes():
    RequestRouter(routes=[])


def test_can_get_routes():
    my_routes = [('^/api.*', lambda _x, _y: None)]
    router = RequestRouter(routes=my_routes)
    assert router.routes == my_routes


def test_router_may_be_passed_environment():
    environ = dict(os.environ)
    wsgiref.util.setup_testing_defaults(environ)
    router = RequestRouter(routes=[])
    router(environ, lambda _x, _y: None)
