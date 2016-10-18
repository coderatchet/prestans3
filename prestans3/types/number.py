# -*- coding: utf-8 -*-
"""
    prestans.types.number
    ~~~~~~~~~~~~~~~~~~~~~

    A WSGI compliant REST micro-framework.

    :copyright: (c) 2016 Anomaly Software
    :license: Apache 2.0, see LICENSE for more details.
"""
from prestans3.errors import ValidationException

from . import ImmutableType


# noinspection PyAbstractClass
class Number(ImmutableType):
    pass


def _min(instance, config):
    if instance < config:
        raise ValidationException(instance.__class__,
                                  "{} property is {}, however the configured minimum value is {}".format(
                                      instance.__class__, instance, config))


def _max(instance, config):
    if instance > config:
        raise ValidationException(instance.__class__,
                                  "{} property is {}, however the configured maximum value is {}".format(
                                      instance.__class__, instance, config))


Number.register_property_rule(_min, name="min")
Number.register_property_rule(_max, name="max")
