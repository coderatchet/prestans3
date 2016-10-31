# -*- coding: utf-8 -*-
"""
    prestans.types.string
    ~~~~~~~~~~~~~~~~~~~~~
    
    A WSGI compliant REST micro-framework.

    :copyright: (c) 2016 Anomaly Software
    :license: Apache 2.0, see LICENSE for more details.
"""
import re
from future.types.newstr import BaseNewStr, newstr
from future.utils import with_metaclass, PYPY

from ..errors import ValidationException, PropertyConfigError
from ..types import PrestansTypeMeta
from . import ImmutableType
from ..utils import is_str


class MergingStrMeta(BaseNewStr, PrestansTypeMeta):
    pass


# noinspection PyAbstractClass
class String(with_metaclass(MergingStrMeta, ImmutableType, newstr)):
    """
    Prestans 3 String type. Acts as a native :class:`str` with additional Prestans 3 functionality.
    """

    if PYPY:
        def __init__(self, value=u'', encoding=None):
            newstr.__init__(self, value, encoding)
            super(String, self).__init__()

    else:
        def __init__(self, value=u'', encoding=None):
            newstr.__init__(value, encoding)
            super(String, self).__init__()

    @classmethod
    def from_value(cls, value):
        try:
            return ImmutableType.from_value(value)
        except NotImplementedError:
            # py2to3 replace is_str(value) with isinstance(x, str)
            if not is_str(value):
                raise TypeError(
                    "{} of type {} is not coercible to {}".format(value, value.__class__.__name__, cls.__name__))
            return String(value)


def _min_length(instance, config):
    """
    Property rule that checks whether the instance is at least `config` length.

    :param |String| instance: string to check
    :param int config: the minimum length to check for
    :raises |ValidationException|\ : if the instance is less than `config` in length
    """
    length = len(instance)
    if length < config:
        raise ValidationException(instance.__class__,
                                  '{} min_length config is {} however len("{}") == {}'.format(
                                      instance.__class__.__name__,
                                      config, instance,
                                      length))


def _max_length(instance, config):
    """
    Property rule that checks whether the instance is at most `config` length.

    :param |String| instance: string to check
    :param int config: the maximum length to check for
    :raises |ValidationException|\ : if the instance is greater than `config` in length
    """
    length = len(instance)
    if length > config:
        raise ValidationException(instance.__class__,
                                  '{} max_length config is {} however len("{}") == {}'.format(
                                      instance.__class__.__name__,
                                      config, instance,
                                      length))


def _format_regex(instance, config):
    """
    Property rule that checks whether the instance conforms to the configured regular expression

    :param |String| instance: the string to check
    :param str config: The regular expression to check against
    :raises |ValidationException|\ : if the string does not match the configured regular expression
    """
    if not re.match(config, instance):
        raise ValidationException(instance.__class__, '{} does not match the format_regex {}'.format(instance.__class__,
                                                                                                     config))


String.register_property_rule(_min_length, name="min_length")
String.register_property_rule(_max_length, name="max_length")
String.register_property_rule(_format_regex, name="format_regex")


def _min_max_string_check_config(configured_type, all_config):
    """
    checks whether the min/max configurations don't conflict, i.e. min should be equal or less than max

    :param configured_type: subclass of |String|
    :param dict all_config: dictionary of configured rules plus defaults for this |type| subclass
    :raises |PropertyConfigError|\ : if the configuration contains a min greater than max
    """
    if all_config is not None and 'min_length' in all_config and 'max_length' in all_config \
            and all_config['min_length'] > all_config['max_length']:
        raise PropertyConfigError(configured_type, 'min_length and max_length', 'invalid {} property configuration: ' + \
                                  'min_length config of {} is greater than max_length config of {}'.format(
                                      configured_type.__name__, all_config['min_length'], all_config['max_length']))


String.register_config_check(_min_max_string_check_config, name="min_max_string_check_config")


def _prepare_trim(x):
    """ trims whitespace from a string """
    return x.strip()


def _prepare_normalize_whitespace(x):
    """ trims string and causes runs of 2 or more spaces to compress into 1"""
    return re.sub(r'[ ]{2,}', ' ', _prepare_trim(x))


String.register_prepare_function(_prepare_trim, name="trim")
String.register_prepare_function(_prepare_normalize_whitespace, name="normalize_whitespace")
