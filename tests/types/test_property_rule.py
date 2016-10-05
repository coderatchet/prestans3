import pytest, pytest_mock

from prestans3.types import ImmutableType, Container, Structure, _Property

# noinspection PyAbstractClass
from prestans3.types import String
from prestans3.errors import ValidationException


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
def test_valid_signature_of_owner_property_rule():
    class __OtherClassToRegisterWith(Container):
        pass

    def defined_function():
        return True

    with pytest.raises(ValueError) as error:
        __OtherClassToRegisterWith.register_owner_property_rule(defined_function)
    assert "expected owner_property_rule function with 3 arguments, received function with 0 argument(s): defined_function()" in \
           str(error.value)

    # noinspection PyUnusedLocal
    def better_defined_function(owner, instance, config):
        return True

    __OtherClassToRegisterWith.register_owner_property_rule(better_defined_function)


# noinspection PyAbstractClass
def test_can_store_property_rule_in_type():
    class __CustomClass(ImmutableType):
        pass

    # noinspection PyUnusedLocal
    def my_custom_property_rule(instance, config):
        pass

    __CustomClass.register_property_rule(my_custom_property_rule)
    # noinspection PyProtectedMember
    assert any([True if rule.__name__ == my_custom_property_rule.__name__ else False for rule in
                __CustomClass._property_rules.values()])


# noinspection PyAbstractClass
def test_can_store_owner_property_rule_in_type():
    class __CustomClass(Container):
        pass

    # noinspection PyUnusedLocal
    def my_custom_owner_property_rule(owner, instance, config):
        pass

    __CustomClass.register_owner_property_rule(my_custom_owner_property_rule)
    # noinspection PyProtectedMember
    assert any([True if rule.__name__ == my_custom_owner_property_rule.__name__ else False for rule in
                __CustomClass._owner_property_rules.values()])


# noinspection PyProtectedMember,PyAbstractClass,PyUnusedLocal
def test_can_name_property_rule():
    class __CustomClass2(ImmutableType):
        pass

    # noinspection PyUnusedLocal
    def my_custom_property_rule_nameable(instance, config):
        pass

    __CustomClass2.register_property_rule(property_rule=my_custom_property_rule_nameable, name="custom_prop")

    assert "custom_prop" in __CustomClass2._property_rules.keys()
    assert __CustomClass2.get_property_rule("custom_prop").__name__ == my_custom_property_rule_nameable.__name__


# noinspection PyProtectedMember,PyAbstractClass,PyUnusedLocal
def test_can_name_owner_property_rule():
    class __CustomClass3(Container):
        pass

    # noinspection PyUnusedLocal
    def my_custom_owner_property_rule_nameable(owner, instance, config):
        pass

    __CustomClass3.register_owner_property_rule(my_custom_owner_property_rule_nameable,
                                                name="custom_owner_prop")

    assert "custom_prop" in __CustomClass3._property_rules.keys()
    assert __CustomClass3.get_owner_property_rule(
        "custom_owner_prop").__name__ == my_custom_owner_property_rule_nameable.__name__


def test_can_add_rule_config(mocker):
    """
    :param pytest_mock.MockFixture mocker:
    """

    class __CustomClass(ImmutableType):
        pass

    mocker.patch('prestans3.types._Property')
    _property = _Property()
    _property._of_type = mocker.Mock()
    mocker.patch.dict(_property.property_type._property_rules, {"one_rule": lambda _x, _y: print("hello")})
    _property._add_rule_config("one_rule", "config")
    assert "one_rule" in _property.rules_config
    assert "config" == _property.rules_config['one_rule']


def test_can_find_config_by_rule_name(mocker):
    """
    :param pytest_mock.MockFixture mocker:
    """
    mocker.patch('prestans3.types._Property')
    _property = _Property()
    mocker.patch.dict(_property._rules_config, {"one_rule": "confighere"})
    assert 'confighere' == _property.get_rule_config('one_rule')


# noinspection PyAbstractClass
def test_can_set_default_configuration_for_rule(mocker):
    """
    :param pytest_mock.MockFixture mocker:
    """

    class _CustomClassDefaultConfiguration(ImmutableType):
        pass

    _CustomClassDefaultConfiguration.register_property_rule(lambda x, y: print("hello"), name="default_having_rule",
                                                            default="default config")
    assert "default config" == _CustomClassDefaultConfiguration.get_property_rule(
        "default_having_rule").default_config


def test_can_set_rule_as_non_configurable():
    class __CustomClassWithNonConfigurable(ImmutableType):
        pass

    __CustomClassWithNonConfigurable.register_property_rule(lambda x, y: print("hello"), name="non_configurable_rule",
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

    non_configurable_property = __CustomClassWithNonConfigurable.property()
    with pytest.raises(ValueError) as error:
        non_configurable_property._add_rule_config("non_configurable_rule", "doesn't matter, should throw an error")
    assert "non_configurable_rule is a non-configurable rule in class {}, (see {}.{}())" \
        .format(__CustomClassWithNonConfigurable.__name__,
                ImmutableType.__name__,
                ImmutableType.register_property_rule.__name__) in str(error.value)
