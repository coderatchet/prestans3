import pytest
from prestans3.types import Array


def test_array_can_be_set_with_initial_iterable():
    array = Array(['spam', 'ham'], validate_immediately=False)
    array_2 = Array(('ham', 'spam'), validate_immediately=False)


array = Array(['spam', 'ham'], validate_immediately=False)


def test_array_can_equate_array_like_object():
    assert array == ['spam', 'ham']
    assert array == Array(('spam', 'ham'), validate_immediately=False)
    assert not (array == ['no'])
    assert not (array == Array(['no'], validate_immediately=False))


def test_array_can_perform_ne_with_array_like_object():
    assert array != ['ham', 'spam']
    assert not array != ['spam', 'ham']
    assert array != Array(['no'], validate_immediately=False)
    assert not array != Array(['spam', 'ham'], validate_immediately=False)

# def test_iterable_set_item_raises_error():
#     iterable = MyIterable()
#     with pytest.raises(Exception):
#         iterable[0] = 'raises exception'
