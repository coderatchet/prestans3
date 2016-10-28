# -*- coding: utf-8 -*-
"""
    tests.http.test_request_router
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    A WSGI compliant REST micro-framework.

    :copyright: (c) 2016 Anomaly Software
    :license: Apache 2.0, see LICENSE for more details.
"""

from prestans3.http.request_router import RequestRouter


def test_router_is_a_callable_with_two_args():
    assert callable(RequestRouter())
    func = RequestRouter.__call__
    var_names = func.__code__.co_varnames
    assert len(var_names) == 2 or (len(var_names) == 3 and (var_names[0] == 'self' or var_names[0] == 'cls'))
