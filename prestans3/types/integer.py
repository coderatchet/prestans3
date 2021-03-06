# -*- coding: utf-8 -*-
"""
    prestans.types.integer
    ~~~~~~~~~~~~~~~~~~~~~~
    
    A WSGI compliant REST micro-framework.

    :copyright: (c) 2016 Anomaly Software
    :license: Apache 2.0, see LICENSE for more details.
"""

from . import Number


class Integer(Number, int):
    """
    Prestans 3 Integer type. Acts as a native :class:`int` with additional Prestans 3 functionality.
    """

    @classmethod
    def from_value(cls, value):
        try:
            # noinspection PyUnresolvedReferences
            return super(Integer, cls).from_value(value)
        except NotImplementedError:
            if not isinstance(value, int):
                raise ValueError(value)
            return Integer(value)

    def __init__(self, value, base=10):
        int.__init__(value, base)
