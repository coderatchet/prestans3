# -*- coding: utf-8 -*-
"""
    tests.test_utils
    ~~~~~~~~~~~~~~~~

    A WSGI compliant REST micro-framework.

    :copyright: (c) 2016 Anomaly Software
    :license: Apache 2.0, see LICENSE for more details.
"""

from copy import copy

import pytest
from future.types.newstr import unicode
from future.utils import with_metaclass

from prestans3.errors import AccessError
from prestans3.utils import inject_class, MergingProxyDictionary
import prestans3.utils as utils


class InjectableClass(object):
    pass


def test_inject_class():
    class MyClass(object):
        pass

    new_type = inject_class(MyClass, InjectableClass)
    assert new_type.__bases__ == (MyClass, InjectableClass, object)


# noinspection PyClassHasNoInit
def test_can_inject_class_with_more_than_one_subclass():
    class __A(object):
        pass

    class __B(object):
        pass

    class __C(__A, __B):
        pass

    new_type = inject_class(__C, InjectableClass)
    assert new_type.__name__ == 'Injected{}'.format(__C.__name__)
    assert new_type.__bases__[0] == __C
    assert new_type.__bases__[1].__name__ == utils.prefix_with_injected(__A, None, None)
    assert new_type.__bases__[2].__name__ == utils.prefix_with_injected(__B, None, None)
    injected_a = new_type.__bases__[1]
    injected_b = new_type.__bases__[2]

    assert injected_a.__bases__[0] == __A
    assert injected_a.__bases__[1] == InjectableClass
    assert injected_a.__bases__[2] == object
    assert injected_b.__bases__[0] == __B
    assert injected_b.__bases__[1] == InjectableClass
    assert injected_b.__bases__[2] == object


# noinspection PyClassHasNoInit
def test_can_inject_before_custom_class():
    class __A(object):
        pass

    class __B(object):
        pass

    class __C(__A, __B):
        pass

    new_type = inject_class(__C, InjectableClass, __B)
    assert new_type.__name__ == 'Injected{}'.format(__C.__name__)
    assert len(new_type.__bases__) == 4
    assert new_type.__bases__[0] is __C
    assert new_type.__bases__[1] is __A
    assert new_type.__bases__[2] is InjectableClass
    assert new_type.__bases__[3] is __B


# noinspection PyClassHasNoInit
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
    assert len(new_type.__bases__) == 5
    assert new_type.__bases__[0] is __Z
    assert new_type.__bases__[1].__name__ == utils.prefix_with_injected(__X, None, None)
    assert new_type.__bases__[2] is __Y
    assert new_type.__bases__[3] is InjectableClass
    assert new_type.__bases__[4] is __B


# noinspection PyClassHasNoInit
def test_inject_class_returns_original_class_if_target_base_class_is_not_in_mro():
    class __A(object):
        pass

    class __B(object):
        pass

    class __C(__B):
        pass

    assert __A not in __C.mro()
    assert __C is inject_class(__C, InjectableClass, __A)


def test_injected_class_initializes_with_proper_variables():
    class _A(object):
        def __init__(self):
            super(_A, self).__init__()
            self.foo = 'bar'

    class _B(object):
        def __init__(self):
            super(_B, self).__init__()
            self.foo = 'baz'

    new_type = inject_class(_B, _A)
    thing = new_type()
    assert thing.foo == 'baz'

    new_type = inject_class(_A, _B)
    thing = new_type()
    assert thing.foo == 'bar'


# noinspection PyUnusedLocal
def test_cached_object_returned_when_called_twice_with_same_args(mocker):
    """

    :param pytest_mock.MockFixture mocker:
    :return:
    """

    class __A(object):
        pass

    class __B(object):
        pass

    class Proof(object):
        pass

    mocker.patch.dict(utils.injected_class_cache, {(__B, __A, object, None): Proof})
    new_type = inject_class(__B, __A)
    test_type = inject_class(__B, __A)
    assert test_type is new_type
    assert test_type is Proof


# noinspection PyClassHasNoInit
def test_can_customize_new_class_name():
    class __A(object):
        pass

    class __B(__A):
        pass

    # noinspection PyUnusedLocal
    def custom_name(x, _y, _z):
        return "Custom{}".format(x.__name__)

    new_type = inject_class(__B, InjectableClass, new_type_name_func=custom_name)
    assert new_type.__name__ == 'Custom{}'.format(__B.__name__)


def test_new_type_is_sub_type_of_old_type_for_inject_class():
    class __A(object):
        pass

    class __B(object):
        pass

    new_type = inject_class(__B, __A, target_base_class=object)
    assert issubclass(new_type, __A)
    for thing in new_type.__bases__:
        if thing.__name__ == utils.prefix_with_injected(__A, None, None):
            assert issubclass(thing, __A)
            assert __A.mro()


# py2to3 remove when use cases are removed
def test_with_meta_class():
    class Meta(type):
        # noinspection PyMethodParameters,PyUnusedLocal
        def __init__(cls, name, bases, attrs, **kwargs):
            cls.attr = 'foo'
            super(Meta, cls).__init__(name, bases, attrs)

    class WithMeta(with_metaclass(Meta, object)):
        pass

    # noinspection PyUnresolvedReferences
    assert WithMeta.attr == 'foo'


def test_merging_dictionary_can_exist():
    dictionary = MergingProxyDictionary({})
    assert len(dictionary) == 0


def test_merging_dictionary_can_access_all_keys():
    dictionary = MergingProxyDictionary({'foo': 'spam'}, {'bar': 'ham'})
    assert 'foo' in dictionary
    assert 'bar' in dictionary


def test_can_copy_merging_dictionary():
    dictionary = MergingProxyDictionary({'foo': 'bar'}, {'baz': 'ham'}, MergingProxyDictionary({'spam': 'glam'}))
    copy1 = copy(dictionary)
    assert 'foo' in copy1
    assert 'baz' in copy1
    assert 'spam' in copy1
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


def test_merging_dictionary_overrides_later_dictionaries_values():
    dictionary = MergingProxyDictionary({'foo': 'spam'}, {'foo': 'ham'})
    assert dictionary['foo'] == 'spam'
    assert len(dictionary) == 1


def test_mutating_dictionaries_outside_affects_item_retrieval():
    other_dictionary = MergingProxyDictionary({})
    dictionary = MergingProxyDictionary({}, other_dictionary)
    assert len(dictionary) == 0
    other_dictionary['foo'] = 'bar'
    dictionary['ham'] = 'spam'
    assert len(dictionary) == 2
    assert 'foo' in dictionary
    assert 'ham' in dictionary


def test_merging_dictionary_can_return_values():
    dictionary = MergingProxyDictionary({'foo': 'spam'}, {'bar': 'ham'}, {'foo': 'thank you mam'})
    values = dictionary.values()
    assert len(values) == 2
    assert 'spam' in values
    assert 'ham' in values
    assert 'thank you mam' not in values


def test_merging_dictionary_can_return_keys():
    dictionary = MergingProxyDictionary({'foo': 'spam'}, {'bar': 'ham'}, {'foo': 'thank you mam'})
    keys = dictionary.keys()
    assert len(keys) == 2
    assert 'foo' in keys
    assert 'bar' in keys


def test_key_not_found_raises_key_error():
    dictionary = MergingProxyDictionary({'foo': 'spam'}, {'bar': 'ham'})
    with pytest.raises(KeyError):
        # noinspection PyStatementEffect
        dictionary['not there']


def test_can_determine_whether_key_is_own():
    dictionary = MergingProxyDictionary({'foo': 'spam'}, {'bar': 'ham'})
    assert dictionary.is_own_key('foo')
    assert not dictionary.is_own_key('bar')


def test_merging_dictionary_can_see_items():
    dictionary = MergingProxyDictionary({'foo': 'spam'}, {'bar': 'ham'}, {'foo': 'thank you mam'})
    items = dictionary.items()
    assert len(items) == 2


def test_get_returns_default_on_no_key():
    dictionary = MergingProxyDictionary({'foo': 'spam'}, {'bar': 'ham'}, {'foo': 'thank you mam'})
    assert dictionary.get('foo', 'bam') == 'spam'
    assert dictionary.get('bar', 'bam') == 'ham'
    assert dictionary.get('baz', 'bam') == 'bam'


def test_str_method_functioning():
    assert "'foo': 'bar'" in str(MergingProxyDictionary({'foo': 'bar'}, {'baz': 'spam'}))
    assert "'baz': 'spam'" in str(MergingProxyDictionary({'foo': 'bar'}, {'baz': 'spam'}))


def test_repr_method_functioning():
    assert "'foo': 'bar'" in repr(MergingProxyDictionary({'foo': 'bar'}, {'baz': 'spam'}))
    assert "'baz': 'spam'" in repr(MergingProxyDictionary({'foo': 'bar'}, {'baz': 'spam'}))


def test_can_set_item():
    dictionary = MergingProxyDictionary()
    dictionary['foo'] = 'bar'


def test_can_pop_item():
    dictionary = MergingProxyDictionary({'foo': 'bar'})
    pop = dictionary.popitem()
    assert pop == ('foo', 'bar')
    assert len(dictionary) == 0


def test_can_pop():
    dictionary = MergingProxyDictionary({'foo': 'bar'})
    pop = dictionary.pop('foo')
    assert pop == 'bar'
    assert len(dictionary) == 0
    pop = dictionary.pop('foo', 'spam')
    assert pop == 'spam'
    assert len(dictionary) == 0


def test_merging_dictionary_can_update():
    dictionary = MergingProxyDictionary({'foo': 'bar'})
    dictionary.update({'foo': 'baz', 'ham': 'spam'})
    assert dictionary['foo'] == 'baz'
    assert dictionary['ham'] == 'spam'


# noinspection PyStatementEffect
def test_merging_dictionary_can_clear_own_values_only():
    dictionary = MergingProxyDictionary({'baz': 'bar'}, {'spam': 'ham'})
    assert len(dictionary) == 2
    dictionary.clear()
    assert len(dictionary) == 1
    with pytest.raises(KeyError):
        dictionary['baz']
    assert dictionary['spam'] == 'ham'


def test_merging_dictionary_can_set_default():
    dictionary = MergingProxyDictionary({'foo': 'bar'})
    value = dictionary.setdefault('foo', 'baz')
    assert len(dictionary) == 1
    assert value == 'bar'
    value = dictionary.setdefault('ham', 'spam')
    assert len(dictionary) == 2
    assert value == 'spam'


def test_merging_dictionary_raises_exception_when_setting_item():
    dictionary = utils.ImmutableMergingDictionary()
    with pytest.raises(Exception):
        dictionary['foo'] = 'bar'


def test_merging_dictionary_raises_exception_when_deleting_items():
    dictionary = utils.ImmutableMergingDictionary({'foo': 'bar'})
    with pytest.raises(Exception):
        del dictionary['foo']


def test_pop_item_raises_exception():
    dictionary = utils.ImmutableMergingDictionary({'foo': 'spam'}, {'bar': 'ham'}, {'foo': 'thank you mam'})
    with pytest.raises(AccessError):
        dictionary.popitem()


def test_set_default_raises_exception():
    dictionary = utils.ImmutableMergingDictionary({'foo': 'spam'}, {'bar': 'ham'}, {'foo': 'thank you mam'})
    with pytest.raises(AccessError):
        dictionary.setdefault('doesnt', 'matter')


def test_pop_raises_exception():
    dictionary = utils.ImmutableMergingDictionary({'foo': 'spam'}, {'bar': 'ham'}, {'foo': 'thank you mam'})
    with pytest.raises(AccessError):
        dictionary.pop('doesnt', 'matter')


def test_clear_raises_exception():
    dictionary = utils.ImmutableMergingDictionary({'foo': 'spam'}, {'bar': 'ham'}, {'foo': 'thank you mam'})
    with pytest.raises(AccessError):
        dictionary.clear()


def test_update_raises_exception():
    dictionary = utils.ImmutableMergingDictionary({'foo': 'spam'}, {'bar': 'ham'}, {'foo': 'thank you mam'})
    with pytest.raises(AccessError):
        dictionary.update({'foo': 'no'})


def test_merging_dictionary_does_not_skip_items():
    dictionary = MergingProxyDictionary({'foo': 'bar'}, MergingProxyDictionary({'baz': 'spam'}),
                                        MergingProxyDictionary({'bar': 'ham'}))
    assert ('foo', 'bar') in dictionary.items()
    assert ('baz', 'spam') in dictionary.items()
    assert ('bar', 'ham') in dictionary.items()


def test_terminating_type_is_object_when_not_specified_for_lazy_one_way_graph():
    # noinspection PyProtectedMember
    assert utils.LazyOneWayGraph()._terminating_type is object


def test_merging_dictionary_can_access_own_items():
    dictionary = MergingProxyDictionary({'foo': 'bar'}, {'baz': 'spam'})
    assert dictionary.own_items() == {'foo': 'bar'}.items()


def test_merging_dictionary_can_access_own_keys():
    dictionary = MergingProxyDictionary({'foo': 'bar'}, {'baz': 'spam'})
    assert dictionary.own_keys() == {'foo': 'bar'}.keys()


def test_merging_dictionary_can_access_own_values():
    dictionary = MergingProxyDictionary({'foo': 'bar'}, {'baz': 'spam'})
    values = dictionary.own_values()
    assert len(values) == 1
    assert list(values)[0] == list({'foo': 'bar'}.values())[0]

def test_is_str_detects_proper_types():
    assert utils.is_str('')
    assert utils.is_str(u'')
    # py2to3 remove this test and optimize imports
    assert utils.is_str(unicode(''))
    assert not utils.is_str(1)
