# -*- coding: utf-8 -*-
"""
    prestans3.utils
    ~~~~~~~~~~~~~~~

    A WSGI compliant REST micro-framework.

    :copyright: (c) 2016 Anomaly Software
    :license: Apache 2.0, see LICENSE for more details.
"""
from copy import copy

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

    :raises |AccessError|: If an attempt to mutate the dictionary is made.
    """

    def __init__(self, *args):
        """
        :param list[dict] args: the dictionaries to proxy against. key and value resolution is done in the order
        provided to this init function (left to right).
        """
        self._other = None
        if len(args) > 0:
            super(MergingProxyDictionary, self).__init__(args[0])
            if len(args) > 1:
                if isinstance(args[1], MergingProxyDictionary):
                    self._other = args[1]
                else:
                    self._other = MergingProxyDictionary(*args[1:])
        else:
            super(MergingProxyDictionary, self).__init__()

    def __getitem__(self, item):
        try:
            return super(MergingProxyDictionary, self).__getitem__(item)
        except KeyError as error:
            if not self._other:
                raise error
            return self._other[item]

    def __contains__(self, item):
        in_me = super(MergingProxyDictionary, self).__contains__(item)
        if not in_me and self._other:
            in_me = item in self._other
        return in_me

    def __copy__(self):
        return super(MergingProxyDictionary, self).copy()

    def copy(self):
        _copy = {} if not self._other else self._other.copy()
        _copy.update(copy(self))
        return _copy

    def __len__(self):
        return sum(1 for _ in self.keys())

    def __str__(self):
        return str(self.copy())

    def __repr__(self):
        return repr(self.copy())

    def update(self, other=None, **kwargs):
        """ :raises AccessError: when attempting to call this function. """
        raise AccessError(self.__class__)

    def get(self, key, default=None):
        try:
            return super(MergingProxyDictionary, self).__getitem__(key)
        except KeyError:
            if self._other:
                return self._other.get(key, default)
            return default

    # noinspection PyMethodOverriding
    def values(self):
        return self.copy().values()

    def keys(self):
        s = set(super(MergingProxyDictionary, self).keys())
        if self._other:
            s.update(self._other.keys())
        return s
        # return self.copy().keys()

    def items(self):
        return self.copy().items()
