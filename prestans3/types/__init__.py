# -*- coding: utf-8 -*-
"""
    prestans3.types
    ~~~~~~~~~~~~~~
    
    A WSGI compliant REST micro-framework.

    :copyright: (c) 2016 Anomaly Software
    :license: Apache 2.0, see LICENSE for more details.
"""
import functools


class ImmutableType(object):
    """
    Base class of all |types|. Default behaviour of setting an attribute on this class is to throw an
    :class:`AttributeError<builtins.AttributeError>`
    """

    _property_rules = {}

    def __init__(self, validate_immediately=True):
        """
        NOTE: call this method after setting values if validating immediately in order for validation to work!

        if validate_immediately is set, this may possibly raise a |ValidationException| when initializing the object.
        This is the default behaviour of all immutable types.

        :param bool validate_immediately: whether to validate this object on construction or defer validation to the
                                          user or prestans3 REST api process
        :raises: |ValidationException| on invalid state when validate_immediately is True
        """
        if validate_immediately:
            _validation_result = self.validate()
            if _validation_result is not True:  # assumes we have a ValidationException
                raise _validation_result

    @classmethod
    def property(cls, **kwargs):
        """
        :return: configured |_Property| Class
        :rtype: |_Property|
        """
        return _Property(of_type=cls, **kwargs)

    __prestans_attribute__ = True

    def validate(self):
        """
        validates against own rules and configured attribute's rules.

        :raises: |ValidationException| on invalid state
        :rtype: ``True``
        """
        # # todo then validate against own configured rules
        # for rule in self._property_rules:
        #     rule(self, )
        # pass
        if isinstance(self, Structure):
            from prestans3.errors import ValidationException
            validation_exception = None  # type: ValidationException
            for key, attribute in self.prestans_attributes:
                try:
                    attribute.validate()
                except ValidationException as error:
                    if validation_exception is None:
                        validation_exception = ValidationException(self.__class__, (key, error))
                    else:
                        validation_exception.add_validation_exception(key, error)
            # iterate through own rules
            for property_rule in self._property_rules:
                property_rule(self, )
            if validation_exception is not None:
                return True
            else:
                raise validation_exception  # todo change this, this implementation is incorrect

    #
    @classmethod
    def from_value(cls, value, *args, **kwargs):
        """
        returns the wrapped instance of this |type| from a given value. subclasses of |ImmutableType| must override this
        method if prestans should attempt to assign a |_Property| to an object other than an instance of this class.

        for a |Structure| containing a |String| |_Property|, this will allow an api developer to set the contents of the
        structure to a native python string:

        >>> import prestans3.types as types
        >>> class MyClass(types.Structure):
        ...     name = String.property()
        ...
        >>> my_class = MyClass()
        >>> my_class.name = "jum"

        :param value: an acceptable value according to the |type|\ 's subclass
        :raises NotImplementedError: if called on a subclass that does not override this method
        """
        raise NotImplementedError

    @classmethod
    def register_property_rule(cls, property_rule, name=None):
        """
        Register a property rule with all instances and subclasses of this |type|

        :param property_rule: callable to be registered
        :type property_rule: rule(instance: ImmutableType, config: any) -> bool
        :param str name: name of the property rule as will appear in configuring the property:

        >>> import prestans3.types as types
        >>> class MyClass(Structure):
        ...     pass
        ...
        >>> def my_property_rule(instance, config):  # assuming config is a bool
        ...     pass
        ...
        >>> MyClass.register_property_rule(my_property_rule, name="custom_prop")
        >>> class MyOwningClass(Structure):
        ...     sub_prop = MyClass.property(custom_prop=True)  # should now configure the custom_prop
        """
        arg_count = property_rule.__code__.co_argcount
        if arg_count != 2:
            func_name = property_rule.__name__
            func_args = property_rule.__code__.co_varnames
            raise ValueError(
                "expected property_rule function with 2 arguments, received function with {} argument(s): {}({})".format(
                    arg_count, func_name, ", ".join(func_args)))

        @functools.wraps(property_rule)
        def wrapped_pr(*args):
            result = property_rule(*args)
            # if not isinstance()

        if name is None:
            name = wrapped_pr.__name__
        cls._property_rules.update({name: wrapped_pr})

    @classmethod
    def get_property_rule(cls, name):
        """ retrieve the property rule by name (``str``) """
        return cls._property_rules[name]


def _required(owner, instance, config):
    """
    checks if the instance is not None
    :param instance:
    :param config:
    :return:
    """
    if owner is None:
        raise ValueError("owner instance can't be None")
    if not isinstance(owner, ImmutableType):
        raise ValueError("owner instance is not a subclass of {}".format(ImmutableType.__name__))
    return True if not config else instance is not None


class _Property(object):
    """
    Base class for all |_Property| configurations. not instantiated directly but called from the owning |type|\ 's
    :func:`property()<prestans3.types.ImmutableType.property>` method. A |_Property| is a type descriptor that allows the
    setting of prestans attributes on it's containing class
    """

    def __init__(self, of_type=None, **kwargs):
        """
        :param of_type: The class of the |type| being configured. Must be a subclass of |ImmutableType|
        :type of_type: T <= :attr:`ImmutableType.__class__<prestans3.types.ImmutableType>`
        """
        self._of_type = of_type
        self._rules_config = {}
        # if 'required' not in kwargs:
        #     kwargs.update(required=lambda is_required, instance: _required(True, instance))
        # if 'default' not in kwargs:
        #     kwargs.update(default=lambda default_value, instance: ImmutableType._Property._default(None, instance))
        # for _ in kwargs.keys():
        #     pass
        # todo return ImmutableType whose validate method will call it's validators curried with it's member values

    def __set__(self, instance, value):
        """
        If the value provided is not a subclass of the this |_Property|\ 's |type|\ , then it is passed to
        :func:`.ImmutableType.from_value()` in an attempt to coerce the value to the desired |type|.

        :param instance: the storage for this class' |attributes|\ .
        :type instance: dict[str, |ImmutableType|\ ]
        :param value: a subclass or coercible value of this class's |type|\ .
        :type value: T <= G
        """
        # _prestans_attributes.update()
        print("set value: {}".format(value))
        # if value is a ImmutableType then set it otherwise construct it from variable
        if isinstance(value[1], self._of_type):
            instance[value[0]] = value[1]
        else:
            instance[value[0]] = self._of_type.from_value(value[1])

    def __get__(self, instance, owner):
        """
        :param instance: The instance of this |type|
        :type instance: T <= |ImmutableType|
        :param owner: class type of the instance
        :type owner: any
        :return: the value this descriptor holds
        """
        # my_locals = locals()
        # print("got value: {}".format(instance._value))
        # return instance._value
        return instance

    @property
    def rules_config(self):
        """ contains the configuration for all the |rules| on this |Property| instance """
        return self._rules_config

    @property
    def property_type(self):
        return self._of_type

    def _add_rule_config(self, key, config):
        """ adds a configuration of a property rule to this instance """
        self._rules_config.update({key: config})

    def get_rule_config(self, key):
        return self._rules_config[key]


# noinspection PyAbstractClass
class Scalar(ImmutableType):
    """
    Base type of all |Scalar| |attributes|\ .

    known Subclasses:
        - |Boolean|
        - |Number|
            - |Integer|
            - |Float|
    """
    pass


# noinspection PyAbstractClass
class Container(ImmutableType):
    """ subclass of all |types| with containable |attributes| """

    # dict[str, func(owner: |ImmutableType|, instance: |ImmutableType|, config: any) -> bool]
    # func raises |ValidationException| on invalidation
    _owner_property_rules = {}

    @classmethod
    def register_owner_property_rule(cls, owner_property_rule, name=None):
        """
        Register an owner type property rule with all instances and subclasses of this |type|

        :param owner_property_rule: callable to be registered
        :type owner_property_rule: rule(owner: T <= Container.__class__, instance: ImmutableType, config: any) -> bool
        :param str name: name of the property rule as will appear in configuring the property:

        >>> import prestans3.types as types
        >>> class MyClass(Structure):
        ...     pass
        ...
        >>> def my_owner_property_rule(owner, instance, config):  # assuming config is a bool
        ...     pass
        ...
        >>> MyClass.register_property_rule(my_owner_property_rule, name="custom_owner_prop")
        >>> class MyOwningClass(Structure):
        ...     sub_owner_prop = MyClass.property(custom_owner_prop=True)  # should now configure the custom_prop
        """
        argcount = owner_property_rule.__code__.co_argcount
        if argcount != 3:
            func_name = owner_property_rule.__name__
            func_args = owner_property_rule.__code__.co_varnames
            raise ValueError(
                "expected owner_property_rule function with 3 arguments, received function with {} argument(s): {}({})" \
                    .format(argcount, func_name, ", ".join(func_args)))

        @functools.wraps(owner_property_rule)
        def wrapped_opr(*args):
            result = owner_property_rule(*args)
            # if not isinstance()

        if name is None:
            name = wrapped_opr.__name__
        cls._owner_property_rules.update({name: wrapped_opr})

    @classmethod
    def get_owner_property_rule(cls, name):
        """ retrieve the owner property rule by name (``str``) """
        return cls._owner_property_rules[name]


# noinspection PyAbstractClass
class Structure(Container):
    """
    Base class of complex |types|. may contain other |Structures| and/or |Scalars|.
    """

    def __setattr__(self, key, value):

        """
        This is an immutable type, You should not set values directly through here, set them through the main init
        method.

        i.e. We'll fire you if you override this method. `see_stackoverflow`_

        .. _see_stackoverflow: http://stackoverflow.com/a/2425818/735284
        """
        # todo: added by brad because otherwise an object could not even be instantiated
        if key != "_prestans_attributes":
            raise AttributeError("Prestans3 ImmutableType should instantiate object attributes at object creation")

    def is_prestans_attribute(self, key):
        """
        Determines if the key provides is a configured |attribute| of this |Structure|\ .

        :param str key: name of the attribute
        :return bool: ``True`` if this is a |attribute| or False if otherwise.
        """
        if key in object.__getattribute__(self, '__class__').__dict__ and \
                isinstance(object.__getattribute__(self, '__class__').__dict__[key], _Property):
            return True
        else:
            return False

    def __getattribute__(self, item):
        """
        will use the |_Property|\ 's __get__ method if the item is a |attribute| otherwise retrieves the regular
        python attribute as normal
        """
        if object.__getattribute__(self, 'is_prestans_attribute')(item):
            return object.__getattribute__(self, '__class__').__dict__[item].__get__(
                object.__getattribute__(self, '_prestans_attributes')[item],
                object.__getattribute__(self, '_prestans_attributes')[item].__class__)
        else:
            return object.__getattribute__(self, item)

    def __init__(self, **kwargs):
        super(Structure, self).__init__(**kwargs)
        self._prestans_attributes = {}

    @property
    def prestans_attributes(self):
        """
        returns a dictionary of prestan attribute names to their values

        :rtype: dict[str -> |ImmutableType|\ ]
        """
        return self._prestans_attributes

    def mutable(self):
        class _PrivateMutable(_MutableStructure, self.__class__):
            pass

        return _PrivateMutable()


# noinspection PyAbstractClass
class _MutableStructure(Structure):
    """
    Not instantiated directly, instead call the :func:`.Container.mutable()` method to retrieve an instance of this
    |type| that may be mutated. Validation will now not happen on __init__
    """

    def __setattr__(self, key, value):
        """
        |types| maintain an internal dictionary of attribute names to their values for easy demarcation between prestans
        attributes and native python object attributes. This enables the user to set arbitrary values on the object
        without affecting the final serialization of the object. In other words: regular python properties on an object
        are transient to the client requesting the object.

        :param str key: the name of the attribute or regular python property to set on the object.
        :param value: the value to set on this |MutableStructure|. if the key refers a prestans attribute,
                                             it is stored in the internal :attr:`.Structure._prestans_attributes` store.
                                             otherwise it is stored in the :attr:`.Structure.__dict__` as normal.
        :type value: |ImmutableType| or any
        """
        # if the key being set is a |attribute| then store the value in the self._prestans_attributes dictionary
        if self.is_prestans_attribute(key):
            object.__getattribute__(self, '__class__').__dict__[key].__set__(
                object.__getattribute__(self, '_prestans_attributes'),
                (key, value)
            )
        # else default super behaviour
        else:
            super(_MutableStructure, self).__setattr__(key, value)
        pass

    @classmethod
    def from_immutable(cls, instance):
        class _Mute(_MutableStructure, instance.__class__):
            pass

        pass


# noinspection PyAbstractClass
class Iterable(Container):
    # todo construct entire object in __init__
    # todo __setitem__ raises error
    pass


# noinspection PyAbstractClass
class _MutableIterable(Iterable):
    # todo __setitem__ should not raise error.
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
