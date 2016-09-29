import pytest

from prestans3.types import String, Property, _required, ImmutableType

from prestans3.types import Structure



class MyClass(Structure):
    some_string = String.property()

def test_structure_class_can_contain_instances_of_MutableType_Property():
    assert isinstance(MyClass.__dict__['some_string'], Property)

def test_required_throws_exception_when_owner_is_none():
    with pytest.raises(ValueError) as value_error:
        _required(None, True, True)
    assert "owner instance can't be None" in str(value_error.value)

def test_required_throws_exception_when_owner_is_not_immutable_type_subclass():
    with pytest.raises(ValueError) as value_error:
        _required(True, True, True)
    assert "owner instance is not a subclass of {}".format(ImmutableType.__name__)

# def test_required_returns_true_if_provided_instance_not_none_and_config_is_True():
#     assert _required(MyClass(), True, True)
#
# def test_required_returns_true_if_provided_instance_is_none_and_config_is_False():
#     assert _required(None, False)
#
# def test_required_returns_false_if_provided_instance_is_false_and_config_is_True():
#     assert not _required(None, True)

# def test_invalid_instantiated_type_raises_exception():
#     # depends on validation conditions present
#     pass
#
# def test_immutable_structure_cant_set_attributes():
#     # depends on above test
#     my_class = MyClass()
#     with pytest.raises(Exception):
#         my_class.some_string = "jum"
#
#
# def test_prestans_attribute_is_instance_of_ImmutbaleType():
#     my_class = MyClass()
#     my_class.some_string = "jum"
#     assert isinstance(my_class.some_string, String)
#
# def test_required_rule():
#     class MyStructure(Structure):
#         some_string = String.property(required=True)
#
#     my_class = MyStructure()
#     validation = my_class.validate()
#     # assert validation is not None and not validation
