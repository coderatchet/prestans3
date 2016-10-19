# -*- coding: utf-8 -*-
"""
    tests.types.test_type
    ~~~~~~~~~~~~~~~~~~~~~

    A WSGI compliant REST micro-framework.

    :copyright: (c) 2016 Anomaly Software
    :license: Apache 2.0, see LICENSE for more details.
"""

import pytest
from prestans3.errors import ValidationException
from prestans3.types import Integer
from prestans3.types import Model
from prestans3.types import String, _Property, ImmutableType


class MyClass(Model):
    some_string = String.property()


def test_model_class_can_contain_instances_of_putable_type_property():
    assert isinstance(MyClass.__dict__['some_string'], _Property)


def test_default_rules_config_returns_correctly():
    class __MyType(ImmutableType):
        pass

    __MyType.register_property_rule(lambda _x, _y: None, name="foo", default="baz")
    __MyType.register_property_rule(lambda _x, _y: None, name="bar")

    default_config = __MyType.default_rules_config()
    assert 'foo' in default_config
    assert 'bar' not in default_config
    assert default_config['foo'] == 'baz'


def test_direct_instance_of_immutable_type_raises_error_on_from_value():
    with pytest.raises(NotImplementedError):
        ImmutableType().from_value('irrelevant')


def test_choices_property_rule_works():
    class __Model(Model):
        my_int = Integer.property(choices=[1, 5])
        my_string = String.property(choices=['spam', 'ham'])

    model = __Model.mutable()
    model.my_int = 1
    model.my_string = 'spam'
    model.validate()
    model.my_int = 5
    model.my_string = 'ham'
    model.validate()
    model.my_int = 3
    model.my_string = 'no'
    with pytest.raises(ValidationException) as ex:
        model.validate()
    assert "{} property is {}, valid choices are {}".format(String.__name__, 'no', "[spam, ham]") in str(ex)
    assert "{} property is {}, valid choices are {}".format(Integer.__name__, 3, '[1, 5]') in str(ex)

