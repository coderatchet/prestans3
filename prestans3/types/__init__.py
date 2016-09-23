# -*- coding: utf-8 -*-
"""
    prestans.types
    ~~~~~~~~~~~~~~
    
    A WSGI compliant REST micro-framework.

    :copyright: (c) 2016 Anomaly Software
    :license: Apache 2.0, see LICENSE for more details.
"""
from abc import abstractmethod, ABCMeta


class ImmutableType:

    __metaclass__ = ABCMeta

    """
    A descriptor of a type that may call a validator on setting
    """
    __validation_options__ = []

    @abstractmethod
    def __init__(self, *args, **kwargs):
        pass

    @abstractmethod
    def __get__(self, instance, owner):
        pass

    def __set__(self, instance, value):
        raise RuntimeError("Prestans3 ImmutableTypes should instantiate object attributes at object creation")


class Scalar(ImmutableType):
    pass


class Structure(ImmutableType):
    pass


class Collection(ImmutableType):
    pass


from .number import Number as Number
from .string import String as String
from .integer import Integer as Integer
from .float import Float as Float
from .boolean import Boolean as Boolean
from .date import Date as Date
from .datetime import DateTime as DateTime
from .model import Model as Model
from .time import Time as Time
