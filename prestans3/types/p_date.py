# -*- coding: utf-8 -*-
"""
    prestans.types.p_date
    ~~~~~~~~~~~~~~~~~~~~~
    
    A WSGI compliant REST micro-framework.

    :copyright: (c) 2016 Anomaly Software
    :license: Apache 2.0, see LICENSE for more details.
"""
from datetime import date

from . import ImmutableType


class Date(date, ImmutableType):
    """
    Prestans3 Date Type.
    """

    def __init__(self, year, month, day):
        date.__init__(year, month, day)
        super(Date, self).__init__()