# -*- coding: utf-8 -*-
"""
    prestans.types.string
    ~~~~~~~~~~~~~~~~~~~~~
    
    A WSGI compliant REST micro-framework.

    :copyright: (c) 2016 Anomaly Software
    :license: Apache 2.0, see LICENSE for more details.
"""

from . import Scalar


# http://stackoverflow.com/questions/2172189/why-i-cant-extend-bool-in-python
class Boolean(Scalar):
    def __init__(self, value):
        self._value = value

    @classmethod
    def __new__(cls, value=False, **kwargs):
        return Boolean(value)

    pass
