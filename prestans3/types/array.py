# -*- coding: utf-8 -*-
"""
    prestans.types.array
    ~~~~~~~~~~~~~~~~~~~~

    A WSGI compliant REST micro-framework.

    :copyright: (c) 2016 Anomaly Software
    :license: Apache 2.0, see LICENSE for more details.
"""
from collections import Iterable
from copy import copy

from prestans3.errors import ValidationException, ValidationExceptionSummary, AccessError
from prestans3.types import Container, ImmutableType
from prestans3.utils import inject_class


def find_first(array, func):
    """
    return the index of the first occurence of item in array that fulfils func

    :param iterable array: iterable to check for condition
    :param func: a function that accepts an element of the array and returns a true when condition is met
    :type func: (any) -> bool
    """
    array = list(array)
    for i in range(len(array)):
        if not func(array[i]):
            return i
    return -1


# noinspection PyAbstractClass
class Array(Container):
    def __init__(self, of_type, iterable=None, **kwargs):
        if iterable is None:
            iterable = []
        if not isinstance(of_type, type):
            raise TypeError("of_type must be a subclass of {} type object, received {}".format(ImmutableType.__name__,
                                                                                               of_type.__class__.__name__))
        elif not issubclass(of_type, ImmutableType):
            raise TypeError("of_type must be a subclass of {} type object, received {}".format(ImmutableType.__name__,
                                                                                               of_type.__name__))
        if not isinstance(iterable, Iterable):
            raise TypeError(
                "iterable argument of type {} is not an Iterable object".format(iterable.__class__.__name__))
        self._of_type = of_type
        coerced_iterable = []

        def _check_and_store(item):
            try:
                coerced_iterable.append(of_type.from_value(item))
                return True
            except TypeError:
                return False

        first_error_index = find_first(iterable, _check_and_store)
        if first_error_index > -1:
            raise ValueError(self.__class__, 'in Array.__init__, iterable[{}] is {} '
                                             'but the declared type of this array is {}'.format(
                first_error_index, iterable[first_error_index], of_type.__name__))
        self._values = list(coerced_iterable)
        super(Array, self).__init__(**kwargs)

    @classmethod
    def mutable(cls, of_type, iterable=None, **kwargs):
        if cls is Array:
            return _MutableArray(of_type, iterable, **kwargs)
        new_mutable_model_subclass = inject_class(cls, _MutableArray, Array,
                                                  new_type_name_func=lambda x, _y, _z: "PMutable{}".format(
                                                      x.__name__))
        return new_mutable_model_subclass(**kwargs)

    #### list like magic methods

    def __eq__(self, other):
        if isinstance(other, Array):
            return self._values == other._values
        else:
            zipped = zip(self, other)
            for one, two in zipped:
                if (one is None) != (two is None):
                    return False
                else:
                    try:
                        _coerced = self._of_type.from_value(two)
                        if one != _coerced:
                            return False
                    except TypeError:
                        return False
        return True





    def __ne__(self, other):
        return not self.__eq__(other)

    def __len__(self):
        return len(self._values)

    def __getitem__(self, key):
        # if key is of invalid type or value, the list values will raise the error
        return self._values[key]

    def __setitem__(self, key, value):
        raise AccessError(self.__class__, "__setitem__ called on an immutable {class_name}, "
                                          "for a mutable array, initialise with {class_name}.mutable()"
                          .format(class_name=self.__class__.__name__))

    def __delitem__(self, key):
        raise AccessError(self.__class__, "__delitem__ called on an immutable {class_name}, "
                                          "for a mutable array, initialise with {class_name}.mutable()"
                          .format(class_name=self.__class__.__name__))

    def __iter__(self):
        return iter(self._values)

    def __reversed__(self):
        return Array(self._of_type, reversed(self._values), validate_immediately=False)

    def append(self, item):
        raise AccessError(self.__class__, "append called on an immutable {class_name}, "
                                          "for a mutable array, initialise with {class_name}.mutable()"
                          .format(class_name=self.__class__.__name__))

    def head(self):
        # get the first element
        return self._values[0]

    def tail(self):
        # get all elements after the first
        return Array(self._of_type, self._values[1:], validate_immediately=False)

    def init(self):
        # get elements up to the last
        return Array(self._of_type, self._values[:-1], validate_immediately=False)

    def last(self):
        # get last element
        return self._values[-1]

    def drop(self, n):
        # get all elements except first n
        return Array(self._of_type, self._values[n:], validate_immediately=False)

    def take(self, n):
        # get first n elements
        return Array(self._of_type, self._values[:n], validate_immediately=False)

    def copy(self):
        return Array(self._of_type, copy(self._values), validate_immediately=False)


# noinspection PyAbstractClass
class _MutableArray(Array):
    def __setitem__(self, key, value):
        self._values[key] = self._of_type.from_value(value)

    def append(self, value):
        if not isinstance(value, self._of_type):
            try:
                value = self._of_type.from_value(value)
            except:
                raise ValueError(
                    "value is not an instance of {}, one of its subclasses or a coercable type: received value type: {}"
                        .format(self._of_type.__name__, value.__class__.__name__))
        self._values.append(value)


class ArrayValidationException(ValidationException):
    pass


class ElementValidationExceptionSummary(ValidationExceptionSummary):
    pass
