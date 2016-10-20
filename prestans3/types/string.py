# -*- coding: utf-8 -*-
"""
    prestans.types.string
    ~~~~~~~~~~~~~~~~~~~~~
    
    A WSGI compliant REST micro-framework.

    :copyright: (c) 2016 Anomaly Software
    :license: Apache 2.0, see LICENSE for more details.
"""
import re

from prestans3.errors import ValidationException, PropertyConfigError
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


def _min_length(instance, config):
    length = len(instance)
    if length < config:
        raise ValidationException(instance.__class__,
                                  '{} min_length config is {} however len("{}") == {}'.format(
                                      instance.__class__.__name__,
                                      config, instance,
                                      length))


def _max_length(instance, config):
    length = len(instance)
    if length > config:
        raise ValidationException(instance.__class__,
                                  '{} max_length config is {} however len("{}") == {}'.format(
                                      instance.__class__.__name__,
                                      config, instance,
                                      length))


def _format_regex(instance, config):
    if not re.match(config, instance):
        raise ValidationException(instance.__class__, '{} does not match the format_regex {}'.format(instance.__class__,
                                                                                                     config))


String.register_property_rule(_min_length, name="min_length")
String.register_property_rule(_max_length, name="max_length")
String.register_property_rule(_format_regex, name="format_regex")


def _min_max_string_check_config(type, config):
    if config is not None and 'min_length' in config and 'max_length' in config \
            and config['min_length'] > config['max_length']:
        raise PropertyConfigError(type, 'min_length and max_length', 'invalid {} property configuration: ' + \
                                  'min_length config of {} is greater than max_length config of {}'.format(
                                      type.__name__, config['min_length'], config['max_length']))


String.register_config_check(_min_max_string_check_config, name="min_max_string_check_config")
