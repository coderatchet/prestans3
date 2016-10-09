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


# noinspection PyAbstractClass
class Array(Container):
    def __init__(self, iterable=None, **kwargs):
        if iterable is None:
            iterable = []
        # todo expand to allow list-like objects
        elif not isinstance(iterable, list) and not isinstance(iterable, tuple):
            raise Exception("iterable is not a list")
        if isinstance(iterable, tuple):
            iterable = list(iterable)
        self._values = iterable
        super(Array, self).__init__(**kwargs)


#### list like magic methods

    def __eq__(self, other):
        if isinstance(other, Array):
            return self._values == other._values
        else:
            return self._values == other

    def __len__(self):
        return len(self._values)

    def __getitem__(self, key):
        # if key is of invalid type or value, the list values will raise the error
        return self._values[key]

    def __setitem__(self, key, value):
        # todo __setitem__ raises error
        raise AttributeError("__setitem__ called on an immutable {class_name}, "
                             "for a mutable array, initialise with {class_name}.mutable()"
                             .format(class_name=self.__name__))

    def __delitem__(self, key):
        del self._values[key]

    def __iter__(self):
        return iter(self._values)

    def __reversed__(self):
        return Array(reversed(self._values))

    def append(self, value):
        self._values.append(value)

    def head(self):
        # get the first element
        return self._values[0]

    def tail(self):
        # get all elements after the first
        return Array(self._values[1:])

    def init(self):
        # get elements up to the last
        return Array(self._values[:-1])

    def last(self):
        # get last element
        return self._values[-1]

    def drop(self, n):
        # get all elements except first n
        return Array(self._values[n:])

    def take(self, n):
        # get first n elements
        return Array(self._values[:n])

#### list like magic methods

# noinspection PyAbstractClass
class _MutableArray(Array):
    # todo __setitem__ should not raise error.
    pass


class ArrayValidationException(ValidationException):
    pass


class ElementValidationExceptionSummary(ValidationExceptionSummary):
    pass
