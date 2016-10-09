import pytest
from prestans3.types import Array


def test_array_can_be_set_with_initial_iterable():
    array = Array(['spam', 'ham'], validate_immediately=False)
    array_2 = Array(('ham', 'spam'), validate_immediately=False)


def test_array_can_act_as_native_python_iterable():
    array = Array(['spam', 'ham'], validate_immediately=False)
    assert array == ['spam', 'ham']


# def test_iterable_set_item_raises_error():
#     iterable = MyIterable()
#     with pytest.raises(Exception):
#         iterable[0] = 'raises exception'
