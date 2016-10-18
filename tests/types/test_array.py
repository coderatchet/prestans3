# -*- coding: utf-8 -*-
"""
    tests.types.test_array
    ~~~~~~~~~~~~~~~~~~~~~~

    A WSGI compliant REST micro-framework.

    :copyright: (c) 2016 Anomaly Software
    :license: Apache 2.0, see LICENSE for more details.
"""

import pytest
from prestans3.errors import AccessError, ValidationException
from prestans3.types import Array
from prestans3.types import Integer
from prestans3.types import Model
from prestans3.types import String
from prestans3.types.array import _ArrayProperty


def test_array_can_be_set_with_initial_iterable():
    array = Array(String, ['spam', 'ham'], validate_immediately=False)
    array_2 = Array(String, ('ham', 'spam'), validate_immediately=False)


def test_array_must_have_type_arg():
    with pytest.raises(TypeError):
        Array(['spam', 'ham'], validate_immediately=False)
    array = Array(String, [], validate_immediately=False)


array = Array(String, ['spam', 'ham'], validate_immediately=False)


def test_array_can_equate_array_like_object():
    assert array == ['spam', 'ham']
    assert array == Array(String, ('spam', 'ham'), validate_immediately=False)
    assert not (array == ['spam'])
    assert not (array == Array(String, ['no'], validate_immediately=False))
    assert not (array == [1, 3])


def test_array_can_perform_ne_with_array_like_object():
    assert array != ['ham', 'spam']
    assert not array != ['spam', 'ham']
    assert array != Array(String, ['no'], validate_immediately=False)
    assert not array != Array(String, ['spam', 'ham'], validate_immediately=False)
    assert (array != [1])


def test_array_has_len():
    assert len(Array(String, ['no', 'way', 'hozay'], validate_immediately=False)) == 3
    assert len(Array(String, validate_immediately=False)) == 0


# noinspection PyStatementEffect
def test_array_has_get_item():
    assert array[0] == 'spam'
    assert array[1] == 'ham'
    with pytest.raises(IndexError):
        array[2]


# noinspection PyUnusedLocal
def test_array_has_iter():
    for i in array:
        pass


def test_array_has_reversed():
    assert reversed(array) == ['ham', 'spam']


def test_array_can_copy_itself():
    __copy = array.copy()
    assert __copy == array
    assert __copy is not array


def test_array_append_raises_access_error():
    with pytest.raises(AccessError) as error:
        array.append('jam')
    assert "append called on an immutable {class_name}".format(
        class_name=Array.__name__) in str(error.value)


def test_array_can_retrieve_tail():
    assert array.tail() == ['ham']


def test_array_can_retrieve_init():
    assert array.init() == ['spam']


def test_array_can_retrieve_head():
    assert array.head() == 'spam'


def test_array_can_retrieve_last():
    assert array.last() == 'ham'


def test_can_drop_n_elements():
    Array(Integer, [1, 2, 3, 4, 5, 6, 7, 8, 9], validate_immediately=False).drop(3) == [4, 5, 6, 7, 8, 9]


def test_can_take_n_elements():
    Array(Integer, [1, 2, 3, 4, 5], validate_immediately=False).take(3) == [1, 2, 3]


# noinspection PyStatementEffect
def test_immutable_array_set_item_raises_error():
    with pytest.raises(AccessError):
        array[0] = 'pinnaple'


def test_deleting_item_in_array_raises_error():
    with pytest.raises(AccessError):
        del array[0]


def test_adding_non_of_type_subclass_to_array_raises_value_error():
    class MySuperString(String):
        pass

    with pytest.raises(ValueError) as error:
        Array(String, [1])
    assert 'in Array.__init__, iterable[{}] is {} but the declared type of this array is {}'.format(0, 1,
                                                                                                    String.__name__) \
           in str(error)

    __array = Array.mutable(String, validate_immediately=False)
    __array.append('this is a string')
    __array.append(String('this is a string'))
    __array.append(MySuperString('this is also a string'))
    with pytest.raises(ValueError):
        __array.append(1)


def test_can_make_mutable_array():
    Array.mutable(String)


def test_mutable_can_set_item():
    my_array = Array.mutable(Integer, [2])
    my_array[0] = 1


def test_mutable_can_del_item():
    my_array = Array.mutable(Integer, [3])
    del my_array[0]
    assert len(my_array) == 0


def test_array_can_configure_property_rules_for_all_elements():
    _property = _ArrayProperty(of_type=Array, element_type=Integer, min=1)


def test_validate_elements_of_array_stops_at_first_error():
    class _Model(Model):
        int_array = Array.property(Integer, min=1)


def test_array_can_check_min_length():
    class _Model(Model):
        min_2_int_array = Array.property(Integer, min_length=2)

        def __init__(self):
            super(_Model, self).__init__({'min_2_int_array': [1]})

    with pytest.raises(ValidationException) as error:
        _Model()
    assert "{} instance length is {}, the minimum configured length is {}".format(Array.__class__, 1, 2)


def test_cannot_create_array_of_non_immutable_type():
    with pytest.raises(TypeError):
        Array(int)


def test_can_set_array_instance_to_model_property():
    class _Model(Model):
        my_array = Array.property(String)

    mutable = _Model.mutable()
    mutable.my_array = Array(String, ['foo'])


def test_unknown_property_rule_name_config_raises_value_error():
    with pytest.raises(ValueError) as error:
        _ArrayProperty(Array, Integer, unknown_rule=True)
    assert "'{key}={config}' config in {array_class_name}.__init__ was neither a property rule of " + \
           "'{array_class_name}' or a property rule of the element type '{element_type_name}'".format(
               key='unknown_rule', config=True, array_class_name=Array.__name__,
               element_type_name=Integer.__name__) in str(error.value)


def test_array_with_non_iterable_raises_type_error():
    with pytest.raises(TypeError) as error:
        Array(Integer, 6)
    assert 'iterable argument of type {} is not an iterable object'.format(int.__name__) in str(error.value)


def test_can_create_mutable_subclass_of_array():
    class _SubArray(Array):
        pass

    _SubArray.mutable(Integer, [1, 2, 3])


def test_array_does_not_accept_iterable_array_of_different_type():
    with pytest.raises(TypeError) as error:
        Array(Integer, Array(String))
    assert "element type '{}' of iterable is not a subclass of element type '{}' of self".format(String.__name__,
                                                                                                 Integer.__name__) \
           in str(error.value)


def test_array_element_rule_configuration_checks_elements():
    class _Model(Model):
        array = Array.property(Integer, min=1)

    model = _Model.mutable()
    model.array = [3, 4, 0, 2, -4]
    with pytest.raises(ValidationException):
        model.validate()


def test_array_validation_stops_at_first_error_by_default():
    class _Model(Model):
        array = Array.property(Integer, min=1)

    model = _Model.mutable()
    model.array = Array(Integer, [3, 4, 0, 2, -4])
    with pytest.raises(ValidationException) as exception:
        model.validate()
    assert '0' in str(exception)
    assert '-4' not in str(exception)


def test_array_from_value_raises_error_when_native_array_received():
    with pytest.raises(NotImplementedError) as error:
        Array.from_value([1, 2, 3, 4])
    assert '{class_name} must declare an explicit element type, create an array from an existing native array using ' + \
           'the constructor: {class_name}(<type>, native_array)'.format(class_name=Array.__name__) in str(error.value)


def test_array_from_value_with_array_type_returns_self():
    array = Array(String, ['spam', 'ham', 'bam'])
    assert Array.from_value(array) is array
