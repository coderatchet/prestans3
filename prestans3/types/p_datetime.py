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
    def __init__(self):
        super(DateTime, self).__init__()
    pass
