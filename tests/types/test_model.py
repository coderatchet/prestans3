# -*- coding: utf-8 -*-
"""
    tests.types.test_model
    ~~~~~~~~~~~~~~~~~~~~~~

    A WSGI compliant REST micro-framework.

    :copyright: (c) 2016 Anomaly Software
    :license: Apache 2.0, see LICENSE for more details.
"""
import pytest
from prestans3.errors import ValidationException, AccessError
from prestans3.types import Integer, String, Model
from prestans3.types.model import ModelValidationException

exception_1 = ValidationException(String)
exception_2 = ValidationException(String)


class MyModel(Model):
    some_string = String.property()


# def test_validation_tree_can_accept_single_validation_message_in___init__

class MySuperModel(Model):
    some_model = MyModel.property(required=True)
    stringy_1 = String.property()
    stringy_2 = String.property()


def test_should_raise_exception_when_adding_validation_exception_for_attribute_of_different_type():
    exception_integer = ValidationException(Integer)
    model_exception = ModelValidationException(MySuperModel, ('stringy_1', exception_1))
    with pytest.raises(TypeError) as error:
        model_exception.add_validation_exception('stringy_2', exception_integer)
    assert 'validation exception for MySuperModel.stringy_2 was of type Integer, ' + \
           'however MySuperModel.stringy_2 is a String Property' \
           in str(error.value)
    with pytest.raises(TypeError) as error:
        ModelValidationException(MySuperModel, ('stringy_2', exception_integer))
    assert 'validation exception for MySuperModel.stringy_2 was of type Integer, ' + \
           'however MySuperModel.stringy_2 is a String Property' \
           in str(error.value)


def test_validation_error_can_have_child_validation_exception():
    validation_exception = ValidationException(String)
    model_exception = ModelValidationException(MyModel, ('some_string', validation_exception))
    assert isinstance(model_exception.validation_exceptions['some_string'], ValidationException)
    assert validation_exception == model_exception.validation_exceptions['some_string']


def test_can_append_additional_child_validation_exceptions_to_validation_exception():
    model_exception = ModelValidationException(MySuperModel, ('stringy_1', exception_1))
    model_exception.add_validation_exception('stringy_2', exception_2)
    assert all([key in model_exception.validation_exceptions.keys() for key in ['stringy_1', 'stringy_2']])
    assert exception_1 == model_exception.validation_exceptions['stringy_1']
    assert exception_2 == model_exception.validation_exceptions['stringy_2']


def test_should_not_add_non_validation_exception_subclass_to_model_validation_exceptions():
    model_exception = ModelValidationException(MySuperModel, ('stringy_1', exception_1))
    with pytest.raises(TypeError):
        model_exception.add_validation_exception('stringy_2', "not an exception")
    with pytest.raises(TypeError):
        ModelValidationException(MySuperModel, ('stringy_2', "also not an exception"))


def test_should_only_add_validation_exceptions_for_attribute_keys_of_defined_prestans_properties_contained_on_model_class_definition():
    model_exception = ModelValidationException(MySuperModel, ('stringy_1', exception_1))
    with pytest.raises(AttributeError) as error:
        model_exception.add_validation_exception('not_an_attribute', exception_1)
    assert 'not_an_attribute is not a configured prestans attribute of MySuperModel class, when trying to set validation exception' in str(
        error.value)


def test_can_retrieve_dict_of_validation_exceptions_by_qualified_name():
    sub_sub_exception = ValidationException(String)
    sub_model_exception = ModelValidationException(MyModel, ('some_string', sub_sub_exception))
    model_exception = ModelValidationException(MySuperModel, ('some_model', sub_model_exception))


def test_nested_exception_message_correctly_constructed_from_root_exception_class():
    validation_exception = ValidationException(String, "error with string")
    sub_validation_exception = ModelValidationException(MyModel, ('some_string', validation_exception))
    super_validation_exception = ModelValidationException(MySuperModel, ('some_model', sub_validation_exception))
    expected_message = 'MySuperModel.some_model.some_string is invalid: ["error with string"]'
    assert expected_message == str(super_validation_exception[0])


def test_cannot_add_validation_exception_to_scalar_validation_exception():
    model_exception = ModelValidationException(String, "error")
    with pytest.raises(TypeError):
        # noinspection PyUnresolvedReferences
        model_exception.add_validation_exception('not way', ValidationException(String, "error"))


def test_property_type_returns_correct_value():
    assert ModelValidationException(MySuperModel, ('stringy_1', exception_1)).property_type == MySuperModel


def test_can_make_mutable_version_of_model_class():
    mutable_model = MyModel.mutable()
    mutable_model.some_string = 'potato'


def test_cannot_make_mutable_of_base_model_class():
    with pytest.raises(TypeError):
        Model.mutable()


def test_model_validation_exception_iters_own_messages_and_attribute_messages():
    class __Model(Model):
        my_string = String.property()
        my_int = Integer.property()

    exception = ModelValidationException(__Model)
    exception.add_validation_messages(["own message"])
    exception.add_validation_exception("my_string", ValidationException(String, "invalid"))
    exception.add_validation_exception("my_int", ValidationException(Integer, "invalid"))

    def invalid_format(name, message):
        return '{} is invalid: ["{}"]'.format(name, message)

    assert invalid_format(__Model.__name__, "own message") in str(exception)
    assert invalid_format("{}.{}".format(__Model.__name__, 'my_string'), "invalid") in str(exception)
    assert invalid_format("{}.{}".format(__Model.__name__, 'my_int'), "invalid") in str(exception)


def test_immutable_type_cannot_set_prestans_attributes():
    class __Model(Model):
        my_string = String.property(required=False)

    model = __Model()
    with pytest.raises(AccessError) as error:
        model.my_string = "should not work"
    assert 'attempted to set value of prestans3 attribute on an immutable Model' in str(error.value)


def test_model_can_provide_initial_values_through_init_method():
    class _Model(Model):
        my_string = String.property()
        my_int = Integer.property()

        def __init__(self, my_string, my_int):
            super(_Model, self).__init__({'my_string': my_string, 'my_int': my_int})

    model = _Model('string', 1)
    assert model.my_int == 1
    assert model.my_string == 'string'


def test_cannot_del_prestans_attribute_on_immutable_model():
    class _Model(Model):
        def __init__(self, string):
            super(_Model, self).__init__({'my_string': 'cannot delete'})

        my_string = String.property(required=False)

    model = _Model('cannot delete')
    assert model.my_string == 'cannot delete'
    with pytest.raises(AccessError) as error:
        del model.my_string
    assert 'attempted to delete value of prestans3 attribute on an immutable Model' in str(error.value)

def test_cannot_pass_non_prestans_attributes_to_super_init_method():
    class _Model(Model):
        def __init__(self):
            super(_Model, self).__init__({'not_an_attribute': 'doesn\'t matter'})

    with pytest.raises(ValueError):
        _Model()
