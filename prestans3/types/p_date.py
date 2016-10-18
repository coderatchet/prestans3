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


class Date(ImmutableType):
    """
    Prestans3 Date Type.
    """

    def __init__(self, date_or_year, month=None, day=None):
        if month is None and day is None and isinstance(date_or_year, date):
            self._value = date_or_year
        elif bool(month is None) != bool(day is None):
            raise ValueError(
                "both month and day must be specified if calling {}(year, month, day)".format(self.__class__.__name__))
        else:
            self._value = date(date_or_year, month, day)
        super().__init__()
