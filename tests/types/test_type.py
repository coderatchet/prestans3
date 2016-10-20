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


def test_type_can_access_graph_storage_for_own_prepare_functions():
    class _IM(ImmutableType):
        pass

    assert isinstance(_IM.prepare_functions, MergingProxyDictionary)
    assert len(_IM.prepare_functions.own_items()) == 0


def test_type_may_register_relevant_prepare_function():
    class _IM(ImmutableType):
        pass

    noop = lambda x: None
    _IM.register_prepare_function(noop, name="noop")
    _IM.prepare_functions['noop'] == noop


def test_resolve_prepare_function_on_property_will_return_func_if_function_provided():
    prop = _Property(ImmutableType)
    noop = lambda x: None
    assert prop._resolve_prepare_function(noop) == noop


def test_resolve_prepare_function_raises_type_error_when_passed_function_with_less_or_more_than_one_argument():
    prop = _Property(ImmutableType)

    def _no_args(): None

    def _two_args(x, y): None

    def _one_arg(x): None

    with pytest.raises(TypeError) as error:
        prop._resolve_prepare_function(_no_args)
    assert 'provided prepare function should only 1 argument, received function has {}: {}({})'.format(
        0, _no_args.__name__, ''
    )

    with pytest.raises(TypeError) as error:
        prop._resolve_prepare_function(_two_args)
    assert 'provided prepare function should only 1 argument, received function has {}: {}({})'.format(
        2, _two_args.__name__, ", ".join(_two_args.__code__.co_varnames)
    )

    assert prop._resolve_prepare_function(_one_arg) == _one_arg


def test_string_parameter_raises_key_error_on_no_pre_registered_prepare_function_with_name():
    class _IM(ImmutableType):
        pass

    noop = lambda x: None
    _IM.register_prepare_function(noop, name='here')
    prop = _IM.property()

    assert prop._resolve_prepare_function('here') == noop
    with pytest.raises(KeyError) as error:
        prop._resolve_prepare_function('not here')
    assert "'{}' is not a registered prepare function of {}".format('not here', _IM.__name__) in str(error.value)


def test_get_prepare_process_method_on_property_returns_function_that_adjusts_input_as_expected():
    class _IM(ImmutableType):
        pass

    double = lambda x: x + x
    _IM.register_prepare_function(double, name="double")

    prop = ImmutableType.property(prepare=double)
    function = prop.prepare_process_function
    assert function.__code__.co_argcount == 1
    assert function(1) == 2
    assert function("foo") == "foofoo"


def test_get_prepare_process_method_accepts_named_parameter_correctly():
    class _IM(ImmutableType):
        pass

    double = lambda x: x + x
    _IM.register_prepare_function(double, name="double")

    prop = _IM.property(prepare="double")
    function = prop.prepare_process_function
    assert function(1) == 2
    assert function("foo") == "foofoo"


def test_can_provide_custom_function():
    class _IM(ImmutableType):
        pass

    double = lambda x: x + x
    prop_1 = ImmutableType.property(prepare=double)
    prop_2 = ImmutableType.property(prepare=lambda x: x - x)

    assert prop_1.prepare_process_function(1) == 2
    assert prop_2.prepare_process_function(1) == 0


def test_can_provide_list_of_prepare_functions_resolved_in_order():
    class _IM(ImmutableType):
        pass

    _IM.register_prepare_function(lambda x: x * x, name="square")

    def _divide_by_2(x):
        return x / 2

    prop = _IM.property(prepare=['square', lambda x: x + 2, _divide_by_2])
    assert prop.prepare_process_function(2) == 3
    prop = _IM.property(prepare=[lambda x: x + 2, 'square', _divide_by_2])
    assert prop.prepare_process_function(2) == 8


def test_resolve_prepare_function_raises_type_error_on_invalid_argument():
    with pytest.raises(TypeError) as error:
        _Property(ImmutableType)._resolve_prepare_function(1)
    assert "prepare argument to property must be a str name of a pre-registered prepare function, a" + \
           "custom one-argument function or a list of any of the previous values, received: {} of type {}".format(
               1, int.__name__
           ) in str(error.value)


def test_no_prepare_argument_does_not_break_code():
    _Property(ImmutableType).prepare_process_function(1)
