# -*- coding: utf-8 -*-
"""
    prestans.types.p_date
    ~~~~~~~~~~~~~~~~~~~~~
    
    A WSGI compliant REST micro-framework.

    :copyright: (c) 2016 Anomaly Software
    :license: Apache 2.0, see LICENSE for more details.
"""
from datetime import date

from prestans3.errors import AccessError
from prestans3.types.temporal import Temporal


# noinspection PyAbstractClass
class Date(date, Temporal):
    """
    Prestans3 Date Type.
    """

    def __init__(self, year, month, day):
        date.__init__(year, month, day)
        super(Date, self).__init__()

    def replace(self, year=None, month=None, day=None):
        raise AccessError(self.__class__, "attempted to call replace on an immutable {class_name}, " +
                          "For a mutable {class_name}, call {class_name}.mutable(...)".format(
                              class_name=self.__class__.__name__))
