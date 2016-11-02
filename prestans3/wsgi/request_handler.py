# -*- coding: utf-8 -*-
"""
    prestans3.wsgi.request_handler
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    A WSGI compliant REST micro-framework.

    :copyright: (c) 2016 Anomaly Software
    :license: Apache 2.0, see LICENSE for more details.
"""


def request(func):
    """ decorator for configuring HTTP methods on RequestHandlers """
    return func
