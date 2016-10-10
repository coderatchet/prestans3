# -*- coding: utf-8 -*-
"""
    prestans3.utils
    ~~~~~~~~~~~~~~~

    A WSGI compliant REST micro-framework.

    :copyright: (c) 2016 Anomaly Software
    :license: Apache 2.0, see LICENSE for more details.
"""
from copy import copy
from functools import lru_cache

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


@lru_cache(maxsize=100)
def inject_class(template_class, class_to_inject, target_base_class=object, new_type_name_func=None):
    """
    injects a class above a target class in the mro of the specified class. New class's default name is
    Injected<name of template_class>

    :param type template_class: the class to have its hierarchy modified to create a new class
    :param type class_to_inject: the class to inject about the target_base_class
    :param type target_base_class: the class to inject the class above (i.e. type(class_to_inject, bases=target_base_class, dict=class_to_inject.__dict__))
    :param new_type_name_func: function that determines the name of the new class to be generated
     :type new_type_name_func: (type, type, type) -> str
    :return: the new modified type
    """
    if new_type_name_func is None:
        new_type_name_func = prefix_with_injected

    new_type_name = new_type_name_func(template_class, class_to_inject, target_base_class)

    _bases = list(copy(template_class.__bases__))
    if target_base_class in _bases:
        index_of_target = _bases.index(target_base_class)
        _bases.insert(index_of_target, class_to_inject)
        return type(new_type_name, tuple(_bases), dict(class_to_inject.__dict__))
    else:
        _bases = [inject_class(base, class_to_inject, target_base_class, new_type_name_func)
                  for base in _bases if target_base_class in base.mro()] \
                 + [base for base in _bases if target_base_class not in base.mro()]
        return type(new_type_name, tuple(_bases), dict(template_class.__dict__))
