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
from unittest.mock import create_autospec

import pytest
import pytest_mock
import logging

from prestans3.wsgi.request_router import RequestRouter


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


def test_router_redirects_routes(mocker):
    """
    :param pytest_mock.MockFixture mocker:
    """
    here = []
    there = []

    # noinspection PyUnusedLocal
    def _test(environ, start_response):
        here.append('yes')

    # noinspection PyUnusedLocal
    def _more(environ, start_response):
        there.append('yes')

    router = RequestRouter(routes=[
        ('/', _test),
        ('/more', _more)
    ])

    assert here == []
    assert there == []
    router(_default_wsgi_environ, lambda _x, _y: None)
    assert here == ['yes']
    assert there == []
    _custom_path_wsgi_environ = setup_test_environ({"PATH_INFO": '/more'})
    router(_custom_path_wsgi_environ, lambda _x, _y: None)
    assert here == ['yes']
    assert there == ['yes']


def test_route_always_starts_and_ends_with_proper_dollar_and_carets():
    r = RequestRouter(routes=[(r'/', _test_handler)])
    assert r.routes[0][0] == r'^/$'
    r = RequestRouter(routes=[(r'^/', _test_handler)])
    assert r.routes[0][0] == r'^/$'
    r = RequestRouter(routes=[(r'/$', _test_handler)])
    assert r.routes[0][0] == r'^/$'
    r = RequestRouter(routes=[(r'^/$', _test_handler)])
    assert r.routes[0][0] == r'^/$'


def test_route_configuration_only_accepts_valid_tuples():
    RequestRouter(routes=[('/valid', _test_handler)])
    with pytest.raises(Exception):
        RequestRouter(routes=['no'])
    with pytest.raises(Exception):
        RequestRouter(routes=[('/valid', _test_handler, 'too many arguments')])
    with pytest.raises(ValueError) as error:
        RequestRouter(routes=[('/invalid', 123)])
    assert "invalid route definition: ('{}', '{}'). " \
           "The correct format is (route: str, handler: (environ, start_response) -> any)".format('/invalid', 123) \
           in str(error.value)
    with pytest.raises(ValueError) as error:
        RequestRouter(routes=[(432, _test_handler)])
    assert "invalid route definition: ('{}', '{}'). " \
           "The correct format is (route: str, handler: (environ, start_response) -> any)".format(432, _test_handler) \
           in str(error.value)

    # noinspection PyUnusedLocal
    def _incorrect(x):
        pass

    with pytest.raises(ValueError) as error:
        RequestRouter(routes=[('/invalid', _incorrect)])
    assert "invalid route definition: ('{}', '{}'). " \
           "The correct format is (route: str, handler: (environ, start_response) -> any)".format('/invalid',
                                                                                                  _incorrect) \
           in str(error.value)


def test_request_router_accepts_logger():
    logger = logging.getLogger("test logger")
    r = RequestRouter(routes=[], logger=logger)
    assert r.logger == logger
