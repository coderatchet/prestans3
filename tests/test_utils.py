from copy import copy

import pytest
from prestans3.errors import AccessError
from prestans3.utils import is_str, inject_class, MergingProxyDictionary


def test_is_str():
    assert is_str("yes")
    assert not is_str(1)


class InjectableClass(object):
    pass


def test_inject_class():
    class MyClass(object):
        pass

    new_type = inject_class(MyClass, InjectableClass)
    assert new_type.__bases__ == (InjectableClass, object)


def test_can_inject_class_with_more_than_one_subclass():
    class __A(object):
        pass

    class __B(object):
        pass

    class __C(__A, __B):
        pass

    new_type = inject_class(__C, InjectableClass)
    assert new_type.__name__ == 'Injected{}'.format(__C.__name__)
    first_base = new_type.__bases__[0]
    assert first_base.__name__ == 'Injected{}'.format(__A.__name__)
    assert first_base.__bases__ == (InjectableClass, object)
    second_base = new_type.__bases__[1]
    assert second_base.__name__ == 'Injected{}'.format(__B.__name__)
    assert second_base.__bases__ == (InjectableClass, object)


def test_can_inject_before_custom_class():
    class __A(object):
        pass

    class __B(object):
        pass

    class __C(__A, __B):
        pass

    new_type = inject_class(__C, InjectableClass, __B)
    assert new_type.__name__ == 'Injected{}'.format(__C.__name__)
    assert len(new_type.__bases__) == 3
    assert new_type.__bases__[0] is __A
    new_base = new_type.__bases__[1]
    assert new_base is InjectableClass
    assert new_type.__bases__[2] is __B
    assert new_type.mro() == [new_type, __A, InjectableClass, __B, object]


def test_can_inject_class_in_complex_hierarchy():
    class __A(object):
        pass

    class __B(object):
        pass

    class __X(__A, __B):
        pass

    class __Y(__A):
        pass

    class __Z(__X, __Y, __B):
        pass

    new_type = inject_class(__Z, InjectableClass, __B)
    assert len(new_type.__bases__) == 4
    __new_X = new_type.__bases__[0]
    assert __new_X.__name__ == 'Injected{}'.format(__X.__name__)
    assert len(__new_X.__bases__) == 3


def test_inject_class_returns_original_class_if_target_base_class_is_not_in_mro():
    class __A(object):
        pass

    class __B(object):
        pass

    class __C(__B):
        pass

    assert __A not in __C.mro()
    assert __C is inject_class(__C, InjectableClass, __A)


def test_can_customize_new_class_name():
    class __A(object):
        pass

    class __B(__A):
        pass

    def custom_name(x, _y, _z):
        return "Custom{}".format(x.__name__)

    new_type = inject_class(__B, InjectableClass, new_type_name_func=custom_name)
    assert new_type.__name__ == 'Custom{}'.format(__B.__name__)


def test_merging_dictionary_can_exist():
    dictionary = MergingProxyDictionary()
    assert len(dictionary) == 0


def test_merging_dictionary_can_access_all_keys():
    dictionary = MergingProxyDictionary({'foo': 'spam'}, {'bar': 'ham'})
    assert 'foo' in dictionary
    assert 'bar' in dictionary


def test_can_copy_merging_dictionary():
    dictionary = MergingProxyDictionary({'foo': 'bar'})
    copy1 = copy(dictionary)
    assert 'foo' in copy1
    assert copy1 is not dictionary


def test_merging_dictionary_can_retrieve_values():
    dictionary = MergingProxyDictionary({'foo': 'spam'}, {'bar': 'ham'})
    assert dictionary['foo'] == 'spam'
    assert dictionary['bar'] == 'ham'


def test_merging_dictionary_reports_correct_length():
    dictionary = MergingProxyDictionary()
    assert len(dictionary) == 0
    dictionary = MergingProxyDictionary({'foo': 'spam'}, {'bar': 'ham'})
    assert len(dictionary) == 2
    dictionary = MergingProxyDictionary({'foo': 'spam'}, {'foo': 'ham'})
    assert len(dictionary) == 1


def test_merging_dictionary_overrides_later_dictionariys_values():
    dictionary = MergingProxyDictionary({'foo': 'spam'}, {'foo': 'ham'})
    assert dictionary['foo'] == 'spam'
    assert len(dictionary) == 1


def test_merging_dictionary_raises_exception_when_setting_item():
    dictionary = MergingProxyDictionary()
    with pytest.raises(Exception):
        dictionary['foo'] = 'bar'


def test_merging_dictionary_raises_exception_when_deleting_items():
    dictionary = MergingProxyDictionary({'foo': 'bar'})
    with pytest.raises(Exception):
        del dictionary['foo']


def test_mutating_dictionaries_outside_affects_item_retrieval():
    my_dict = {}
    dictionary = MergingProxyDictionary(my_dict)
    assert len(dictionary) == 0
    my_dict['foo'] = 'bar'
    assert len(dictionary) == 1
    assert 'foo' in dictionary


def test_updating_merging_dictionary_raises_exception():
    dictionary = MergingProxyDictionary()
    with pytest.raises(AccessError):
        dictionary.update({"shouldnt": "work"})


def test_merging_dictionary_can_return_values():
    dictionary = MergingProxyDictionary({'foo': 'spam'}, {'bar': 'ham'}, {'foo': 'thankyoumam'})
    values = dictionary.values()
    assert len(values) == 2
    assert 'spam' in values
    assert 'ham' in values
    assert 'thankyouman' not in values


def test_merging_dictionary_can_return_keys():
    dictionary = MergingProxyDictionary({'foo': 'spam'}, {'bar': 'ham'}, {'foo': 'thankyoumam'})
    keys = dictionary.keys()
    assert len(keys) == 2
    assert 'foo' in keys
    assert 'bar' in keys


def test_key_not_found_raises_key_error():
    dictionary = MergingProxyDictionary({'foo': 'spam'}, {'bar': 'ham'})
    with pytest.raises(KeyError):
        # noinspection PyStatementEffect
        dictionary['notthere']


def test_merging_dictionary_can_see_items():
    dictionary = MergingProxyDictionary({'foo': 'spam'}, {'bar': 'ham'}, {'foo': 'thankyoumam'})
    items = dictionary.items()
    assert len(items) == 2


def test_pop_item_raises_exception():
    dictionary = MergingProxyDictionary({'foo': 'spam'}, {'bar': 'ham'}, {'foo': 'thankyoumam'})
    with pytest.raises(AccessError):
        dictionary.popitem()


def test_set_default_raises_exception():
    dictionary = MergingProxyDictionary({'foo': 'spam'}, {'bar': 'ham'}, {'foo': 'thankyoumam'})
    with pytest.raises(AccessError):
        dictionary.setdefault('doesnt', 'matter')


def test_pop_raises_exception():
    dictionary = MergingProxyDictionary({'foo': 'spam'}, {'bar': 'ham'}, {'foo': 'thankyoumam'})
    with pytest.raises(AccessError):
        dictionary.pop('doesnt', 'matter')