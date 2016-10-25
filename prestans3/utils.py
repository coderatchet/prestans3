# -*- coding: utf-8 -*-
"""
    prestans3.utils
    ~~~~~~~~~~~~~~~

    A WSGI compliant REST micro-framework.

    :copyright: (c) 2016 Anomaly Software
    :license: Apache 2.0, see LICENSE for more details.
"""
import functools
import numbers
import sys
from copy import copy

import prestans3.types
from prestans3.errors import AccessError

try:
    # noinspection PyUnresolvedReferences,PyStatementEffect
    basestring


    def is_str(s):
        """python 2.7 safe version"""
        # noinspection PyUnresolvedReferences
        return isinstance(s, basestring)
except NameError:
    def is_str(s):
        """python 3+ safe version"""
        return isinstance(s, str)


# noinspection PyUnusedLocal
def prefix_with_injected(template_class, class_to_inject, target_base_class):
    return "Injected{}".format(template_class.__name__)


injected_class_cache = dict()


def _injected_class_init__(*args, **kwargs):
    super(args[0].__class__, args[0]).__init__(*args[1:], **kwargs)


def inject_class(template_class, class_to_inject, target_base_class=object, new_type_name_func=None):
    """
    injects a class above a target class in the mro of the specified class. New class's default name is
    Injected<name of template_class>. If the target_base_class is not in the template class's method resolution order
    (MRO), the original template_class is returned to the caller. a custom function may be provided to the
    new_type_name_func parameter to adjust the name of the new class.

    :param type template_class: the class to have its hierarchy modified to create a new class
    :param type class_to_inject: the class to inject about the target_base_class
    :param type target_base_class: the class to inject the class before
    :param new_type_name_func: function that determines the name of the new class to be generated.
     :type new_type_name_func: (template_class: type, class_to_inject: type, target_base_class: type) -> str
    :return: the new modified type
    """
    args_key = (template_class, class_to_inject, target_base_class, new_type_name_func)
    if args_key in injected_class_cache:
        return injected_class_cache[args_key]

    if target_base_class in template_class.mro():
        if new_type_name_func is None:
            new_type_name_func = prefix_with_injected
        new_type_name = new_type_name_func(template_class, class_to_inject, target_base_class)

        new_bases = []
        _bases = list(copy(template_class.__bases__))
        for base in _bases:
            if base is target_base_class:
                new_bases += [class_to_inject, target_base_class]
            else:
                new_bases.append(inject_class(base, class_to_inject, target_base_class))
        new_bases.insert(0, template_class)
        new_type = type(new_type_name, tuple(new_bases), dict(template_class.__dict__))
        new_type.__init__ = _injected_class_init__
        injected_class_cache.update({args_key: new_type})
        return new_type
    else:
        injected_class_cache.update({args_key: template_class})
        return template_class


def with_metaclass(meta, *bases):
    """
    Create a base class with a metaclass.

    code from `six`_ PyPi package licenced under `MIT licence`_

    .. _MIT Licence: https://opensource.org/licenses/MIT
    .. _six: https://pypi.python.org/pypi/six
    """

    # This requires a bit of explanation: the basic idea is to make a dummy
    # metaclass for one level of class instantiation that replaces itself with
    # the actual metaclass.
    class MetaClass(meta):
        # noinspection PyUnusedLocal
        def __new__(cls, name, this_bases, d):
            return meta(name, bases, d)

    return type.__new__(MetaClass, 'temporary_class', (), {})


class MergingProxyDictionary(dict):
    """
    A MergingProxyDictionary allows for the merging of dictionaries without copying their values. for this reason,
    mutation of the contained dictionaries is not allowed directly through this class's interface. changing the
    referenced dictionaries outside this class will be reflected when accessing the keys through this interface. The
    dictionary will resolve keys with left to right priority on dictionaries provided in the __init__ function.
    """

    def __init__(self, initial_values=None, *args):
        """
        :param list[dict] args: the dictionaries to proxy against. key and value resolution is done in the order
        provided to this init function (left to right).
        """
        self._others = None
        if len(args) > 0:
            for arg in args:
                if isinstance(arg, MergingProxyDictionary):
                    self._append_others(arg)
                else:
                    self._append_others(MergingProxyDictionary(initial_values=arg))
        if initial_values is None:
            super(MergingProxyDictionary, self).__init__()
        else:
            super(MergingProxyDictionary, self).__init__(initial_values)

    def own_items(self):
        return super(MergingProxyDictionary, self).items()

    def own_keys(self):
        return super(MergingProxyDictionary, self).keys()

    def own_values(self):
        return super(MergingProxyDictionary, self).values()

    def _append_others(self, item):
        if self._others:
            return self._others.append(item)
        else:
            self._others = [item]
            return self._others

    def __getitem__(self, item):
        try:
            return super(MergingProxyDictionary, self).__getitem__(item)
        except KeyError as error:
            if self._others:
                for other in self._others:
                    try:
                        return other[item]
                    except KeyError:
                        pass
            raise error

    def _find_first(self, dictionary, condition):
        for key, value in list(dictionary.items()):
            if condition(key, value):
                return key, value
        return None

    def __contains__(self, item):
        in_me = super(MergingProxyDictionary, self).__contains__(item)
        if not in_me and self._others:
            return any(self._find_first(other, lambda key, _: item == key) for other in self._others)
        return in_me

    def __copy__(self):
        _copy = {}
        if self._others:
            for other in reversed(self._others):
                _copy.update(copy(other))
        _copy.update(super(MergingProxyDictionary, self).copy())
        return _copy

    def copy(self):
        return copy(self)

    def __len__(self):
        return sum(1 for _ in self.keys())

    def __str__(self):
        return str(self.copy())

    def __repr__(self):
        return repr(self.copy())

    def get(self, key, default=None):
        try:
            return super(MergingProxyDictionary, self).__getitem__(key)
        except KeyError:
            if self._others:
                for other in self._others:
                    try:
                        return other[key]
                    except KeyError:
                        pass
        return default

    # noinspection PyMethodOverriding
    def values(self):
        return self.copy().values()

    def keys(self):
        s = set(super(MergingProxyDictionary, self).keys())
        if self._others:
            [s.update(other.keys()) for other in self._others]
        return s
        # return self.copy().keys()

    def items(self):
        return self.copy().items()

    def is_own_key(self, key):
        return key in super(MergingProxyDictionary, self).keys()


class ImmutableMergingDictionary(MergingProxyDictionary):
    """ raises AccessError on an attempt to mutate, otherwise the same as |MergingProxyDictionary| """

    def __delitem__(self, key):
        """ :raises AccessError: when attempting to call this function. """
        raise AccessError(self.__class__, key)

    def __setitem__(self, key, value):
        """ :raises AccessError: when attempting to call this function. """
        raise AccessError(self.__class__, key)

    def update(self, other=None, **kwargs):
        """ :raises AccessError: when attempting to call this function. """
        raise AccessError(self.__class__)

    def popitem(self):
        """ :raises AccessError: when attempting to call this function. """
        raise AccessError(self.__class__)

    def setdefault(self, key, default=None):
        """ :raises AccessError: when attempting to call this function. """
        raise AccessError(self.__class__)

    def pop(self, key, default=None):
        """ :raises AccessError: when attempting to call this function. """
        raise AccessError(self.__class__)

    def clear(self):
        """ :raises AccessError: when attempting to call this function. """
        raise AccessError(self.__class__)


class LazyOneWayGraph(dict):
    """
    A lazily initialized one way graph. node's dependants are resolved if the terminating_type exists in the mro of the
    base classes.
    """

    def __init__(self, terminating_type=None):
        """
        :param type terminating_type: class of which must exist in a node's bases for it to be included as dependant for
          each queried class. otherwise each node without the terminating class will exist as a non-depending node
        """
        if terminating_type is None:
            terminating_type = object
        self._terminating_type = terminating_type
        super(LazyOneWayGraph, self).__init__()

    def __missing__(self, of_type):
        """
        lazily sets and returns the initialized dictionary values for each |type|\ . Each type will have it's own
        mutable values whilst maintaining a proxied read-only reference to it's base class's values using the
        |MergingProxyDictionary| \.
        :param of_type: the |type| to find the value for
        :type of_type: T <= |ImmutableType|
        :return: the newly instantiated dictionary of property_rules with read-only references to the |type|\ 's base
                 class value on this graph.
        """
        mro_ = [self[base] for base in of_type.__bases__ if
                self._terminating_type in base.mro() and base is not of_type]
        self[of_type] = MergingProxyDictionary({}, *mro_)
        return self[of_type]

class _PropertyRulesProperty(object):
    # noinspection PyUnusedLocal
    def __get__(self, cls, _mcs):
        return _mcs._property_rule_graph[cls]


class _ConfigChecksProperty(object):
    # noinspection PyUnusedLocal
    def __get__(self, cls, _mcs):
        return _mcs._config_check_graph[cls]


class _PrepareFunctionsProperty(object):
    # noinspection PyUnusedLocal
    def __get__(self, cls, _mcs):
        return _mcs._prepare_functions_graph[cls]


class _PrestansTypeMeta(type):
    property_rules = _PropertyRulesProperty()  # type: dict[str, (T <= ImmutableType, any) -> None]
    config_checks = _ConfigChecksProperty()  # type: dict[str, (type, any) -> None]
    prepare_functions = _PrepareFunctionsProperty()  # type: dict[str, (T <= ImmutableType) -> T]
    _prepare_functions_graph = None
    _config_check_graph = None
    _property_rule_graph = None


########################################################################################################################
# The following code was obtained from the `future library`_ and is used in compliance with the `MIT licence`_         #
#                                                                                                                      #
# .. _future library: https://pypi.python.org/pypi/future                                                              #
# .. _MIT Licence: https://opensource.org/licenses/MIT                                                                 #
########################################################################################################################



PY3 = sys.version_info[0] == 3
PY2 = sys.version_info[0] == 2
PY26 = sys.version_info[0:2] == (2, 6)
PY27 = sys.version_info[0:2] == (2, 7)
PYPY = hasattr(sys, 'pypy_translation_info')


def istext(obj):
    """
    Deprecated. Use::
        >>> isinstance(obj, str)
    after this import:
        >>> from future.builtins import str
    """
    return isinstance(obj, type(u''))


def isbytes(obj):
    """
    Deprecated. Use::
        >>> isinstance(obj, bytes)
    after this import:
        >>> from future.builtins import bytes
    """
    return isinstance(obj, type(b''))


def isnewbytes(obj):
    """
    Equivalent to the result of ``isinstance(obj, newbytes)`` were
    ``__instancecheck__`` not overridden on the newbytes subclass. In
    other words, it is REALLY a newbytes instance, not a Py2 native str
    object?
    """
    # TODO: generalize this so that it works with subclasses of newbytes
    # Import is here to avoid circular imports:
    from prestans3.future.newbytes import newbytes
    return type(obj) == newbytes


def isint(obj):
    """
    Deprecated. Tests whether an object is a Py3 ``int`` or either a Py2 ``int`` or
    ``long``.

    Instead of using this function, you can use:

        >>> from future.builtins import int
        >>> isinstance(obj, int)

    The following idiom is equivalent:

        >>> from numbers import Integral
        >>> isinstance(obj, Integral)
    """

    return isinstance(obj, numbers.Integral)


# Some utility functions to enforce strict type-separation of unicode str and
# bytes:
def disallow_types(argnums, disallowed_types):
    """
    A decorator that raises a TypeError if any of the given numbered
    arguments is of the corresponding given type (e.g. bytes or unicode
    string).

    For example:

        @disallow_types([0, 1], [unicode, bytes])
        def f(a, b):
            pass

    raises a TypeError when f is called if a unicode object is passed as
    `a` or a bytes object is passed as `b`.

    This also skips over keyword arguments, so

        @disallow_types([0, 1], [unicode, bytes])
        def g(a, b=None):
            pass

    doesn't raise an exception if g is called with only one argument a,
    e.g.:

        g(b'Byte string')

    Example use:

    >>> class newbytes(object):
    ...     @disallow_types([1], [unicode])
    ...     def __add__(self, other):
    ...          pass

    >>> newbytes('1234') + u'1234'      #doctest: +IGNORE_EXCEPTION_DETAIL
    Traceback (most recent call last):
      ...
    TypeError: can't concat 'bytes' to (unicode) str
    """

    def decorator(function):

        @functools.wraps(function)
        def wrapper(*args, **kwargs):
            # These imports are just for this decorator, and are defined here
            # to prevent circular imports:
            from prestans3.future.newbytes import newbytes
            from prestans3.future.newstr import newstr
            from prestans3.future.newint import newint

            errmsg = "argument can't be {0}"
            for (argnum, mytype) in zip(argnums, disallowed_types):
                # Handle the case where the type is passed as a string like 'newbytes'.
                if isinstance(mytype, str) or isinstance(mytype, bytes):
                    mytype = locals()[mytype]

                # Only restrict kw args only if they are passed:
                if len(args) <= argnum:
                    break

                # Here we use type() rather than isinstance() because
                # __instancecheck__ is being overridden. E.g.
                # isinstance(b'abc', newbytes) is True on Py2.
                if type(args[argnum]) == mytype:
                    raise TypeError(errmsg.format(mytype))

            return function(*args, **kwargs)

        return wrapper

    return decorator


def no(mytype, argnums=(1,)):
    """
    A shortcut for the disallow_types decorator that disallows only one type
    (in any position in argnums).

    Example use:

    >>> class newstr(object):
    ...     @no('bytes')
    ...     def __add__(self, other):
    ...          pass

    >>> newstr(u'1234') + b'1234'     #doctest: +IGNORE_EXCEPTION_DETAIL
    Traceback (most recent call last):
      ...
    TypeError: argument can't be bytes

    The object can also be passed directly, but passing the string helps
    to prevent circular import problems.
    """
    if isinstance(argnums, numbers.Integral):
        argnums = (argnums,)
    disallowed_types = [mytype] * len(argnums)
    return disallow_types(argnums, disallowed_types)


def issubset(list1, list2):
    """
    Examples:

    >>> issubset([], [65, 66, 67])
    True
    >>> issubset([65], [65, 66, 67])
    True
    >>> issubset([65, 66], [65, 66, 67])
    True
    >>> issubset([65, 67], [65, 66, 67])
    False
    """
    n = len(list1)
    for startpos in range(len(list2) - n + 1):
        if list2[startpos:startpos + n] == list1:
            return True
    return False


def native(obj):
    """
    On Py3, this is a no-op: native(obj) -> obj

    On Py2, returns the corresponding native Py2 types that are
    superclasses for backported objects from Py3:

    >>> from builtins import str, bytes, int

    >>> native(str(u'ABC'))
    u'ABC'
    >>> type(native(str(u'ABC')))
    unicode

    >>> native(bytes(b'ABC'))
    b'ABC'
    >>> type(native(bytes(b'ABC')))
    bytes

    >>> native(int(10**20))
    100000000000000000000L
    >>> type(native(int(10**20)))
    long

    Existing native types on Py2 will be returned unchanged:

    >>> type(native(u'ABC'))
    unicode
    """
    if hasattr(obj, '__native__'):
        return obj.__native__()
    else:
        return obj

########################################################################################################################
# The above code was obtained from the `future library`_ and is used in compliance with the `MIT licence`_         #
#                                                                                                                      #
# .. _future library: https://pypi.python.org/pypi/future                                                              #
# .. _MIT Licence: https://opensource.org/licenses/MIT                                                                 #
########################################################################################################################