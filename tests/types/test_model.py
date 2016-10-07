import pytest
from prestans3.errors import ValidationException
from prestans3.types import Integer, String
from prestans3.types.model import ModelValidationException
from tests.test_errors import MySuperModel, exception_1, MyModel, exception_2


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
    expected_message = 'MySuperModel.some_model.some_string was invalid: ["error with string"]'
    assert expected_message == str(super_validation_exception[0])

def test_cannot_add_validation_exception_to_scalar_validation_exception():
    model_exception = ModelValidationException(String, "error")
    with pytest.raises(TypeError):
        # noinspection PyUnresolvedReferences
        model_exception.add_validation_exception('not way', ValidationException(String, "error"))
