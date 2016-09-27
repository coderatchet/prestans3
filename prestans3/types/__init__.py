# -*- coding: utf-8 -*-
"""
    prestans.types
    ~~~~~~~~~~~~~~
    
    A WSGI compliant REST micro-framework.

    :copyright: (c) 2016 Anomaly Software
    :license: Apache 2.0, see LICENSE for more details.
"""


def property_rule(function):
    return function


class MutableType(object):
    """
    A descriptor of a type that may call a validator when setting it's value. May also ``repr`` itself as via a
    serializer
    """

    @classmethod
    @property_rule
    def _required(cls, instance):
        pass

    @classmethod
    def property(cls, **kwargs):
        """
        :param kwargs:
         :rtype: ``Property``
        :return: configured Property Class
        """
        return Property(of_type=cls, **kwargs)

    __prestans_attribute__ = True

    # def __init__(self, validate=True):
    #     validation_result = self.validate()
    #     if isinstance(validation_result, ValidationExceptionSet):
    #         pass
    #     pass
    #
    def validate(self):
        """
        validates against own rules and configured attribute's rules
        :return: ``True`` if the validation succeeded or ``ValidationExceptionSet`` if the validation failed
        :rtype: True | prestans3.validation_tree.ValidationTree
        """
        # todo for each attribute property, validate and append any exceptions with namespace to exception set
        # todo then validate against own configured rules
        pass
    #
    @classmethod
    def from_value(cls, value, *args, **kwargs):
        """
        returns the wrapped instance of the Type from a given value
        :param value:
        :return:
        """
        raise NotImplementedError


class Property(object):

    # __validation_rules__ = {}  # type: dict[str, (object, T <= MutableType) -> True | ValidationExceptionSet ]

    # @classmethod
    # def _required(cls, is_required, instance):
    #     pass
    #
    # @classmethod
    # def _default(cls, default_value, instance):
    #     pass

    def __init__(self, of_type=MutableType, **kwargs):
        self._of_type = of_type
        # if 'required' not in kwargs:
        #     kwargs.update(required=lambda is_required, instance: MutableType.Property._required(False, instance))
        # if 'default' not in kwargs:
        #     kwargs.update(default=lambda default_value, instance: MutableType.Property._default(None, instance))
        # for _ in kwargs.keys():
        #     pass
        # super(ImmutableType.Property, self).__init__(self)
        # todo return ImmutableType whose validate method will call it's validators curried with it's member values
        pass

    def __set__(self, instance, value):
        # _prestans_attributes.update()
        print("set value: {}".format(value))
        # if value is a MutableType then set it otherwise construct it from variable
        if isinstance(value[1], self._of_type):
            instance[value[0]] = value[1]
        else:
            instance[value[0]] = self._of_type.from_value(value[1])

    def __get__(self, instance, owner):
        """

        :param instance: instance to retrieve value from
        :param owner: class type of the instance
        :type owner: T
        :return: the value this descriptor describes
        """
        # my_locals = locals()
        # print("got value: {}".format(instance._value))
        # return instance._value
        return instance

    @property
    def property_type(self):
        return self._of_type

class ImmutableType(MutableType):
    def __setattr__(self, key, value):
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
        raise AttributeError("Prestans3 ImmutableType should instantiate object attributes at object creation")


class Scalar(MutableType):
    pass


class Structure(MutableType):
    def __setattr__(self, key, value):
        # if the key being set is a prestans attribute then store the value in the self._prestans_attributes dictionary
        if self.is_prestans_attribute(key):
            object.__getattribute__(self, '__class__').__dict__[key].__set__(
                object.__getattribute__(self, '_prestans_attributes'),
                (key, value)
            )
        # else default super behaviour
        else:
            super(Structure, self).__setattr__(key, value)
        pass

    def is_prestans_attribute(self, key):
        if key in object.__getattribute__(self, '__class__').__dict__ and \
                isinstance(object.__getattribute__(self, '__class__').__dict__[key], Property):
            return True
        else:
            return False

    def __getattribute__(self, item):
        if object.__getattribute__(self, 'is_prestans_attribute')(item):
            return object.__getattribute__(self, '__class__').__dict__[item].__get__(
                object.__getattribute__(self, '_prestans_attributes')[item],
                object.__getattribute__(self, '_prestans_attributes')[item].__class__)
        else:
            return object.__getattribute__(self, item)

    def __init__(self):
        self._prestans_attributes = {}

    # contains other scalars
    pass


class Collection(MutableType):
    pass


from .boolean import Boolean as Boolean
from .number import Number as Number
from .integer import Integer as Integer
from .float import Float as Float
from .model import Model as Model
from .p_date import Date as Date
from .p_datetime import DateTime as DateTime
from .string import String as String
from .time import Time as Time

