# -*- coding: utf-8 -*-
"""
    prestans.types.p_datetime
    ~~~~~~~~~~~~~~~~~~~~~~~~~
    
    A WSGI compliant REST micro-framework.

    :copyright: (c) 2016 Anomaly Software
    :license: Apache 2.0, see LICENSE for more details.
"""
from datetime import datetime

from prestans3.types.temporal import Temporal


# noinspection PyAbstractClass
class DateTime(Temporal, datetime):
    """
    Prestans 3 DateTime type.  Acts as a native python :class:`datetime.datetime` class with added prestans 3
    functionality.
    """

    def __init__(self, year, month=None, day=None, hour=0, minute=0, second=0, microsecond=0, tzinfo=None):
        import platform
        if platform.python_implementation() == 'PyPy':
            datetime.__init__(datetime(year, month, day, hour, minute, second, microsecond, tzinfo))
        else:
            datetime.__init__(year, month, day, hour, minute, second, microsecond, tzinfo)
        super(DateTime, self).__init__()

    @classmethod
    def from_value(cls, value):
        try:
            return super(DateTime, cls).from_value(value)
        except NotImplementedError:
            if not isinstance(value, datetime):
                raise TypeError(
                    "{} of type {} not coercible to type {}".format(value, value.__class__.__name__, cls.__name__))
        return DateTime(value.year, value.month, value.day, value.hour, value.minute, value.second, value.microsecond,
                        value.tzinfo)
