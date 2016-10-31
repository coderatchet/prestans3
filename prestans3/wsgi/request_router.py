# -*- coding: utf-8 -*-
"""
    prestans3.http.request_router
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    A WSGI compliant REST micro-framework.

    :copyright: (c) 2016 Anomaly Software
    :license: Apache 2.0, see LICENSE for more details.
"""
import re
from inspect import isfunction

from ..utils import is_str


class RequestRouter(object):
    def __init__(self, routes, serializers=None, default_serializer=None, deserializers=None,
                 default_deserializers=None, logger=None, application_name='wsgi_application'):
        if deserializers is None:
            deserializers = {}
        if serializers is None:
            serializers = {}
        if default_deserializers is None:
            default_deserializers = []
        self._logger = logger
        self._routes = self._normalize_routes(routes)
        self._serializers = serializers
        self._default_serializer = default_serializer
        self._deserializers = deserializers
        self._default_deserializers = default_deserializers
        self._application_name = application_name

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

    @property
    def serializers(self):
        return self._serializers

    @property
    def default_serializer(self):
        return self._default_serializer

    @property
    def deserializers(self):
        return self._deserializers

    @property
    def default_deserializers(self):
        return self._default_deserializers

    @property
    def application_name(self):
        return self._application_name

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
    def valid_wsgi_application(cls, _callable):
        if not callable(_callable):
            return False
        from inspect import isclass
        if isclass(_callable):
            _callable = _callable.__call__
        if not isfunction(_callable) and hasattr(_callable, '__call__'):
            _callable = _callable.__call__.__func__
        var_names = _callable.__code__.co_varnames
        arg_count = _callable.__code__.co_argcount
        return arg_count == 2 or (arg_count == 3 and (var_names[0] == 'self' or var_names[0] == 'cls'))
