# -*- coding: utf-8 -*-
"""
    prestans.types.integer
    ~~~~~~~~~~~~~~~~~~~~~~
    
    A WSGI compliant REST micro-framework.

    :copyright: (c) 2016 Anomaly Software
    :license: Apache 2.0, see LICENSE for more details.
"""
import pprint

from prestans3.errors import ValidationException

from . import Number


class Integer(int, Number):
    @classmethod
    def from_value(cls, integer):
        if isinstance(integer, Integer):
            return integer
        elif not isinstance(integer, int):
            raise ValueError(integer)
        return Integer(integer)

    def __init__(self, value, base=10):
        int.__init__(value, base)

def _min(instance, config):
    if instance < config:
        raise ValidationException(instance.__class__, "{} property is {}, however the configured minimum value is {}".format(instance.__class__, instance, config))

Integer.register_property_rule(_min, name="min")