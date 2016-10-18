# -*- coding: utf-8 -*-
"""
    prestans.types.temporal
    ~~~~~~~~~~~~~~~~~~~~~~~

    A WSGI compliant REST micro-framework.

    :copyright: (c) 2016 Anomaly Software
    :license: Apache 2.0, see LICENSE for more details.
"""
from prestans3.errors import ValidationException
from prestans3.types import ImmutableType


# noinspection PyAbstractClass
class Temporal(ImmutableType):
    """ Base class for all time and date style classes """
    pass


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


Temporal.register_property_rule(_after, name="after")
Temporal.register_property_rule(_before, name="before")
