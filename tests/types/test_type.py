from urllib.request import Request

from prestans3.types import String, Property

from prestans3.types import MutableType, Structure, Scalar


# def test_can_call_Property_class_():
#     ImmutableType.Property()
#     assert str(error.value) == "Should not instantiate this class directly"

# def test_can_set_and_get_subclass_property_instance():
#     class MyType(MutableType):
#         pass
#
#     class MyModel(MutableType):
#         my_type = MyType.Property()
#
#     model = MyModel()
#     model.my_type = "jum"
#     assert model.my_type == 'jum'
#
#
# def test_can_set_request_data_as_custom_class():
#     request = Request('http://www.example.com')
#     request.data = MutableType.Property()
#     request.data = "jum"
#     assert request.data == "jum"
class MyClass(Structure):
    some_string = String.property()


def test_structure_class_can_contain_instances_of_MutableType_Property():
    assert isinstance(MyClass.__dict__['some_string'], Property)


def test_structure_can_set_and_get_a_prestans_attribute():
    my_class = MyClass()
    my_class.some_string = "jum"
    assert "jum" == my_class.some_string


def test_prestans_attribute_is_instance_of_MutableType():
    my_class = MyClass()
    my_class.some_string = "jum"
    assert isinstance(my_class.some_string, String)


def test_required_rule():
    class MyClass(Structure):
        some_string = String.property(required=True)

    my_class = MyClass()
    assert not my_class.validate()
