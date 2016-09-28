# -*- coding: utf-8 -*-
"""
    prestans.types.string
    ~~~~~~~~~~~~~~~~~~~~~
    
    A WSGI compliant REST micro-framework.

    :copyright: (c) 2016 Anomaly Software
    :license: Apache 2.0, see LICENSE for more details.
"""

from . import Iterable


class Array(Iterable):
    def __init__(self, seq=None):
        super().__init__(seq if seq is not None else [])
