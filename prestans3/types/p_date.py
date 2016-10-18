# -*- coding: utf-8 -*-
"""
    prestans.types.p_date
    ~~~~~~~~~~~~~~~~~~~~~
    
    A WSGI compliant REST micro-framework.

    :copyright: (c) 2016 Anomaly Software
    :license: Apache 2.0, see LICENSE for more details.
"""

from . import ImmutableType


class Date(ImmutableType):
    """
    Prestans3 Date Type.
    """

    def __init__(self):
        super().__init__()
