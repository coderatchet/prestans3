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
        self._routes = routes

    def __call__(self, environ, start_response):
        for expression, route in self.routes:
            regex = re.compile(expression)
            if regex.match(environ.get("PATH_INFO", '')):
                return route(environ, start_response)


    @property
    def routes(self):
        return self._routes
