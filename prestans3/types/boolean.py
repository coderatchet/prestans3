# -*- coding: utf-8 -*-
"""
    prestans.types.string
    ~~~~~~~~~~~~~~~~~~~~~
    
    A WSGI compliant REST micro-framework.

    :copyright: (c) 2016 Anomaly Software
    :license: Apache 2.0, see LICENSE for more details.
"""

from . import ImmutableType


# http://stackoverflow.com/questions/2172189/why-i-cant-extend-bool-in-python
# noinspection PyAbstractClass
class Boolean(ImmutableType):

    @classmethod
    def from_value(cls, value):
        if isinstance(value, cls):
            return value
        elif value.__class__ is not bool:
            raise TypeError("{} of type {} is not a subclass of {} or a bool".format(value, value.__class__.__name__, cls))
        return Boolean(bool(value))

    def __init__(self, value=False):
        self._value = value
        super(Boolean, self).__init__()

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self._eq_other_instance(other)
        else:
            return self._value is other

    def __ne__(self, other):
        return not self == other

    def __nonzero__(self):
        return self._value

    def __bool__(self):
        return self.__nonzero__()

    def _eq_other_instance(self, other_instance):
        """
        :param Boolean other_instance:
        :return: bool
        """
        return self._value == other_instance._value