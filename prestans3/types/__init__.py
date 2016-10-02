# -*- coding: utf-8 -*-
"""
    prestans3.types
    ~~~~~~~~~~~~~~
    
    A WSGI compliant REST micro-framework.

    :copyright: (c) 2016 Anomaly Software
    :license: Apache 2.0, see LICENSE for more details.
"""
import functools


class PropertyRule(classmethod):
    """
    decorator used for declaring a function as a rule inside an |ImmutableType| subclass. The property rule may then be
    configured as a parameter to :func:`ImmutableType.property()<.ImmutableType.property>`

    for instance, the default property rule ``required`` is defined:

    .. code-block:: python

        class ImmutableType(object):
            @property_rule(name="required")
            def _required(self, instance):
               # verifies whether the instance given is
               # defined on a containing class
               pass

    And may be configured on a subclass of |Structure|:

    >>> import prestans3.types as types
    >>> class MyStringContainingClass(types.Structure)
    ...     string_property = String.property(required=True)
    ...
    >>> my_class = MyStringContainingClass()
    >>> type(my_class.validate())  # prestans3.validation_tree.ValidationTreeNode

    :param function: the function to register as a property. Must accept an instance of the |type| being validated
    :type function: rule(instance : |ImmutableType| or |ImmutableType|) -> bool or |ValidationTree| or |LeafValidationException|
    :returns: the original function
    """

    # noinspection PyMissingConstructor
    def __init__(self, name=None):
        """
        :param str name: name of the Property Rule. for convenience sake, it is recommended that this name should be a
        space free python-like identifier e.g. ``my_property_rule``.
        """
        self._name = name
        pass

    def __call__(self, function):
        self._function = function
        name__ = function.__name__
        # for name in set(dir(function)) - set(dir(self)):
        #     setattr(self, name, getattr(function, name))
        return self._function


class ImmutableType(object):
    """
    Base class of all |types|. Default behaviour of setting an attribute on this class is to throw an
    :class:`AttributeError<builtins.AttributeError>`
    """

    _property_rules = {}

    def __init__(self, validate_immediately=True):
        """
        NOTE: call this method after setting values if validating immediately in order for validation to work!

        if validate_immediately is set, will raise a subclass of |ValidationTreeNode| when initializing the object.
        This is the default behaviour of all immutable types.

        :param bool validate_immediately: whether to validate this object on construction or defer validation to the
                                          user or prestans3 REST api process
        :raises: |ValidationTreeNode|
        """
        if validate_immediately:
            _validation_result = self.validate()
            if _validation_result is not True:  # assumes we have a ValidationTreeNode(Exception) class instance
                raise _validation_result

    @classmethod
    def property(cls, **kwargs):
        """
        :param kwargs: additional configured rules e.g. ``required``, ``default``, etc |hellip|
        :type kwargs: dict
        :return: configured |Property| Class
        :rtype: |Property|
        """
        return Property(of_type=cls, **kwargs)

    __prestans_attribute__ = True

    def validate(self):
        """
        validates against own rules and configured attribute's rules. Scalars will return a |LeafValidationException|
        whilst |Structures| will return a |ValidationTree| with nested |ValidationTreeNode| subclasses

        :rtype: ``True`` or |ValidationTree| or |LeafValidationException|
        """
        # # todo for each attribute property, validate and append any exceptions with namespace to exception set
        # # todo then validate against own configured rules
        # for rule in self._property_rules:
        #     rule(self, )
        # pass

    #
    @classmethod
    def from_value(cls, value, *args, **kwargs):
        """
        returns the wrapped instance of this |type| from a given value. subclasses of |ImmutableType| must override this
        method if prestans should attempt to assign a |Property| to an object other than an instance of this class.

        for a |Structure| containing a |String| |Property|, this will allow an api developer to set the contents of the
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
        argcount = property_rule.__code__.co_argcount
        if argcount != 2:
            func_name = property_rule.__name__
            func_args = property_rule.__code__.co_varnames
            raise ValueError(
                "expected property_rule function with 2 arguments, received function with {} argument(s): {}({})".format(
                    argcount, func_name, ", ".join(func_args)))

        @functools.wraps(property_rule)
        def wrapped_pr(*args):
            result = property_rule(*args)
            # if not isinstance()

        if name is None:
            name = wrapped_pr.__name__
        cls._property_rules.update({name: wrapped_pr})

    @classmethod
    def get_property_rule_by_name(cls, name):
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


class Property(object):
    """
    Base class for all |Property| configurations. not instantiated directly but called from the owning |type|\ 's
    :func:`property()<prestans3.types.ImmutableType.property>` method. A Property is a type descriptor that allows the
    setting of prestans attributes on it's containing class
    """

    # __validation_rules__ = {}  # type: dict[str, (object, T <= ImmutableType) -> True | ValidationExceptionSet ]

    # @classmethod
    # def _required(cls, is_required, instance):
    #     pass
    #
    # @classmethod
    # def _default(cls, default_value, instance):
    #     pass

    def __init__(self, of_type=ImmutableType, **kwargs):
        """
        :param of_type: The class of the |type| being configured. Must be a subclass of |ImmutableType|
        :type of_type: T <= :attr:`ImmutableType.__class__<prestans3.types.ImmutableType>`
        :param dict **kwargs: additional property rule configuration
        """
        self._of_type = of_type
        # if 'required' not in kwargs:
        #     kwargs.update(required=lambda is_required, instance: ImmutableType.Property._required(False, instance))
        # if 'default' not in kwargs:
        #     kwargs.update(default=lambda default_value, instance: ImmutableType.Property._default(None, instance))
        # for _ in kwargs.keys():
        #     pass
        # super(ImmutableType.Property, self).__init__(self)
        # todo return ImmutableType whose validate method will call it's validators curried with it's member values
        pass

    def __set__(self, instance, value):
        """
        If the value provided is not a subclass of the this |Property|\ 's |type|\ , then it is passed to
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
    def property_type(self):
        return self._of_type


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


class Container(ImmutableType):
    """
    subclass of all |types| with containable |attributes|
    """

    # dict[str, func(owner: |ImmutableType|, instance: |ImmutableType|, config: any) -> bool]  # func raises |ValidationTreeNode| on invalidation
    _owner_property_rules = {}

    @classmethod
    def register_owner_property_rule(cls, owner_property_rule, name=None):
        """
        Register an owner type property rule with all instances and subclasses of this |type|

        :param property_rule: callable to be registered
        :type property_rule: rule(owner: T <= Container.__class__, instance: ImmutableType, config: any) -> bool
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
                "expected owner_property_rule function with 3 arguments, received function with {} argument(s): {}({})".format(
                    argcount, func_name, ", ".join(func_args)))

        @functools.wraps(owner_property_rule)
        def wrapped_opr(*args):
            result = owner_property_rule(*args)
            # if not isinstance()

        if name is None:
            name = wrapped_opr.__name__
        cls._owner_property_rules.update({name: wrapped_opr})

    @classmethod
    def get_owner_property_rule_by_name(cls, name):
        """ retrieve the owner property rule by name (``str``) """
        return cls._owner_property_rules[name]


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

    # @classmethod
    # def mutable(cls, *args, **kwargs):
    #     """
    #     return an instance of this class with mutable |attributes|
    #     :param args:
    #     :param kwargs:
    #     :return:
    #     """
    #     pass

    def is_prestans_attribute(self, key):
        """
        Determines if the key provides is a configured |attribute| of this |Structure|\ .

        :param str key:
        :return bool: ``True`` if this is a |attribute| or False if otherwise.
        """
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
        super(Structure, self).__init__()
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


class Iterable(Container):
    # todo construct entire object in __init__
    # todo __setitem__ raises error
    pass


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
