# -*- coding: utf-8 -*-
"""
    prestans.types.number
    ~~~~~~~~~~~~~~~~~~~~~

    A WSGI compliant REST micro-framework.

    :copyright: (c) 2016 Anomaly Software
    :license: Apache 2.0, see LICENSE for more details.
"""
from ..errors import ValidationException

from . import ImmutableType


# noinspection PyAbstractClass
class Number(ImmutableType):

    @classmethod
    def from_value(cls, value):
        return super(Number, cls).from_value(value)


def _min(instance, config):
    """ checks the `instance` is at least `config` """
    if instance < config:
        raise ValidationException(instance.__class__,
                                  "{} property is {}, however the configured minimum value is {}".format(
                                      instance.__class__, instance, config))


def _max(instance, config):
    """ checks the `instance` is at most `config` """
    if instance > config:
        raise ValidationException(instance.__class__,
                                  "{} property is {}, however the configured maximum value is {}".format(
                                      instance.__class__, instance, config))


Number.register_property_rule(_min, name="min")
Number.register_property_rule(_max, name="max")
