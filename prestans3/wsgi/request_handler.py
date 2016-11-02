# -*- coding: utf-8 -*-
"""
    prestans3.wsgi.request_handler
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    A WSGI compliant REST micro-framework.

    :copyright: (c) 2016 Anomaly Software
    :license: Apache 2.0, see LICENSE for more details.
"""


class request(object):
    """ decorator for configuring HTTP methods on RequestHandlers """
    def __init__(self, http_method=None):
        self.prestans_handler = True
        self.http_method = http_method

    def __call__(self, f):
        def wrapped_f(*args, **kwargs):
            return f(*args, **kwargs)
        wrapped_f.prestans_handler = self.prestans_handler
        wrapped_f.http_method = self.http_method
        return wrapped_f



