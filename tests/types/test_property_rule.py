import pytest

from prestans3.types import ImmutableType, Container


# noinspection PyAbstractClass
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

# def test_property_rule_should_not_validate_on_non_instances_or_subclasses_of_owning_class():
#     MyClass()
#     with pytest.raises(TypeError):
#         MyClass._property_rules
#
#
# def test_property_rule_annotated_function_in_immutable_type_subclass_stores_rule_in_class():
#     assert MyClass.my_property_rule in MyClass._property_rules
#
#
# def test_method_decorated_with_property_rule_should_raise_exception_if_return_value_not_True():
#     class MyIncorrectClass(ImmutableType):
#         @PropertyRule
#         def my_incorrect_property_rule(self):
#             return "True"
#
#     with pytest.raises(Exception):
#         MyIncorrectClass.my_incorrect_property_rule()
#
#
# def test_method_decorated_with_property_rule_should_raise_subclass_of_exception_when_invalid():
#     pass
#
#
# def test_property_rule_is_nameable():
#     # depends on property rule being stored somewhere
#     pass
