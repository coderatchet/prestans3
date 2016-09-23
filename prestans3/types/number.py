# -*- coding: utf-8 -*-
"""
    prestans.types.number
    ~~~~~~~~~~~~~~~~~~~~~

    A WSGI compliant REST micro-framework.

    :copyright: (c) 2016 Anomaly Software
    :license: Apache 2.0, see LICENSE for more details.
"""

from . import Scalar


class Number(Scalar):
    def __init__(self, *args, **kwargs):
        super(Scalar, self).__init__(*args, **kwargs)

    def __get__(self, instance, owner):
        pass
