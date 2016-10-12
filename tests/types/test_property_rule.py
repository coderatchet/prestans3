import pytest
import pytest_mock
from prestans3.errors import InvalidMethodUseError
from prestans3.types import ImmutableType, Container, _Property


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


def test_can_add_rule_config(mocker):
    """
    :param pytest_mock.MockFixture mocker:
    """

    class __CustomClass(ImmutableType):
        pass

    mocker.patch('prestans3.types._Property')
    _property = _Property(__CustomClass)
    _property._of_type = mocker.Mock()
    mocker.patch.dict(_property.property_type.property_rules, {"one_rule": lambda _x, _y: None})
    _property._add_rule_config("one_rule", "config")
    assert "one_rule" in _property.rules_config
    assert "config" == _property.rules_config['one_rule']


def test_can_find_config_by_rule_name(mocker):
    """
    :param pytest_mock.MockFixture mocker:
    """

    class __CustomClass(ImmutableType):
        pass

    mocker.patch('prestans3.types._Property')
    _property = _Property(__CustomClass)
    mocker.patch.dict(_property._rules_config, {"one_rule": "confighere"})
    assert 'confighere' == _property.get_rule_config('one_rule')


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


def test_setting_configuration_for_non_existing_rule_raises_value_error():
    class __CustomClass(ImmutableType):
        pass

    __CustomClass.register_property_rule(lambda _x, _y: None, name="exists")
    _prop = __CustomClass.property()
    _prop._add_rule_config("exists", "should work")
    with pytest.raises(ValueError) as error:
        _prop._add_rule_config("doesnt exist", "should throw error")
    assert "{} is not a registered rule of type {}".format("doesnt exist", __CustomClass.__name__) in str(error.value)


def test_adding_configuration_for_non_configurable_property_raises_value_error():
    class __CustomClassWithNonConfigurable(ImmutableType):
        pass

    __CustomClassWithNonConfigurable.register_property_rule(lambda _x, _y: None, name="non_configurable_rule",
                                                            configurable=False)

    non_configurable_property = __CustomClassWithNonConfigurable.property()
    with pytest.raises(ValueError) as error:
        non_configurable_property._add_rule_config("non_configurable_rule", "doesn't matter, should throw an error")
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


def test_setting_non_configurable_after_initialization_causes_value_error():
    class __CustomClass(ImmutableType):
        pass

    def non_configurable(instance, config):
        pass

    __CustomClass.register_property_rule(non_configurable, default="non-configurable-default", configurable=False)
    _property = __CustomClass.property()
    with pytest.raises(InvalidMethodUseError) as error:
        _property._setup_non_configurable_rule_config("non_configurable", "throws error")


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
