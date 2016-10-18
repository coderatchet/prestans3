# -*- coding: utf-8 -*-
"""
    prestans.types.string
    ~~~~~~~~~~~~~~~~~~~~~
    
    A WSGI compliant REST micro-framework.

    :copyright: (c) 2016 Anomaly Software
    :license: Apache 2.0, see LICENSE for more details.
"""
from prestans3.errors import ValidationException
from prestans3.utils import is_str

from . import ImmutableType


class String(ImmutableType, str):
    def __init__(self, value=None):
        if value is None:
            value = ""
        str.__init__(value)

    @classmethod
    def from_value(cls, value):
        if not is_str(value):
            raise TypeError(
                "{} of type {} is not coercible to {}".format(value, value.__class__.__name__, cls.__name__))
        return String(value)


def _str_min_length(instance, config):
    length = len(instance)
    if length < config:
        raise ValidationException(instance.__class__,
                                  '{} str_min_length config is {} however len("{}") == {}'.format(
                                      instance.__class__.__name__,
                                      config, instance,
                                      length))


def _str_max_length(instance, config):
    length = len(instance)
    if length > config:
        raise ValidationException(instance.__class__,
                                  '{} str_max_length config is {} however len("{}") == {}'.format(
                                      instance.__class__.__name__,
                                      config, instance,
                                      length))


String.register_property_rule(_str_min_length, name="str_min_length")
String.register_property_rule(_str_max_length, name="str_max_length")
