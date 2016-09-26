# coding=utf-8
"""
    prestans.types.string
    ~~~~~~~~~~~~~~~~~~~~~

    A WSGI compliant REST micro-framework.

    :copyright: (c) 2016 Anomaly Software
    :license: Apache 2.0, see LICENSE for more details.
"""
from abc import ABCMeta


class TypeProperty:

    def __init__(self):
        raise Exception("Should not instantiate this class directly")

    __metaclass__ = ABCMeta
    pass