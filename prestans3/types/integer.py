# -*- coding: utf-8 -*-
"""
    prestans.types.integer
    ~~~~~~~~~~~~~~~~~~~~~~
    
    A WSGI compliant REST micro-framework.

    :copyright: (c) 2016 Anomaly Software
    :license: Apache 2.0, see LICENSE for more details.
"""

from . import Number


class Integer(int, Number):
    # @property_rule
    @classmethod
    def _min(cls, min_value=0, instance=None):
        if instance is None:
            raise TypeError("Huh?")
        return instance >= min_value

    def __init__(self, value, base=10):
        int.__init__(value, base)
