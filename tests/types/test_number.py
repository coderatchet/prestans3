# -*- coding: utf-8 -*-
"""
    tests.types.test_integer
    ~~~~~~~~~~~~~~~~~~~~~~~~

    A WSGI compliant REST micro-framework.

    :copyright: (c) 2016 Anomaly Software
    :license: Apache 2.0, see LICENSE for more details.
"""
wimport pytest

from prestans3.errors import ValidationException
from prestans3.types import Float
from prestans3.types import Integer
from prestans3.types import Model


def test_min_property_rule_works():
    class __Model(Model):
        my_int = Integer.property(min=1)
        my_float = Float.property(min=9.3)

    model = __Model.mutable()
    model.my_int = 1
    model.my_float = 9.3
    model.validate()
    model.my_int = 0
    model.my_float = 9.26
    with pytest.raises(ValidationException) as ex:
        model.validate()
    assert "{} property is {}, however the configured minimum value is {}".format(
        Integer, 0, 1) in str(ex)
    assert "{} property is {}, however the configured minimum value is {}".format(
        Float, 9.26, 9.3) in str(ex)


def test_max_property_rule_works():
    class __Model(Model):
        my_int = Integer.property(max=1)
        my_float = Float.property(max=9.26)

    model = __Model.mutable()
    model.my_int = 1
    model.my_float = 9.26
    model.validate()
    model.my_int = 2
    model.my_float = 9.3
    with pytest.raises(ValidationException) as ex:
        model.validate()
    assert "{} property is {}, however the configured maximum value is {}".format(
        Integer, 2, 1) in str(ex)
    assert "{} property is {}, however the configured maximum value is {}".format(
        Float, 9.3, 9.26) in str(ex)