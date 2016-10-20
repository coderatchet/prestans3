# -*- coding: utf-8 -*-
"""
    prestans3.types
    ~~~~~~~~~~~~~~~
    
    A WSGI compliant REST micro-framework.

    :copyright: (c) 2016 Anomaly Software
    :license: Apache 2.0, see LICENSE for more details.
"""
import functools

from prestans3.errors import PropertyConfigError, ValidationException
from prestans3.utils import with_metaclass, MergingProxyDictionary, LazyOneWayGraph, ImmutableMergingDictionary, is_str


class _PropertyRulesProperty(object):
    # noinspection PyUnusedLocal
    def __get__(self, cls, _mcs):
        return _property_rule_graph[cls]


class _ConfigChecksProperty(object):
    # noinspection PyUnusedLocal
    def __get__(self, cls, _mcs):
        return _config_check_graph[cls]


class _PrepareFunctionsProperty(object):
    # noinspection PyUnusedLocal
    def __get__(self, cls, _mcs):
        return _prepare_functions_graph[cls]


class _PrestansTypeMeta(type):
    property_rules = _PropertyRulesProperty()  # type: dict[str, (T <= ImmutableType, any) -> None]
    config_checks = _ConfigChecksProperty()  # type: dict[str, (type, any) -> None]
    prepare_functions = _PrepareFunctionsProperty()  # type: dict[str, (T <= ImmutableType) -> T]


class ImmutableType(with_metaclass(_PrestansTypeMeta, object)):
    """
    Base class of all |types|. Default behaviour of setting an attribute on this class is to throw an
    :class:`AttributeError<builtins.AttributeError>`

    Attributes:
        property_rules  registered property rules for this |type|
        is_scalar       informs whether the class is a scalar type object or otherwise

                        known Scalars
                        -------------
                        - |Boolean|
                        - |Number|
                            - |Integer|
                            - |Float|
                        - |String|
                        - |Date|
                        - |DateTime|
                        - |Time|
    """

    is_scalar = True

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
            self.validate()

    @classmethod
    def property(cls, **kwargs):
        """
        :return: configured |_Property| Class
        :rtype: |_Property|
        """
        return _Property(of_type=cls, **kwargs)

    __prestans_attribute__ = True

    def validate(self, config=None):
        """
        validates against own |rules| and configured |attribute|\ 's rules.

        :raises: |ValidationException| on invalid state
        """
        if config is None:
            config = {}
        config = ImmutableMergingDictionary(config, self.default_rules_config())
        exception_messages = None
        for rule_name, rule in list(self.__class__.property_rules.items()):
            try:
                if rule_name in config:
                    rule(self, config[rule_name])
            except ValidationException as ex:
                if exception_messages is None:
                    exception_messages = []
                exception_messages += ex.messages
            if exception_messages:
                exception = ValidationException(self.__class__)
                exception.add_validation_messages(exception_messages)
                raise exception

    @classmethod
    def from_value(cls, value):
        """
        returns the wrapped instance of this |type| from a given value. subclasses of |ImmutableType| must override this
        method if prestans should attempt to assign a |_Property| to an object other than an instance of this class.

        for a |Model| containing a |String| |_Property|, this will allow an api developer to set the contents of the
        |String| |type| to a native python ``str``:

        >>> import prestans3.types as types
        >>> class MyClass(types.Model):
        ...     name = String.property()
        ...
        >>> my_class = MyClass.mutable()
        >>> my_class.name = "jum"

        :param value: an acceptable value according to the |type|\ 's subclass
        :raises NotImplementedError: if called on a subclass that does not override this method
        """
        if isinstance(value, cls):
            return value
        raise NotImplementedError

    # noinspection PyUnusedLocal,PyAbstractClass
    @classmethod
    def register_property_rule(cls, property_rule, name=None, default=None, configurable=True):
        """
        Register a |rule| with all instances and subclasses of this |type|

        :param property_rule: callable to be registered
        :type property_rule: rule(instance: ImmutableType, config: any) -> bool
        :param str name: name of the |rule| as will appear in configuring the property:
        :param object default: the default configuration to apply to this |rule| if none is specified
        :param bool configurable: when ``False``, adding a rule configuration for this property will throw an error

        >>> import prestans3.types as types
        >>> class MyClass(Model):
        ...     pass
        ...
        >>> def my_property_rule(instance, config):  # assuming config is a bool
        ...     pass
        ...
        >>> MyClass.register_property_rule(my_property_rule, name="custom_prop")
        >>> class MyOwningClass(Model):
        ...     sub_prop = MyClass.property(custom_prop=True)  # should now configure the custom_prop
        """
        arg_count = property_rule.__code__.co_argcount
        if arg_count != 2:
            func_name = property_rule.__name__
            func_args = property_rule.__code__.co_varnames
            raise ValueError(
                "expected property_rule function with 2 arguments, "
                "received function with {} argument(s): {}({})".format(arg_count, func_name, ", ".join(func_args)))

        @functools.wraps(property_rule)
        def wrapped_pr(*args):
            result = property_rule(*args)
            return result
            # if not isinstance()

        wrapped_pr.default_config = default
        wrapped_pr.configurable = configurable
        if name is None:
            name = wrapped_pr.__name__
        cls.property_rules[name] = wrapped_pr

    @classmethod
    def register_config_check(cls, config_check, name=None):
        arg_count = config_check.__code__.co_argcount
        if arg_count != 2:
            func_name = config_check.__name__
            func_args = config_check.__code__.co_varnames
            raise ValueError(
                "expected property_rule function with 2 arguments, "
                "received function with {} argument(s): {}({})".format(arg_count, func_name, ", ".join(func_args)))
        if name is None:
            name = config_check.__name__
        cls.config_checks[name] = config_check

    @classmethod
    def get_property_rule(cls, name):
        """ retrieve the |rule| by name (``str``) """
        return cls.property_rules[name]

    @classmethod
    def default_rules_config(cls):
        """
        returns any rule_names paired with their default configuration. If no default is present, then no pair is
        produced.

        :return: dict (str -> any)
        """
        return {rule_name: rule.default_config if not callable(rule.default_config) else rule.default_config()
                for rule_name, rule in list(cls.property_rules.items()) if rule.default_config}

    @classmethod
    def register_prepare_function(cls, func, name=None):
        cls.prepare_functions[name] = func


_property_rule_graph = LazyOneWayGraph(ImmutableType)
_config_check_graph = LazyOneWayGraph(ImmutableType)
_prepare_functions_graph = LazyOneWayGraph(ImmutableType)


def _choices(instance, config):
    if instance not in config:
        raise ValidationException(instance.__class__,
                                  "{} property is {}, valid choices are [{}]"
                                  .format(instance.__class__.__name__, instance,
                                          ", ".join([str(item) for item in config])))


ImmutableType.register_property_rule(_choices, name="choices")


class _Property(object):
    """
    Base class for all |_Property| configurations. not instantiated directly but called from the owning |type|\ 's
    :func:`property()<prestans3.types.ImmutableType.property>` method. A |_Property| is a type descriptor that allows
    the setting of prestans attributes on it's containing class
    """

    def __init__(self, of_type, required=True, default=None, prepare=None, **kwargs):
        """
        :param of_type: The class of the |type| being configured. Must be a subclass of |ImmutableType|
        :type of_type: T <= :attr:`ImmutableType.__class__<prestans3.types.ImmutableType>`
        """
        self._of_type = of_type
        self._rules_config = MergingProxyDictionary(self._get_and_check_rules_config(kwargs),
                                                    of_type.default_rules_config())
        self.required = required
        self.default = default
        self.prepare = prepare if prepare is not None else []

    def __set__(self, instance, value):
        """
        If the value provided is not a subclass of the this |_Property|\ 's |type|\ , then it is passed to
        :func:`.ImmutableType.from_value()` in an attempt to coerce the value to the desired |type|.

        :param instance: the storage for this class' |attributes|\ .
        :type instance: dict[str, |ImmutableType|\ ]
        :param value: a subclass or coercible value of this class's |type|\ .
        :type value: T <= G
        """
        # if value is a ImmutableType then set it otherwise construct it from variable
        prepared_value = self.prepare_process_function(value[1])
        if isinstance(value[1], self._of_type):
            instance[value[0]] = prepared_value
        else:
            instance[value[0]] = self._of_type.from_value(prepared_value)

    # noinspection PyUnusedLocal
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
        if instance is None and self.default:
            return self.default
        return instance

    @property
    def rules_config(self):
        """ contains the configuration for all the |rules| on this |_Property| instance """
        return self._rules_config

    @property
    def property_type(self):
        """
        :return: T <= :attr:`ImmutableType.__class__<prestans3.types.ImmutableType>`
        """
        return self._of_type

    def _get_and_check_rule_config(self, key, config):
        """
        adds a configuration of a |rule| to this instance

        :raises ValueError: if the key is not registered property rule name on this property_type
        :raises PropertyConfigError: if the property rule is a non-configurable property
        """
        try:
            _rule = self.property_type.get_property_rule(key)
        except KeyError:
            if key in ['required', 'default']:
                return key, config
            else:
                raise ValueError("{} is not a registered rule of type {}".format(key, self.property_type.__name__))
        if not _rule.configurable:
            raise PropertyConfigError(self.property_type, key,
                                      "{} is a non-configurable rule in class {}, (see {}.{}()))"
                                      .format(key, self.property_type.__name__, ImmutableType.__name__,
                                              ImmutableType.register_property_rule.__name__))
        return key, config

    def get_rule_config(self, key):
        """ find a |rule|\ 's configuration by its name """
        return self._rules_config[key]

    @property
    def config_checks(self):
        return self._of_type.config_checks

    def _get_and_check_rules_config(self, kwargs):
        """
        merge default rule configs with explicit rule configs in kwargs

        :param dict kwargs:
        """

        def _gen():
            for key, config in list(kwargs.items()):
                yield self._get_and_check_rule_config(key, config)

        all_config = {checked_key: checked_config for checked_key, checked_config in list(_gen())}
        for key, config_check in list(self.config_checks.items()):
            config_check(self._of_type, all_config)
        return all_config

    @property
    def prepare_process_function(self):
        """
        Return the aggregated process chain function that will iterate through configured prepare parameter from the
        init function. it will honour the order of arguments in the list and produce a resulting object that must be of
        the same type as its input, otherwise an error will be raised

        :return: a function that will process the string
        """

        """ recursively resolves and calls prepare functions in order """
        if not is_str(self.prepare) and hasattr(self.prepare, '__iter__') and hasattr(self.prepare, '__len__'):
            return self._aggregate_prepare_functions(self.prepare)
        else:
            return self._resolve_prepare_function(self.prepare)

    def _aggregate_prepare_functions(self, rest):
        def _all(x, tail):
            if len(tail) < 1:
                return x
            return _all(self._resolve_prepare_function(tail[0])(x), tail[1:])

        return lambda x: _all(x, rest)

    def _resolve_prepare_function(self, str_or_func):
        """
        Will resolve a string into the named function stored in self.__class__.prepare_functions dictionary and throw an
        error on no resolution or will return the function provided given it accepts only one argument

        :param str_or_func: name of a predefined and registered prepare function or a custom function with one argument
                            that returns the same type.
        :type str_or_func: str or (t: T <= ImmutableType) -> T
        :raises TypeError: if the provided function has 0 or more than 1 argument
        :raises KeyError: if the provided string does not map to a pre-registered prepare function on this property's
                          type
        :return: (t: T <= ImmutableType) -> T
        """
        if is_str(str_or_func):
            try:
                return self.property_type.prepare_functions[str_or_func]
            except KeyError:
                raise KeyError(
                    "'{}' is not a registered prepare function of {}".format(str_or_func, self.property_type.__name__))
        if callable(str_or_func):
            if str_or_func.__code__.co_argcount != 1:
                raise TypeError(
                    'provided prepare function should only 1 argument, received function has {}: {}({})'.format(
                        str_or_func.__code__.co_argcount, str_or_func.__name__,
                        ", ".join(str_or_func.__code__.co_varnames)
                    ))
            return str_or_func
        else:
            raise TypeError("prepare argument to property must be a str name of a pre-registered prepare function, a" +
                            "custom one-argument function or a list of any of the previous values, " +
                            "received: {} of type {}".format(str_or_func, str_or_func.__class__.__name__))


# noinspection PyAbstractClass
class Container(ImmutableType):
    """ subclass of all |types| with containable |attributes| """

    is_scalar = False

    # dict[str, func(owner: |ImmutableType|, instance: |ImmutableType|, config: any) -> bool]
    # func raises |ValidationException| on invalidation


from .boolean import Boolean as Boolean
from .number import Number as Number
from .integer import Integer as Integer
from .float import Float as Float
from .string import String as String
from .model import Model as Model
from .array import Array as Array
from .p_date import Date as Date
from .p_datetime import DateTime as DateTime
from .p_time import Time as Time
