# -*- coding: utf-8 -*-
"""
    prestans.types.string
    ~~~~~~~~~~~~~~~~~~~~~
    
    A WSGI compliant REST micro-framework.

    :copyright: (c) 2016 Anomaly Software
    :license: Apache 2.0, see LICENSE for more details.
"""

from . import Scalar


class String(Scalar, str):
    def __init__(self, value):
        str.__init__(value)

    @classmethod
    def from_value(cls, value, *args, **kwargs):
        return String(value)
    pass
