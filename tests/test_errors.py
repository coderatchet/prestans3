# -*- coding: utf-8 -*-
"""
    tests.types.test_errors
    ~~~~~~~~~~~~~~

    A WSGI compliant REST micro-framework.

    :copyright: (c) 2016 Anomaly Software
    :license: Apache 2.0, see LICENSE for more details.
"""

from prestans3.errors import ValidationException, InvalidMethodUseError
from prestans3.types import String, Model

exception_1 = ValidationException(String)
exception_2 = ValidationException(String)


def test_validation_exception_has_reference_to_type_class():
    exception = ValidationException(String)
    assert exception.property_type == String
    pass


def test_validation_exception_has_an_empty_messages_array_on_no_init_message():
    exception = ValidationException(String)
    assert len(exception.messages) == 0


def test_leaf_validation_exception_has_correct_error_message():
    blurg = "min length should be blurg"
    exception = ValidationException(String, blurg)
    assert exception.messages[0] == blurg


class MyModel(Model):
    some_string = String.property()


# def test_validation_tree_can_accept_single_validation_message_in___init__

class MySuperModel(Model):
    some_model = MyModel.property()
    stringy_1 = String.property()
    stringy_2 = String.property()


# noinspection PyTypeChecker


def test_property_type_returns_correct_value():
    assert ValidationException(String).property_type == String
    assert ValidationException(MySuperModel, ('stringy_1', exception_1)).property_type == MySuperModel


# noinspection PyUnusedLocal
def test_can_use_iterator_syntax_for_validation_exception():
    exception = ValidationException(MyModel)
    exception.add_validation_message("yeah")
    tree_ = exception[0]
    for summary in exception:
        summary_ = summary[0]


def test_head_retrieves_first_exception_from_validation_exception():
    exception = ValidationException(String, "first error")
    exception.add_validation_message("second error")
    assert "first error" in str(exception.head)


def test_invalid_method_user_error_has_empty_message_if_not_specified():
    assert InvalidMethodUseError(lambda _: None).args[0] == ""
