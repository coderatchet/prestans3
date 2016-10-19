# -*- coding: utf-8 -*-
"""
    prestans.types.float
    ~~~~~~~~~~~~~~~~~~~~
    
    A WSGI compliant REST micro-framework.

    :copyright: (c) 2016 Anomaly Software
    :license: Apache 2.0, see LICENSE for more details.
"""

from . import Number


class Float(Number, float):


    @classmethod
    def from_value(cls, value):
        try:
            return super(Float, cls).from_value(value)
        except NotImplementedError:
            if not isinstance(value, float):
                raise TypeError("{} of type {} not coercible to {}".format(value, value.__class__.__name__, cls.__name__))
            return Float(value)
