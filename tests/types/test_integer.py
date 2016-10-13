""" coding=utf-8 """

import pytest
from prestans3.errors import ValidationException

from prestans3.types import Integer, Model


def test_can_create_integer():
    myInt = Integer(1)


def test_integer_behaves_like_native_integer():
    myInt = Integer(3)
    assert myInt + 3 == 6
    assert myInt - 1 == 2
    assert myInt / 3 == 1
    assert myInt * 3 == 9
    myInt -= 2
    assert myInt == 1
    myInt += 2
    assert myInt == 3
    myInt /= 3
    assert myInt == 1
    myInt *= 3
    assert myInt == 3


def test_from_value_with_integer_instance_succeeds():
    integer = Integer(1)
    value = Integer.from_value(integer)
    assert value == integer


def test_from_value_with_native_int_succeeds():
    integer = 1
    value = Integer.from_value(integer)
    assert value == Integer(1)


def test_from_value_raises_value_error_on_non_int_subclass():
    with pytest.raises(ValueError):
        Integer.from_value('string')
    with pytest.raises(ValueError):
        Integer.from_value({})
    with pytest.raises(ValueError):
        Integer.from_value(0.3)


def test_min_property_rule_works():
    class __Model(Model):
        my_int = Integer.property(min=1)

    model = __Model.mutable()
    model.my_int = 1
    model.validate()
    model.my_int = 0
    with pytest.raises(ValidationException):
        model.validate()

#
# # noinspection PyTypeChecker
# def test_can_use_prestans3_integer_with_native_int_magic_methods_int():
#     class MockOwnerClass:
#         one = Integer(1)
#         two = Integer(2)
#         three = Integer(3)
#         four = Integer(4)
#
#     def __init__(self):
#         self.one = 1
#         self.two = 2
#         self.three = 3
#         self.four = 4
#
#     t = MockOwnerClass()
#     assert t.one + t.one == 2
#     assert t.two * t.two == 4
#     assert t.four / t.two == 2
#     assert float(t.four) + 0.1 == 4.1
#
# def test_mro_order():
#     mro = Integer.mro()
#     assert mro[:5] == [Integer,
#                        int,
#                        Number,
#                        Scalar,
#                        ImmutableType]
