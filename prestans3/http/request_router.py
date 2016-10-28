# -*- coding: utf-8 -*-
"""
    prestans3.http.request_router
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    A WSGI compliant REST micro-framework.

    :copyright: (c) 2016 Anomaly Software
    :license: Apache 2.0, see LICENSE for more details.
"""
import re


class RequestRouter(object):
    def __init__(self, routes):
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

    @classmethod
    def _normalize_routes(cls, routes):
        return [(re.sub(r'\^{0,1}([^^$]*)\${0,1}', r'^\1$', regex), route) for regex, route in routes]
