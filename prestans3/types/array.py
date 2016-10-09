# -*- coding: utf-8 -*-
"""
    prestans.types.array
    ~~~~~~~~~~~~~~~~~~~~

    A WSGI compliant REST micro-framework.

    :copyright: (c) 2016 Anomaly Software
    :license: Apache 2.0, see LICENSE for more details.
"""

from prestans3.errors import ValidationException, ValidationExceptionSummary
from prestans3.types import Container
from collections import Iterable
from copy import copy


# noinspection PyAbstractClass
class Array(Container):
    def __init__(self, iterable=None, **kwargs):
        if iterable is None:
            iterable = []
        elif not isinstance(iterable, Iterable):
            raise Exception(
                "iterable argument of type {} is not an Iterable object".format(iterable.__class__.__name__))
        self._values = list(iterable)
        super(Array, self).__init__(**kwargs)

    #### list like magic methods

    def __eq__(self, other):
        if isinstance(other, Array):
            return self._values == other._values
        else:
            return self._values == other

    def __ne__(self, other):
        return not self.__eq__(other)

    def __len__(self):
        return len(self._values)

    def __getitem__(self, key):
        # if key is of invalid type or value, the list values will raise the error
        return self._values[key]

    def __setitem__(self, key, value):
        raise AttributeError("__setitem__ called on an immutable {class_name}, "
                             "for a mutable array, initialise with {class_name}.mutable()"
                             .format(class_name=self.__name__))

    def __delitem__(self, key):
        raise AttributeError("__delitem__ called on an immutable {class_name}, "
                             "for a mutable array, initialise with {class_name}.mutable()"
                             .format(class_name=self.__name__))

    def __iter__(self):
        return iter(self._values)

    def __reversed__(self):
        return Array(reversed(self._values), validate_immediately=False)

    def append(self, value):
        self._values.append(value)

    def head(self):
        # get the first element
        return self._values[0]

    def tail(self):
        # get all elements after the first
        return Array(self._values[1:], validate_immediately=False)

    def init(self):
        # get elements up to the last
        return Array(self._values[:-1], validate_immediately=False)

    def last(self):
        # get last element
        return self._values[-1]

    def drop(self, n):
        # get all elements except first n
        return Array(self._values[n:], validate_immediately=False)

    def take(self, n):
        # get first n elements
        return Array(self._values[:n], validate_immediately=False)

    def copy(self):
        return Array(copy(self._values), validate_immediately=False)


# noinspection PyAbstractClass
class _MutableArray(Array):
    # todo __setitem__ should not raise error.
    pass


class ArrayValidationException(ValidationException):
    pass


class ElementValidationExceptionSummary(ValidationExceptionSummary):
    pass
