# -*- coding: utf-8 -*-
"""
    prestans.types.p_time
    ~~~~~~~~~~~~~~~~~~~~~
    
    A WSGI compliant REST micro-framework.

    :copyright: (c) 2016 Anomaly Software
    :license: Apache 2.0, see LICENSE for more details.
"""
from datetime import time

from prestans3.types.temporal import Temporal


class Time(Temporal, time):
    """
    Prestans 3 Time type.  Acts as a native python :class:`datetime.time` class with added prestans 3 functionality.
    """

    def __init__(self, hour=0, minute=0, second=0, microsecond=0, tzinfo=None):
        import platform
        if platform.python_implementation() == 'PyPy':
            time.__init__(time(hour, minute, second, microsecond, tzinfo))
        else:
            time.__init__(hour, minute, second, microsecond, tzinfo)
        super(Time, self).__init__()

    @classmethod
    def from_value(cls, value):
        try:
            return super(Time, cls).from_value(value)
        except NotImplementedError:
            if not isinstance(value, time):
                raise TypeError(
                    "{} of type {} is not coercible to type {}".format(value, value.__class__.__name__, cls.__name__))
        return Time(value.hour, value.minute, value.second, value.microsecond, value.tzinfo)
