# -*- coding: utf-8 -*-
"""
    prestans.types.string
    ~~~~~~~~~~~~~~~~~~~~~
    
    A WSGI compliant REST micro-framework.

    :copyright: (c) 2016 Anomaly Software
    :license: Apache 2.0, see LICENSE for more details.
"""

from prestans3.utils import is_str

from . import ImmutableType


class String(ImmutableType, str):
    def __init__(self, value=None):
        if value is None:
            value = ""
        str.__init__(value)

    @classmethod
    def from_value(cls, value):
        if not is_str(value):
            raise TypeError
        return String(value)
