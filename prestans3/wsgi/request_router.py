# -*- coding: utf-8 -*-
"""
    prestans3.http.request_router
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    A WSGI compliant REST micro-framework.

    :copyright: (c) 2016 Anomaly Software
    :license: Apache 2.0, see LICENSE for more details.
"""
import re

from ..utils import is_str


class RequestRouter(object):
    def __init__(self, routes, logger=None):
        self._logger = logger
        self._routes = self._normalize_routes(routes)

    def __call__(self, environ, start_response):
        for expression, route in self.routes:
            # implicit start and end string characters
            regex = re.compile(expression)
            if regex.match(environ.get("PATH_INFO", '')):
                return route(environ, start_response)

    @property
    def routes(self):
        return self._routes

    @property
    def logger(self):
        return self._logger

    @classmethod
    def _normalize_routes(cls, routes):
        for path, handler in routes:
            # py2to3 replace with isinstance(path, str)
            if not is_str(path) or not cls.valid_wsgi_application(handler):
                raise ValueError(
                    "invalid route definition: ('{}', '{}'). The correct format is (route: str, handler: "
                    "(environ, start_response) -> any)".format(path, handler))
        return [(re.sub(r'\^?([^^$]+)\$?', r'^\1$', regex), route) for regex, route in routes]

    @classmethod
    def valid_wsgi_application(cls, func):
        if not callable(func):
            return False
        var_names = func.__code__.co_varnames
        arg_count = func.__code__.co_argcount
        return arg_count == 2 or (arg_count == 3 and (var_names[0] == 'self' or var_names[0] == 'cls'))
