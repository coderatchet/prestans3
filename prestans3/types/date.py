# -*- coding: utf-8 -*-
"""
    prestans.types.string
    ~~~~~~~~~~~~~~~~~~~~~
    
    A WSGI compliant REST micro-framework.

    :copyright: (c) 2016 Anomaly Software
    :license: Apache 2.0, see LICENSE for more details.
"""
from datetime import date

from . import Structure


class Date(Structure, date):

    @classmethod
    def __new__(cls, year, month, day):
        cls._date = date.__new__(cls, year, month, day)

    def __get__(self, instance, owner):
        return self._date

    def __set__(self, instance, value):
        # todo validate
        self._date = value

    pass
