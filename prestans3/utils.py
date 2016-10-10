# -*- coding: utf-8 -*-
"""
    prestans3.utils
    ~~~~~~~~~~~~~~~

    A WSGI compliant REST micro-framework.

    :copyright: (c) 2016 Anomaly Software
    :license: Apache 2.0, see LICENSE for more details.
"""
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


@lru_cache
def inject_class_in_hierarchy(template_class, class_to_inject, target_base_class=object):
    """
    injects a class above a target class in the mro of the specified class

    :param type template_class: the class to have its hierarchy modified to create a new class
    :param type class_to_inject: the class to inject about the target_base_class
    :param type target_base_class: the class to inject the class above (i.e. type(class_to_inject, bases=target_base_class, dict=class_to_inject.__dict__))
    :return: the new modified type
    """

