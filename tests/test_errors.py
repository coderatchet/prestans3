# -*- coding: utf-8 -*-
"""
    tests.test_errors
    ~~~~~~~~~~~~~~~~~

    A WSGI compliant REST micro-framework.

    :copyright: (c) 2016 Anomaly Software
    :license: Apache 2.0, see LICENSE for more details.
"""
import pytest
from prestans3.errors import ValidationException, InvalidMethodUseError
from prestans3.types import String, ImmutableType

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


# noinspection PyTypeChecker


def test_property_type_returns_correct_value():
    assert ValidationException(String).property_type == String


# noinspection PyUnusedLocal
def test_can_use_iterator_syntax_for_validation_exception():
    exception = ValidationException(String)
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


def test_str_method_on_exception_produces_valid_string():
    exception = ValidationException(String)
    exception.add_validation_messages(["some error", 'other error'])
    string = str(exception)
    assert '{} is invalid: ["some error", "other error"]'.format(String.__name__) in string


def test_validation_exception_can_only_be_for_prestans_types():
    with pytest.raises(TypeError) as error:
        ValidationException(int)
    assert 'validation exceptions are only valid for subclasses of {}, ' \
           'received type {}'.format(ImmutableType.__name__, int.__name__) in str(error.value)


def test_default_validation_exception_message():
    exception = ValidationException(String)
    expected_message = 'validation exception for type {}'.format(String.__name__)
    assert expected_message in exception._default_message()
    assert expected_message in str(exception)
