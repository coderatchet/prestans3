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


def test_array_has_len():
    assert len(Array(['no', 'way', 'hozay'], validate_immediately=False)) == 3
    assert len(Array(validate_immediately=False)) == 0


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


def test_array_can_append():
    __my_array = array.copy()
    __my_array.append('jam')
    assert __my_array == ['spam', 'ham', 'jam']


def test_array_can_retrieve_tail():
    assert array.tail() == ['ham']


def test_array_can_retrieve_init():
    assert array.init() == ['spam']


def test_array_can_retrieve_head():
    assert array.head() == 'spam'

def test_array_can_retrieve_last():
    assert array.last() == 'ham'
