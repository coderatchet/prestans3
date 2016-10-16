# -*- coding: utf-8 -*-
"""
    prestans3.types
    ~~~~~~~~~~~~~~~
    
    A WSGI compliant REST micro-framework.

    :copyright: (c) 2016 Anomaly Software
    :license: Apache 2.0, see LICENSE for more details.
"""
import functools

from prestans3.utils import with_metaclass, MergingProxyDictionary


class _MergingDictionaryWithMutableOwnValues(MergingProxyDictionary):
    """
        |MergingProxyDictionary| that has reference to read-only dictionary values whilst still being able to mutate
        own values.
    """

    def __init__(self, dictionary=None):
        """
        :param MergingProxyDictionary dictionary: the read-only inherited values
        """
        self._own_values = {}
        if dictionary is None:
            dictionary = {}
        self._inherited_values = dictionary
        super(_MergingDictionaryWithMutableOwnValues, self).__init__(self._own_values, self._inherited_values)

    def __setitem__(self, key, value):
        """ allows for setting own values (not inherited values)"""
        self._own_values[key] = value

    def update(self, other=None, **kwargs):
        def _update(other):
            if 'keys' in other.__class__.__dict__:
                [self._own_values.__setitem__(k, other[k]) for k in other]
            else:
                [self._own_values.__setitem__(k, v) for k, v in list(other.items())]

        if other:
            _update(other)
        for k, v in list(kwargs.items()):
            self[k] = v

    def is_own_key(self, key):
        return key in self._own_values


class _LazyOneWayGraph(dict):
    def __init__(self, terminating_type=None, **kwargs):
        if terminating_type is None:
            terminating_type = object
        self._terminating_type = terminating_type
        super().__init__(**kwargs)

    def __missing__(self, of_type):
        """
        lazily sets and returns the initialized dictionary values for each |type|\ . Each type will have it's own
        mutable values whilst maintaining a proxied read-only reference to it's base class's values using the
        |MergingProxyDictionary| \.
        :param prestans_type: the |type| to find the value for
        :type prestans_type: T <= |ImmutableType|
        :return: the newly instantiated dictionary of property_rules with read-only references to the |type|\ 's base
                 class value on this graph.
        """
        merging_proxy_dictionary = MergingProxyDictionary(*[self[base]
                                                            for base in of_type.__bases__ if
                                                            issubclass(base, self._terminating_type)])
        self[of_type] = _MergingDictionaryWithMutableOwnValues(merging_proxy_dictionary)
        return self[of_type]


class _PropertyRules(object):
    # noinspection PyUnusedLocal
    def __get__(self, cls, _mcs):
        return _property_rule_graph[cls]


class _PrestansTypeMeta(type):
    property_rules = _PropertyRules()


class ImmutableType(with_metaclass(_PrestansTypeMeta, object)):
    """
    Base class of all |types|. Default behaviour of setting an attribute on this class is to throw an
    :class:`AttributeError<builtins.AttributeError>`

    Attributes:
        property_rules  registered property rules for this |type|
    """

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

        # iterate through own rules
        exception_messages = []
        if config is None:
            config = {}
        from prestans3.errors import ValidationException
        for rule_name, rule in list(self.__class__.property_rules.items()):
            try:
                if rule_name in config:
                    rule(self, config[rule_name])
                elif rule.default_config:
                    rule(self, rule.default_config)
            except ValidationException as ex:
                exception_messages += ex.messages
        if exception_messages:
            this_type_exception = ValidationException(self.__class__)
            this_type_exception.add_validation_messages(exception_messages)
            raise this_type_exception

    #
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
        >>> my_class = MyClass()
        >>> my_class.name = "jum"

        :param value: an acceptable value according to the |type|\ 's subclass
        :raises NotImplementedError: if called on a subclass that does not override this method
        """
        raise NotImplementedError

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
                "expected property_rule function with 2 arguments, received function with {} argument(s): {}({})".format(
                    arg_count, func_name, ", ".join(func_args)))

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
        return {rule_name: rule.default_config for rule_name, rule in list(cls.property_rules.items())
                if rule.default_config}


_property_rule_graph = _LazyOneWayGraph(ImmutableType)


class _Property(object):
    """
    Base class for all |_Property| configurations. not instantiated directly but called from the owning |type|\ 's
    :func:`property()<prestans3.types.ImmutableType.property>` method. A |_Property| is a type descriptor that allows the
    setting of prestans attributes on it's containing class
    """

    @property
    def property_rules(self):
        return [lambda x, this=self: rule(x, this.get_rule_config(key)) for (key, rule) in
                list(self._of_type.property_rules.items())]

    def __init__(self, of_type, required=True, default=None, **kwargs):
        """
        :param of_type: The class of the |type| being configured. Must be a subclass of |ImmutableType|
        :type of_type: T <= :attr:`ImmutableType.__class__<prestans3.types.ImmutableType>`
        """
        self._of_type = of_type
        self._rules_config = _MergingDictionaryWithMutableOwnValues(of_type.default_rules_config())
        self._check_rules_config(kwargs)
        self.required = required
        self.default = default

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

    def _check_rule_config(self, key, config):
        """ adds a configuration of a |rule| to this instance """
        try:
            _rule = self.property_type.get_property_rule(key)
        except KeyError:
            raise ValueError("{} is not a registered rule of type {}".format(key, self.property_type.__name__))
        if not _rule.configurable:
            raise ValueError("{} is a non-configurable rule in class {}, (see {}.{}()))" \
                             .format(key, self.property_type.__name__, ImmutableType.__name__,
                                     ImmutableType.register_property_rule.__name__))
        self._rules_config.update({key: config})

    def get_rule_config(self, key):
        """ find a |rule|\ 's configuration by its name """
        return self._rules_config[key]

    def _check_rules_config(self, kwargs):
        """
        merge default rule configs with explicit rule configs in kwargs

        :param dict kwargs:
        """
        [self._check_rule_config(key, config) for key, config in list(kwargs.items())]


# noinspection PyAbstractClass
class Scalar(ImmutableType):
    """
    Base type of all |Scalar| |attributes|\ .

    known Subclasses:
        - |Boolean|
        - |Number|
            - |Integer|
            - |Float|
        - |String|
        - |Date|
        - |DateTime|
        - |Time|
    """
    pass


# noinspection PyAbstractClass
class Container(ImmutableType):
    """ subclass of all |types| with containable |attributes| """

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
