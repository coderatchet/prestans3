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


def setup_test_environ(overrides=None):
    dictionary = dict(os.environ)
    if overrides is not None:
        dictionary.update(overrides)
    wsgiref.util.setup_testing_defaults(dictionary)
    return dictionary


_default_wsgi_environ = setup_test_environ()


def _test_handler(x, y):
    pass


def test_router_is_a_callable_with_two_args():
    assert callable(RequestRouter(routes=[]))
    func = RequestRouter.__call__
    var_names = func.__code__.co_varnames
    arg_count = func.__code__.co_argcount
    assert arg_count == 2 or (arg_count == 3 and (var_names[0] == 'self' or var_names[0] == 'cls'))


def test_router_accepts_a_list_of_routes():
    RequestRouter(routes=[])


def test_can_get_routes():
    my_routes = [('^/api.*$', lambda _x, _y: None)]
    router = RequestRouter(routes=my_routes)
    assert router.routes == my_routes


def test_router_may_be_passed_environment():
    router = RequestRouter(routes=[])
    router(_default_wsgi_environ, lambda _x, _y: None)


def test_router_redirects_routes():
    here = False
    there = False

    # noinspection PyUnusedLocal
    def _test(x, y):
        nonlocal here
        here = True

    def _more(x, y):
        nonlocal there
        there = True

    router = RequestRouter(routes=[
        ('/', _test),
        ('/more', _more)
    ])
    router(_default_wsgi_environ, lambda _x, _y: None)
    assert here is True
    assert there is False
    _default_wsgi_environ['PATH_INFO'] = '/more'
    router(_default_wsgi_environ, lambda _x, _y: None)
    assert there is True


def test_route_always_starts_and_ends_with_proper_dollar_and_carets():
    r = RequestRouter(routes=[(r'/', _test_handler)])
    assert r.routes[0][0] == r'^/$'
    r = RequestRouter(routes=[(r'^/', _test_handler)])
    assert r.routes[0][0] == r'^/$'
    r = RequestRouter(routes=[(r'/$', _test_handler)])
    assert r.routes[0][0] == r'^/$'
    r = RequestRouter(routes=[(r'^/$', _test_handler)])
    assert r.routes[0][0] == r'^/$'
