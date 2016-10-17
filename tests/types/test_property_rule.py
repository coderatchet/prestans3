# -*- coding: utf-8 -*-
"""
    tests.types.test_property_rule
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    A WSGI compliant REST micro-framework.

    :copyright: (c) 2016 Anomaly Software
    :license: Apache 2.0, see LICENSE for more details.
"""
import pytest
import pytest_mock
from prestans3.errors import InvalidMethodUseError, ValidationException, PropertyConfigError
from prestans3.types import ImmutableType, Container, _Property
from prestans3.types import Model
from prestans3.types import String


class MyClass(ImmutableType):
    pass


# noinspection PyUnusedLocal
def my_property_rule(instance, config):
    return True


MyClass.register_property_rule(my_property_rule)


# noinspection PyAbstractClass
class MyOtherClass(ImmutableType):
    pass


# noinspection PyAbstractClass
def test_registered_class_has_correct_signature():
    class __ClassToRegisterWith(ImmutableType):
        pass

    # should have 2 args (class instance and configuration)
    _func = lambda x: x
    with pytest.raises(ValueError) as error:
        __ClassToRegisterWith.register_property_rule(_func)
    assert "expected property_rule function with 2 arguments, received function with 1 argument(s): <lambda>(x)" in str(
        error.value)

    def actually_defined_function():
        return True

    with pytest.raises(ValueError) as error:
        __ClassToRegisterWith.register_property_rule(actually_defined_function)
    assert "expected property_rule function with 2 arguments, received function with 0 argument(s): actually_defined_function()" in str(
        error.value)

    # noinspection PyUnusedLocal
    def proper_property_rule(instance, config):
        pass

    __ClassToRegisterWith.register_property_rule(proper_property_rule)


# noinspection PyAbstractClass
def test_can_store_property_rule_in_type():
    class __CustomClass(ImmutableType):
        pass

    # noinspection PyUnusedLocal
    def my_custom_property_rule(instance, config):
        pass

    __CustomClass.register_property_rule(my_custom_property_rule)
    # noinspection PyProtectedMember
    assert my_custom_property_rule.__name__ in __CustomClass.property_rules


# noinspection PyProtectedMember,PyAbstractClass,PyUnusedLocal
def test_can_name_property_rule():
    class __CustomClass2(ImmutableType):
        pass

    # noinspection PyUnusedLocal
    def my_custom_property_rule_nameable(instance, config):
        pass

    __CustomClass2.register_property_rule(property_rule=my_custom_property_rule_nameable, name="custom_prop")

    assert "custom_prop" in __CustomClass2.property_rules.keys()
    assert __CustomClass2.get_property_rule("custom_prop").__name__ == my_custom_property_rule_nameable.__name__


def test_can_find_config_by_rule_name(mocker):
    """
    :param pytest_mock.MockFixture mocker:
    """

    class __CustomClass(ImmutableType):
        pass

    __CustomClass.register_property_rule(lambda _x, _y: None, name="one_rule", default="config here")

    mocker.patch('prestans3.types._Property')
    _property = _Property(__CustomClass)
    # noinspection PyProtectedMember
    assert 'config here' == _property.get_rule_config('one_rule')


# noinspection PyAbstractClass
def test_can_set_default_configuration_for_rule(mocker):
    """
    :param pytest_mock.MockFixture mocker:
    """

    class _CustomClassDefaultConfiguration(ImmutableType):
        pass

    _CustomClassDefaultConfiguration.register_property_rule(lambda x, y: None, name="default_having_rule",
                                                            default="default config")
    assert "default config" == _CustomClassDefaultConfiguration.get_property_rule(
        "default_having_rule").default_config


def test_can_set_rule_as_non_configurable():
    class __CustomClassWithNonConfigurable(ImmutableType):
        pass

    __CustomClassWithNonConfigurable.register_property_rule(lambda x, y: None, name="non_configurable_rule",
                                                            configurable=False)
    assert not __CustomClassWithNonConfigurable.get_property_rule("non_configurable_rule").configurable


def test_check_rule_config_for_non_existing_rule_raises_value_error():
    class __CustomClass(ImmutableType):
        pass

    __CustomClass.register_property_rule(lambda _x, _y: None, name="exists")
    _prop = __CustomClass.property()
    _prop._get_and_check_rule_config("exists", "should work")
    with pytest.raises(ValueError) as error:
        _prop._get_and_check_rule_config("doesnt exist", "should throw error")
    assert "{} is not a registered rule of type {}".format("doesnt exist", __CustomClass.__name__) in str(error.value)


# noinspection PyAbstractClass
def test_check_rules_config_for_non_configurable_property_raises_property_config_error():
    class __CustomClassWithNonConfigurable(ImmutableType):
        pass

    __CustomClassWithNonConfigurable.register_property_rule(lambda _x, _y: None, name="non_configurable_rule",
                                                            configurable=False)

    non_configurable_property = __CustomClassWithNonConfigurable.property()
    with pytest.raises(PropertyConfigError) as error:
        non_configurable_property._get_and_check_rules_config(
            {"non_configurable_rule": "doesn't matter, should throw an error"})
    assert "non_configurable_rule is a non-configurable rule in class {}, (see {}.{}())" \
               .format(__CustomClassWithNonConfigurable.__name__,
                       ImmutableType.__name__,
                       ImmutableType.register_property_rule.__name__) in str(error.value)


def test_setup_rules_config_method_on__property_class_merges_defaults_with_kwargs():
    class __CustomClass(ImmutableType):
        pass

    __CustomClass.register_property_rule(lambda _x, _y: None, "override_me", default="default_config")
    __CustomClass.register_property_rule(lambda _x, _y: None, "no_override_me", default="default_config")

    class_property = __CustomClass.property(override_me="overriden_config")

    assert "overriden_config" == class_property.get_rule_config("override_me")
    assert "default_config" == class_property.get_rule_config("no_override_me")


def test_can_setup_non_configurable_rule_on_init():
    class __CustomClass(ImmutableType):
        pass

    def non_configurable(instance, config):
        pass

    __CustomClass.register_property_rule(non_configurable, default="non-configurable-default", configurable=False)

    _property = __CustomClass.property()
    "non-configurable_default" == _property.get_rule_config("non_configurable")


def test_unrelated_class_does_not_have_unrelated_rule():
    class __OneClass(ImmutableType):
        pass

    class __UnrelatedClass(ImmutableType):
        pass

    __OneClass.register_property_rule(lambda _x, _y: None, "unrelated_rule")
    assert "unrelated_rule" not in __UnrelatedClass.property_rules
    assert "unrelated_rule" in __OneClass.property_rules


def test_subclass_of_immutable_types_inherit_rules():
    class __MyClass(ImmutableType):
        pass

    class __MySubClass(__MyClass):
        pass

    __MyClass.register_property_rule(lambda _x, _y: None, name="my_class_rule")
    __MySubClass.register_property_rule(lambda _x, _y: None, name="my_sub_class_rule")

    assert "my_class_rule" in __MyClass.property_rules
    assert "my_sub_class_rule" not in __MyClass.property_rules
    assert "my_sub_class_rule" in __MySubClass.property_rules
    assert "my_class_rule" in __MySubClass.property_rules


def test_registering_rule_after_property_rules_accessed_correctly_reflects_changes():
    class __MyClass(ImmutableType):
        pass

    class __MySubClass(__MyClass):
        pass

    __MyClass.register_property_rule(lambda _x, _y: None, name="my_class_rule")
    __MySubClass.register_property_rule(lambda _x, _y: None, name="my_sub_class_rule")

    assert "my_class_rule" in __MyClass.property_rules
    assert "my_sub_class_rule" not in __MyClass.property_rules
    assert "my_sub_class_rule" in __MySubClass.property_rules
    assert "my_class_rule" in __MySubClass.property_rules

    __MyClass.register_property_rule(lambda _x, _y: None, name="injected_after_access")

    assert "my_class_rule" in __MyClass.property_rules
    assert "injected_after_access" in __MyClass.property_rules
    assert "my_sub_class_rule" not in __MyClass.property_rules
    assert "my_sub_class_rule" in __MySubClass.property_rules
    assert "injected_after_access" in __MySubClass.property_rules
    assert "my_class_rule" in __MySubClass.property_rules


def test_required_attributes_on_class_get_checked_on_validation():
    class __MyModel(Model):
        my_string = String.property(required=True)
        my_unrequired_string = String.property(required=False)

    my_model = __MyModel.mutable()
    my_model.my_string = "some_string"

    my_model.validate()


def test_required_attributes_raises_error_if_not_present():
    class __MyModel(Model):
        my_string = String.property(required=True)
        my_unrequired_string = String.property(required=False)

    my_model = __MyModel.mutable()

    with pytest.raises(ValidationException):
        my_model.validate()


def test_property_may_have_default_value():
    class __MyModel(Model):
        my_string_with_default = String.property(default="my string")

    assert __MyModel.my_string_with_default == 'my string'


def test_property_default_gets_overriden_when_set():
    class __MyModel(Model):
        my_string_with_default = String.property(default="default")

    model = __MyModel.mutable()
    model.my_string_with_default = 'not default'
    assert model.my_string_with_default == 'not default'


def test_property_rule_with_no_config_is_not_run():
    class _HasRule(ImmutableType):
        pass

    def __must_have_config(instance, config):
        raise ValidationException(instance.__class__, "test failure")

    _HasRule.register_property_rule(__must_have_config, name="must")
    _HasRule()
