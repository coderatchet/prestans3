# -*- coding: utf-8 -*-
"""
    prestans.types.integer
    ~~~~~~~~~~~~~~~~~~~~~~
    
    A WSGI compliant REST micro-framework.

    :copyright: (c) 2016 Anomaly Software
    :license: Apache 2.0, see LICENSE for more details.
"""

from .number import Number


class Integer(int, Number):
    def __init__(self, value, base=10):
        int.__init__(value, base)

    def __set__(self, instance, value, base=10):
        int.__init__(value, base)

    def __get__(self, instance, owner):
        return self
