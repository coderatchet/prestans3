from prestans3.types import Model
from prestans3.types import String


class MyImmutableModel(Model):
    string_property = String.property()

class MySecondInheritance(MyImmutableModel):
    another_property = String.property()

# def test_mutable_method():
#
#     my_i = MyImmutableModel()
#
#     assert isinstance(my_i, MyImmutableModel)
#     assert isinstance(my_i, Model)
#
#     with pytest.raises(Exception):
#         my_i.string_property = "something"
#
#     my_m = my_i.mutable()
#
#     assert isinstance(my_i, MyImmutableModel)
#     assert isinstance(my_m, Model)
#     assert isinstance(my_m, _MutableModel)
#
#     my_m.string_property = "something"
#
#     my_2i = MySecondInheritance()
#     my2_m = my_2i.mutable()
#
#     with pytest.raises(Exception):
#         my_2i.another_property = "something"
#
#     assert isinstance(my_2i, MyImmutableModel)
#     assert isinstance(my2_m, Model)
#     assert isinstance(my2_m, _MutableModel)
#
#     my2_m.string_property = "something"
#
#     assert False