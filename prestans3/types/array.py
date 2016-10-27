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

from prestans3.errors import ValidationException, AccessError, ContainerValidationException
from prestans3.types import Container, ImmutableType, _Property
from prestans3.utils import inject_class, MergingProxyDictionary

# py2to3 remove try, prefer builtins
try:
    from __builtin__ import property as prop
except ImportError:
    from builtins import property as prop


def find_first(array, func):
    """
    return the index of the first occurence of item in array that fulfils func

    :param iterable array: iterable to check for condition
    :param func: a function that accepts an element of the array and returns a true when condition is met
    :type func: (any) -> bool
    """
    array = array if hasattr(array, '__getitem__') and hasattr(array, '__len__') else list(array)
    for i in range(len(array)):
        if not func(array[i]):
            return i
    return -1


# noinspection PyAbstractClass
class Array(Container):
    """
    Prestans 3 Array type. Wraps a native python list and delegates most operations to it. Provides Prestans 3
    functionality such as serialization and validation.

    Note: Validation will stop at the first error by default.
    """

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
                "iterable argument of type {} is not an iterable object".format(iterable.__class__.__name__))
        self._of_type = of_type
        if isinstance(iterable, self.__class__):
            if not issubclass(iterable._of_type, self._of_type):
                raise TypeError("element type '{}' of iterable is not a subclass of element type '{}' of self".format(
                    iterable._of_type.__name__, self._of_type.__name__))
        coerced_iterable = []

        def _check_and_store(item):
            try:
                coerced_iterable.append(of_type.from_value(item))
                return True
            except TypeError:
                return False

        iterable = list(iterable)
        first_error_index = find_first(iterable, _check_and_store)
        if first_error_index > -1:
            raise ValueError(self.__class__, 'in Array.__init__, iterable[{}] is {} of type {}, '
                                             'but the declared type of this array is {}'.format(
                first_error_index, iterable[first_error_index], iterable[first_error_index].__class__.__name__,
                of_type.__name__))
        self._values = list(coerced_iterable)
        super(Array, self).__init__(**kwargs)

    @classmethod
    def from_value(cls, value):
        try:
            return super(Array, cls).from_value(value)
        except NotImplementedError:
            raise NotImplementedError(
                '{class_name} must declare an explicit element type, create an array from an existing native ' +
                'array using the constructor: {class_name}(<type>, native_array)'.format(class_name=cls.__name__))

    @classmethod
    def mutable(cls, of_type, iterable=None, **kwargs):
        if cls is Array:
            return _MutableArray(of_type, iterable, **kwargs)
        new_mutable_model_subclass = inject_class(cls, _MutableArray, Array,
                                                  new_type_name_func=lambda x, _y, _z: "PMutable{}".format(
                                                      x.__name__))
        return new_mutable_model_subclass(cls, **kwargs)

    @classmethod
    def property(cls, element_type, element_rules=None, **kwargs):
        """
        :return: configured |_Property| Class
        :rtype: |_Property|
        """
        return _ArrayProperty(of_type=cls, element_type=element_type, element_rules=element_rules, **kwargs)

    def validate(self, config=None):
        """
        this validate will check all of it's elements, then check the global element rule config set on the array, then
        check any validation on the array itself. by default, the first element in this array to have a validation error
        will stop the validation checks on elements and return with a message.

        :param config: the rule configuration for this array and its elements
        :raises ValidationException: if there are invalid contents or the array itself is invalid according to the given
                                     config
        """
        validation_exception = None
        _index = 0
        element_rules = {}
        if config is None:
            array_rules = {}
        else:
            array_rules = {key: config for key, config in list(config.items()) if key != 'element_rules'}
            if 'element_rules' in config:
                element_rules = config['element_rules']
        try:
            for index, element in enumerate(self._values):  # type: ImmutableType
                _index = index
                element.validate(element_rules)
        except ValidationException as exception:
            if not validation_exception:
                validation_exception = ArrayValidationException(self.__class__)
            validation_exception.add_validation_exception('{}[{}]'.format(self.__class__.__name__, _index), exception)
        try:
            super(Array, self).validate(array_rules)
        except ValidationException as exception:
            if not validation_exception:
                validation_exception = ArrayValidationException(self.__class__)
            validation_exception.add_validation_messages(exception.messages)
        if validation_exception:
            raise validation_exception

    @prop
    def native_value(self):
        return [value.native_value for value in self]

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
        """ append an element to the array """
        raise AccessError(self.__class__, "append called on an immutable {class_name}, "
                                          "for a mutable array, initialise with {class_name}.mutable()"
                          .format(class_name=self.__class__.__name__))

    def head(self):
        """ get the first element """
        return self._values[0]

    def tail(self):
        """ get all elements after the first """
        return Array(self._of_type, self._values[1:], validate_immediately=False)

    def init(self):
        """ get elements up to the last """
        return Array(self._of_type, self._values[:-1], validate_immediately=False)

    def last(self):
        """ get last element """
        return self._values[-1]

    def drop(self, n):
        """ get all elements except first n """
        return Array(self._of_type, self._values[n:], validate_immediately=False)

    def take(self, n):
        """ get first n elements """
        return Array(self._of_type, self._values[:n], validate_immediately=False)

    def copy(self):
        """ create a copy of the array """
        return Array(self._of_type, copy(self._values), validate_immediately=False)


def _min_length(instance, config):
    length = len(instance)
    if length < config:
        raise ValidationException(instance.__class__,
                                  "{} instance length is {}, the minimum configured length is {}".format(
                                      instance.__class__.__name__, length, config))


def _max_length(instance, config):
    length = len(instance)
    if length > config:
        raise ValidationException(instance.__class__,
                                  "{} instance length is {}, the maximum configured length is {}".format(
                                      instance.__class__.__name__, length, config))


Array.register_property_rule(_min_length, name="min_length")
Array.register_property_rule(_max_length, name="max_length")


class _ArrayProperty(_Property):
    """
    allows for property rule configuration that checks all elements
    """

    def __init__(self, of_type, element_type, element_rules=None, **kwargs):
        super(_ArrayProperty, self).__init__(of_type, **{key: config for key, config in list(kwargs.items()) if
                                                         key in ['required', 'default']})
        self._element_type = element_type
        self._element_rules_config = element_rules if element_rules is not None else {}
        self._rules_config = MergingProxyDictionary({'element_rules': element_rules},
                                                    self._get_and_check_rules_config(kwargs),
                                                    of_type.default_rules_config())

    def __set__(self, instance, value):
        """
        :param instance:
        :type instance: any coercible type of self._of_type provided by __init__ function
        :param value:
        :type value: tuple
        :return:
        """
        if isinstance(value[1], self._of_type):
            super(_ArrayProperty, self).__set__(instance, value)
        elif hasattr(value, '__getitem__'):
            super(_ArrayProperty, self).__set__(instance, (value[0], Array(self._element_type, value[1])))

    def _get_and_check_rule_config(self, key, config):
        try:
            key, config = super(_ArrayProperty, self)._get_and_check_rule_config(key, config)
            return key, config
        except ValueError:
            if key not in self._element_type.property_rules:
                raise ValueError(
                    "'{key}={config}' config in {array_class_name}.__init__ was neither a property rule of " +
                    "'{array_class_name}' or a property rule of the element type '{element_type_name}'".format(
                        key=key, config=config, array_class_name=self._of_type.__name__,
                        element_type_name=self._element_type.__name__))
            else:
                return key, config


# noinspection PyAbstractClass
class _MutableArray(Array):
    def __setitem__(self, key, value):
        self._values[key] = self._of_type.from_value(value)

    def __delitem__(self, key):
        del self._values[key]

    def append(self, value):
        if not isinstance(value, self._of_type):
            try:
                value = self._of_type.from_value(value)
            except:
                raise ValueError(
                    "value is not an instance of {}, one of its subclasses or a coercable type: received value type: {}"
                        .format(self._of_type.__name__, value.__class__.__name__))
        self._values.append(value)


class ArrayValidationException(ContainerValidationException):
    def check_validation_exception(self, key, validation_exception):
        super(ArrayValidationException, self).check_validation_exception(key, validation_exception)
