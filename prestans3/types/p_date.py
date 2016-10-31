# -*- coding: utf-8 -*-
"""
    prestans.types.p_date
    ~~~~~~~~~~~~~~~~~~~~~
    
    A WSGI compliant REST micro-framework.

    :copyright: (c) 2016 Anomaly Software
    :license: Apache 2.0, see LICENSE for more details.
"""
from datetime import date

from prestans3.types.temporal import Temporal


class Date(date, Temporal):
    """
    Prestans3 Date Type. Acts as a native python :class:`datetime.date` class with added prestans 3 functionality.
    """

    def __init__(self, year, month, day):
        import platform
        # py2to3 remove if and only perform else
        if platform.python_implementation() == 'PyPy':
            date.__init__(date(year, month, day))
        else:
            date.__init__(year, month, day)
        super(Date, self).__init__()

    @classmethod
    def from_value(cls, value):
        try:
            return super(Date, cls).from_value(value)
        except NotImplementedError:
            if not isinstance(value, date):
                raise TypeError(
                    "{} of type {} is not coercible to type {}".format(value, value.__class__.__name__, cls.__name__))
            return Date(value.year, value.month, value.day)

    def __copy__(self):
        return Date(self.year, self.month, self.day)
