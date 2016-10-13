# -*- coding: utf-8 -*-
"""
    prestans.types.p_datetime
    ~~~~~~~~~~~~~~~~~~~~~~~~~
    
    A WSGI compliant REST micro-framework.

    :copyright: (c) 2016 Anomaly Software
    :license: Apache 2.0, see LICENSE for more details.
"""
from datetime import datetime

from . import Model


class DateTime(datetime, Model):
    def __init__(self):
        super(DateTime, self).__init__()
    pass
