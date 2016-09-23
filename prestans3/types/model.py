# -*- coding: utf-8 -*-
"""
    prestans.types.string
    ~~~~~~~~~~~~~~~~~~~~~
    
    A WSGI compliant REST micro-framework.

    :copyright: (c) 2016 Anomaly Software
    :license: Apache 2.0, see LICENSE for more details.
"""

from . import Collection
from builtins import dict


class Model(dict, Collection):
    def __init__(self, seq, **kwargs):
        dict.__init__(seq, **kwargs)
