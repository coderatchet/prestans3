# -*- coding: utf-8 -*-
"""
    tests.types.test_validation_tree
    ~~~~~~~~~~~~~~

    A WSGI compliant REST micro-framework.

    :copyright: (c) 2016 Anomaly Software
    :license: Apache 2.0, see LICENSE for more details.
"""

import pytest
from prestans3.types import Integer

from prestans3.types import String, Structure
from prestans3.validation_tree import LeafValidationException, ValidationTree, \
    ValidationTreeNode, LeafValidationSummary

exception_1 = LeafValidationException(String)
exception_2 = LeafValidationException(String)


def test_leaf_validation_exception_has_reference_to_type_class():
    exception = LeafValidationException(String)
    assert exception.property_type == String
    pass


def test_leaf_validation_exception_has_default_error_message():
    exception = LeafValidationException(String)
    assert exception.message is not None and exception.message == "validation error for type String"


def test_leaf_validation_exception_has_correct_error_message():
    blurg = "min length should be blurg"
    exception = LeafValidationException(String, blurg)
    assert exception.message == blurg


class MyStructure(Structure):
    some_string = String.property()


def test_validation_tree_has_reference_to_type_class():
    exception = LeafValidationException(String)
    validation_tree = ValidationTree(MyStructure, ('some_string', exception))
    assert validation_tree.property_type == MyStructure


def test_validation_tree_can_have_linked_leaf_validation_exception():
    validation_exception = LeafValidationException(String)
    validation_tree = ValidationTree(MyStructure, ('some_string', validation_exception))
    assert isinstance(validation_tree.validation_exceptions['some_string'], ValidationTreeNode)
    assert validation_exception == validation_tree.validation_exceptions['some_string']


class MySuperStructure(Structure):
    some_structure = MyStructure.property()
    stringy_1 = String.property()
    stringy_2 = String.property()


def test_validation_tree_can_have_linked_validation_tree_as_node():
    exception = LeafValidationException(String)
    sub_tree = ValidationTree(MyStructure, ('some_string', exception))
    tree = ValidationTree(MySuperStructure, ('some_structure', sub_tree))
    assert isinstance(tree.validation_exceptions['some_structure'], ValidationTree)


def test_can_append_additional_tree_nodes_to_validation_tree():
    tree = ValidationTree(MySuperStructure, ('stringy_1', exception_1))
    tree.add_validation_exception('stringy_2', exception_2)
    assert all([key in tree.validation_exceptions.keys() for key in ['stringy_1', 'stringy_2']])
    assert exception_1 == tree.validation_exceptions['stringy_1']
    assert exception_2 == tree.validation_exceptions['stringy_2']


# noinspection PyTypeChecker
def test_should_not_add_non_tree_node_subclass_to_validation_tree_dict():
    tree = ValidationTree(MySuperStructure, ('stringy_1', exception_1))
    with pytest.raises(TypeError):
        tree.add_validation_exception('stringy_2', "not an exception")
    with pytest.raises(TypeError):
        tree.add_validation_exception('stringy_2', ValidationTreeNode(String))
    with pytest.raises(TypeError):
        ValidationTree(MySuperStructure, ('stringy_2', "also not an exception"))


def test_should_only_add_validation_exceptions_for_attribute_keys_of_defined_prestans_properties_contained_on_model_class_definition():
    tree = ValidationTree(MySuperStructure, ('stringy_1', exception_1))
    with pytest.raises(AttributeError) as error:
        tree.add_validation_exception('not_an_attribute', exception_1)
    assert 'not_an_attribute is not a configured prestans attribute of MySuperStructure class, when trying to set Validation Exception' in str(
        error.value)


def test_should_raise_exception_when_adding_validation_exception_for_attribute_of_different_type():
    exception_integer = LeafValidationException(Integer)
    tree = ValidationTree(MySuperStructure, ('stringy_1', exception_1))
    with pytest.raises(TypeError) as error:
        tree.add_validation_exception('stringy_2', exception_integer)
    assert 'validation exception for MySuperStructure.stringy_2 was of type Integer, ' + \
           'however MySuperStructure.stringy_2 is a String Property' \
           in str(error.value)
    with pytest.raises(TypeError) as error:
        ValidationTree(MySuperStructure, ('stringy_2', exception_integer))
    assert 'validation exception for MySuperStructure.stringy_2 was of type Integer, ' + \
           'however MySuperStructure.stringy_2 is a String Property' \
           in str(error.value)


def test_property_type_returns_correct_value():
    assert LeafValidationException(String).property_type == String
    assert ValidationTree(MySuperStructure, ('stringy_1', exception_1)).property_type == MySuperStructure


def test_cannot_make_validation_tree_for_scalar():
    with pytest.raises(TypeError) as error:
        ValidationTree(String, ('what?', exception_1))
    assert 'validation trees are only valid for Types with configured prestans attributes' in str(error.value)


# noinspection PyUnusedLocal
def test_can_use_iterator_syntax_for_validation_tree():
    tree = ValidationTree(MyStructure, ('some_string', exception_1))
    tree_ = tree[0]
    for summary in tree:
        summary_ = summary[0]


def test_can_retrieve_dict_of_validation_exceptions_by_qualified_name():
    exception = LeafValidationException(String)
    sub_tree = ValidationTree(MyStructure, ('some_string', exception))
    tree = ValidationTree(MySuperStructure, ('some_structure', sub_tree))
    for val1, val2 in zip(LeafValidationSummary('MySuperStructure', 'some_structure.some_string', exception), tree[0]):
        assert val2 == val2


def test_nested_exception_message_correctly_constructed_from_root_exception_class():
    exception = LeafValidationException(String)
    sub_tree = ValidationTree(MyStructure, ('some_string', exception))
    tree = ValidationTree(MySuperStructure, ('some_structure', sub_tree))
    expected_message = 'MySuperStructure.some_structure.some_string was invalid: validation error for type String'
    assert expected_message == tree[0].message
