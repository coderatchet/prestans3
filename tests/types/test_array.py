import pytest
from prestans3.types import Array
from prestans3.types import String


def test_array_can_be_set_with_initial_iterable():
    array = Array(String, ['spam', 'ham'], validate_immediately=False)
    array_2 = Array(String, ('ham', 'spam'), validate_immediately=False)


def test_array_must_have_type_arg():
    with pytest.raises(TypeError):
        Array(['spam'], ['ham'], validate_immediately=False)
    array = Array(String, [], validate_immediately=False)


array = Array(String, ['spam', 'ham'], validate_immediately=False)


def test_array_can_equate_array_like_object():
    assert array == ['spam', 'ham']
    assert array == Array(String, ('spam', 'ham'), validate_immediately=False)
    assert not (array == ['no'])
    assert not (array == Array(String, ['no'], validate_immediately=False))


def test_array_can_perform_ne_with_array_like_object():
    assert array != ['ham', 'spam']
    assert not array != ['spam', 'ham']
    assert array != Array(String, ['no'], validate_immediately=False)
    assert not array != Array(String, ['spam', 'ham'], validate_immediately=False)


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


def test_can_drop_n_elements():
    Array(String, [1, 2, 3, 4, 5, 6, 7, 8, 9], validate_immediately=False).drop(3) == [4, 5, 6, 7, 8, 9]


def test_can_take_n_elements():
    Array(String, [1, 2, 3, 4, 5], validate_immediately=False).take(3) == [1, 2, 3]


# noinspection PyStatementEffect
def test_immutable_array_set_item_raises_error():
    with pytest.raises(AttributeError):
        array[0] = 'pinnaple'


def test_deleting_item_in_array_raises_error():
    with pytest.raises(AttributeError):
        del array[0]


def test_adding_non_of_type_subclass_to_array_raises_value_error():
    class MySuperString(String):
        pass

    __array = Array(String, validate_immediately=False)
    __array.append('this is a string')
    __array.append(String('this is a string'))
    __array.append(MySuperString('this is also a string'))
    with pytest.raises(ValueError):
        __array.append(1)
