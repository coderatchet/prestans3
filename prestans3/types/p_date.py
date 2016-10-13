# -*- coding: utf-8 -*-
"""
    prestans.types.p_date
    ~~~~~~~~~~~~~~~~~~~~~
    
    A WSGI compliant REST micro-framework.

    :copyright: (c) 2016 Anomaly Software
    :license: Apache 2.0, see LICENSE for more details.
"""
from datetime import date

from . import Model


class Date(Model):
    """
    Prestans3 Date Type.
    """

    def __new__(self, year, month, day):
        if getattr(self, '__init__', None):
            date.__new__(year, month, day)
        return self
