# -*- coding: utf-8 -*-
"""
    tests.types.test_errors
    ~~~~~~~~~~~~~~

    A WSGI compliant REST micro-framework.

    :copyright: (c) 2016 Anomaly Software
    :license: Apache 2.0, see LICENSE for more details.
"""

import pytest
from prestans3.errors import ValidationException
from prestans3.types import Integer
from prestans3.types import String, Structure

exception_1 = ValidationException(String)
exception_2 = ValidationException(String)


def test_validation_exception_has_reference_to_type_class():
    exception = ValidationException(String)
    assert exception.property_type == String
    pass


def test_validation_exception_has_default_error_message():
    exception = ValidationException(String)
    assert len(exception.messages) > 0 and exception.messages[0] == "validation error for type String"


def test_leaf_validation_exception_has_correct_error_message():
    blurg = "min length should be blurg"
    exception = ValidationException(String, blurg)
    assert exception.messages[0] == blurg


class MyStructure(Structure):
    some_string = String.property()


def test_validation_error_can_have_child_validation_exception():
    validation_exception = ValidationException(String)
    validation_tree = ValidationException(MyStructure, ('some_string', validation_exception))
    assert isinstance(validation_tree.validation_exceptions['some_string'], ValidationException)
    assert validation_exception == validation_tree.validation_exceptions['some_string']


# def test_validation_tree_can_accept_single_validation_message_in___init__

class MySuperStructure(Structure):
    some_structure = MyStructure.property()
    stringy_1 = String.property()
    stringy_2 = String.property()


def test_can_append_additional_child_validation_exceptions_to_validation_exception():
    tree = ValidationException(MySuperStructure, ('stringy_1', exception_1))
    tree.add_validation_exception('stringy_2', exception_2)
    assert all([key in tree.validation_exceptions.keys() for key in ['stringy_1', 'stringy_2']])
    assert exception_1 == tree.validation_exceptions['stringy_1']
    assert exception_2 == tree.validation_exceptions['stringy_2']


# noinspection PyTypeChecker
def test_should_not_add_non_validation_exception_subclass_to_validation_tree_dict():
    tree = ValidationException(MySuperStructure, ('stringy_1', exception_1))
    with pytest.raises(TypeError):
        tree.add_validation_exception('stringy_2', "not an exception")
    with pytest.raises(TypeError):
        ValidationException(MySuperStructure, ('stringy_2', "also not an exception"))


def test_should_only_add_validation_exceptions_for_attribute_keys_of_defined_prestans_properties_contained_on_model_class_definition():
    tree = ValidationException(MySuperStructure, ('stringy_1', exception_1))
    with pytest.raises(AttributeError) as error:
        tree.add_validation_exception('not_an_attribute', exception_1)
    assert 'not_an_attribute is not a configured prestans attribute of MySuperStructure class, when trying to set validation exception' in str(
        error.value)


def test_should_raise_exception_when_adding_validation_exception_for_attribute_of_different_type():
    exception_integer = ValidationException(Integer)
    tree = ValidationException(MySuperStructure, ('stringy_1', exception_1))
    with pytest.raises(TypeError) as error:
        tree.add_validation_exception('stringy_2', exception_integer)
    assert 'validation exception for MySuperStructure.stringy_2 was of type Integer, ' + \
           'however MySuperStructure.stringy_2 is a String Property' \
           in str(error.value)
    with pytest.raises(TypeError) as error:
        ValidationException(MySuperStructure, ('stringy_2', exception_integer))
    assert 'validation exception for MySuperStructure.stringy_2 was of type Integer, ' + \
           'however MySuperStructure.stringy_2 is a String Property' \
           in str(error.value)


def test_property_type_returns_correct_value():
    assert ValidationException(String).property_type == String
    assert ValidationException(MySuperStructure, ('stringy_1', exception_1)).property_type == MySuperStructure


# noinspection PyUnusedLocal
def test_can_use_iterator_syntax_for_validation_exception():
    tree = ValidationException(MyStructure, ('some_string', exception_1))
    tree_ = tree[0]
    for summary in tree:
        summary_ = summary[0]


def test_can_retrieve_dict_of_validation_exceptions_by_qualified_name():
    sub_sub_exception = ValidationException(String)
    sub_exception = ValidationException(MyStructure, ('some_string', sub_sub_exception))
    exception = ValidationException(MySuperStructure, ('some_structure', sub_exception))


def test_nested_exception_message_correctly_constructed_from_root_exception_class():
    validation_exception = ValidationException(String)
    sub_validation_exception = ValidationException(MyStructure, ('some_string', validation_exception))
    super_validation_exception = ValidationException(MySuperStructure, ('some_structure', sub_validation_exception))
    expected_message = 'MySuperStructure.some_structure.some_string was invalid: ["validation error for type String"]'
    assert expected_message == str(super_validation_exception[0])
