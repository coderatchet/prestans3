# -*- coding: utf-8 -*-
"""
    prestans3.utils
    ~~~~~~~~~~~~~~~

    A WSGI compliant REST micro-framework.

    :copyright: (c) 2016 Anomaly Software
    :license: Apache 2.0, see LICENSE for more details.
"""
from copy import copy

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


def prefix_with_injected(template_class, class_to_inject, target_base_class):
    return "Injected{}".format(template_class.__name__)


injected_class_cache = dict()


def inject_class(template_class, class_to_inject, target_base_class=object, new_type_name_func=None):
    """
    injects a class above a target class in the mro of the specified class. New class's default name is
    Injected<name of template_class>. If the target_base_class is not in the template class's method resolution order
    (MRO), the original template_class is returned to the caller.

    :param type template_class: the class to have its hierarchy modified to create a new class
    :param type class_to_inject: the class to inject about the target_base_class
    :param type target_base_class: the class to inject the class before
    :param new_type_name_func: function that determines the name of the new class to be generated
     :type new_type_name_func: (type, type, type) -> str
    :return: the new modified type
    """
    args_key = (template_class, class_to_inject, target_base_class, new_type_name_func)
    if args_key in injected_class_cache:
        return injected_class_cache[args_key]
    if new_type_name_func is None:
        new_type_name_func = prefix_with_injected

    new_type_name = new_type_name_func(template_class, class_to_inject, target_base_class)

    _bases = list(copy(template_class.__bases__))
    if target_base_class in template_class.mro():
        new_bases = []
        for base in _bases:
            if base is target_base_class:
                new_bases += [class_to_inject, target_base_class]
            else:
                new_bases.append(inject_class(base, class_to_inject, target_base_class))
        new_type = type(new_type_name, tuple(new_bases), dict(template_class.__dict__))
        injected_class_cache.update({args_key: new_type})
        return new_type
    else:
        injected_class_cache.update({args_key: template_class})
        return template_class


def with_metaclass(meta, *bases):
    """
    Create a base class with a metaclass.

    code from `six`_ pypi package licenced under `MIT licence`_

    .. _MIT Licence: https://opensource.org/licenses/MIT
    .. _six: https://pypi.python.org/pypi/six
    """

    # This requires a bit of explanation: the basic idea is to make a dummy
    # metaclass for one level of class instantiation that replaces itself with
    # the actual metaclass.
    class metaclass(meta):
        def __new__(cls, name, this_bases, d):
            return meta(name, bases, d)

    return type.__new__(metaclass, 'temporary_class', (), {})
