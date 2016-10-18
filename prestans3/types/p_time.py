# -*- coding: utf-8 -*-
"""
    prestans.types.p_time
    ~~~~~~~~~~~~~~~~~~~~~
    
    A WSGI compliant REST micro-framework.

    :copyright: (c) 2016 Anomaly Software
    :license: Apache 2.0, see LICENSE for more details.
"""
from datetime import time

from . import ImmutableType


class Time(time, ImmutableType):
    pass
