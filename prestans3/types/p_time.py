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
    def __init__(self, hour=0, minute=0, second=0, microsecond=0, tzinfo=None):
        time.__init__(hour, minute, second, microsecond, tzinfo)
        super(Time, self).__init__()

