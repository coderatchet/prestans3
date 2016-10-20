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
from prestans3.utils import MergingProxyDictionary


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


def test_register_config_check_raises_value_error_when_receiving_function_with_less_than_2_args():
    # noinspection PyUnusedLocal
    def _test(x):
        pass

    with pytest.raises(ValueError) as error:
        ImmutableType.register_config_check(_test)
    assert 'expected property_rule function with 2 arguments, received ' \
           'function with {arg_count} argument(s): {func_name}({arg_list})'.format(
        arg_count=1, func_name='_test', arg_list=", ".join(_test.__code__.co_varnames)) in str(error.value)


def test_register_config_has_default_config():
    class __Model(Model):
        pass

    # noinspection PyUnusedLocal
    def _test(x, y):
        pass

    __Model.register_config_check(_test)
    assert __Model.config_checks['_test'] is _test


def test_property_may_accept_prepare_argument():
    class _Model(Model):
        prop = ImmutableType.property(prepare=lambda x: None)


# def test_type_can_access_graph_storage_for_own_prepare_functions():
#     class _IM(ImmutableType):
#         pass
#
#     assert isinstance(_IM.prepare_functions, MergingProxyDictionary)
#     assert len(_IM.own_values) == 0


# def test_type_may_register_relevant_prepare_function():
#     class _IM(ImmutableType):
#         pass
#
#     noop = lambda x: None
#     _IM.register_prepare_function(noop, name="noop")
#     _IM.prepare_functions['noop'] == noop

# def test_prepare_argument_will_accept_predefined_function_name():
#     class _Model(Model):
#         prop = ImmutableType.property(prepare='some_func')