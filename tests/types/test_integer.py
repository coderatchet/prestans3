""" coding=utf-8 """

import pytest

from prestans3.errors import ValidationException
from prestans3.types import Integer, MutableType


# def test_can_create_integer():
#     class HasInteger:
#         myInt = Integer(1)
#
#     HasInteger()
#
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


