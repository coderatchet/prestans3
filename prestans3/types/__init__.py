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

    """
    A descriptor of a type that may call a validator when setting it's value. May also ``repr`` itself as via a
    serializer
    """

    __metaclass__ = ABCMeta
    __validation_rules__ = []
    __prestans_attribute__ = True

    def __init__(self):
        pass

    @abstractmethod
    def __get__(self, instance, owner):
        pass

    # We'll fire you if you override this method.
    # http://stackoverflow.com/questions/2425656/how-to-prevent-a-function-from-being-overridden-in-python
    def __set__(self, instance, value):
        """
        This is an immutable type, You should not set values directly through here, set them through the main init
        method.

        i.e. We'll fire you if you override this method. `see_stackoverflow`_

        .. _see_stackoverflow: http://stackoverflow.com/a/2425818/735284
        :param instance: the instance whose attribute is being set
        :type instance: object
        :param value:
        :return:
        """
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
from .p_date import Date as Date
from .p_datetime import DateTime as DateTime
from .model import Model as Model
from .time import Time as Time
