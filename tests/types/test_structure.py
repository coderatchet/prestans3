import pytest

from prestans3.types import Structure
from prestans3.types import _MutableStructure
from prestans3.types import String


class MyImmutableStructure(Structure):
    string_property = String.property()

class MySecondInheritance(MyImmutableStructure):
    another_property = String.property()

# def test_mutable_method():
#
#     my_i = MyImmutableStructure()
#
#     assert isinstance(my_i, MyImmutableStructure)
#     assert isinstance(my_i, Structure)
#
#     with pytest.raises(Exception):
#         my_i.string_property = "something"
#
#     my_m = my_i.mutable()
#
#     assert isinstance(my_i, MyImmutableStructure)
#     assert isinstance(my_m, Structure)
#     assert isinstance(my_m, _MutableStructure)
#
#     my_m.string_property = "something"
#
#     my_2i = MySecondInheritance()
#     my2_m = my_2i.mutable()
#
#     with pytest.raises(Exception):
#         my_2i.another_property = "something"
#
#     assert isinstance(my_2i, MyImmutableStructure)
#     assert isinstance(my2_m, Structure)
#     assert isinstance(my2_m, _MutableStructure)
#
#     my2_m.string_property = "something"
#
#     assert False