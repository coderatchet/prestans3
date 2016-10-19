# -*- coding: utf-8 -*-
"""
    prestans.types.temporal
    ~~~~~~~~~~~~~~~~~~~~~~~

    A WSGI compliant REST micro-framework.

    :copyright: (c) 2016 Anomaly Software
    :license: Apache 2.0, see LICENSE for more details.
"""
from prestans3.errors import ValidationException, PropertyConfigError
from prestans3.types import ImmutableType


# noinspection PyAbstractClass
class Temporal(ImmutableType):
    """ Base class for all time and date style classes """
    @classmethod
    def from_value(cls, value):
        return super(Temporal, cls).from_value(value)


def _after(instance, config):
    """

    :param instance:
    :param config:
    :return:
    """
    if not instance > config:
        raise ValidationException(instance.__class__,
                                  "{} is not after configured temporal {}".format(str(instance), str(config)))


def _before(instance, config):
    """

    :param instance:
    :param config:
    :return:
    """
    if not instance < config:
        raise ValidationException(instance.__class__,
                                  "{} is not before configured temporal {}".format(str(instance), str(config)))


def _before_after_config_check(type, all_config):
    if all_config is not None and 'after' in all_config and 'before' in all_config:
        after = all_config['after']
        before = all_config['before']
        if after >= before:
            raise PropertyConfigError(type, "after and before",
                                      "configuration for after '{}' is equal-to or " +
                                      "later than configuration for before '{}'".format(after, before))


Temporal.register_property_rule(_after, name="after")
Temporal.register_property_rule(_before, name="before")
Temporal.register_config_check(_before_after_config_check, name="before_after_config_check")
