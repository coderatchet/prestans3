from prestans3.types import String, Property

from prestans3.types import Structure


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
    class MyStructure(Structure):
        some_string = String.property(required=True)

    my_class = MyStructure()
    validation = my_class.validate()
    # assert validation is not None and not validation
