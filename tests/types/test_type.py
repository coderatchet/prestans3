import pytest

from prestans3.types import String, _Property, ImmutableType, _MergingDictionaryWithMutableOwnValues

from prestans3.types import Model
from prestans3.utils import MergingProxyDictionary


class MyClass(Model):
    some_string = String.property()


def test_model_class_can_contain_instances_of_MutableType_Property():
    assert isinstance(MyClass.__dict__['some_string'], _Property)

def test_default_rules_config_returns_correctly():
    class __MyType(ImmutableType):
        pass

    __MyType.register_property_rule(lambda _x, _y: None, name="foo", default="baz")
    __MyType.register_property_rule(lambda _x, _y: None, name="bar")

    default_config = __MyType.default_rules_config()
    assert 'foo' in default_config
    assert 'bar' not in default_config
    assert default_config['foo'] == 'baz'

def test_merging_dictionary_with_own_mutable_values_returns_correct_value_for_is_own_key():
    dictionary = _MergingDictionaryWithMutableOwnValues(MergingProxyDictionary({'foo': 'spam'}, {'bar': 'baz'}))
    dictionary['bar'] = 'ham'
    assert dictionary.is_own_key('bar')
    assert not dictionary.is_own_key('foo')
    assert dictionary['bar'] == 'ham'

def test_direct_instance_of_immutable_type_raises_error_on_from_value():
    with pytest.raises(NotImplementedError):
        ImmutableType().from_value('irrelevant')

def test_update_on_merging_dict_with_mutable_own_values_can_accept_dict_lick_with_no_keys():
    class DictLike(object):
        def items(self):
            yield ('foo', 'bar')

    dictionary = _MergingDictionaryWithMutableOwnValues()
    dictionary.update(DictLike())
    assert 'foo' in dictionary
    assert dictionary['foo'] == 'bar'


# noinspection PyArgumentList
def test_update_behaves_like_normal_dict_update():
    values = [{'foo': 'bar'}, {'foo': 'spam', 'bar': 'ham'}]
    dictionary = {}
    dictionary.update(values[0], **values[1])
    merging_dictionary = _MergingDictionaryWithMutableOwnValues()
    merging_dictionary.update(values[0], **values[1])
    assert dictionary['foo'] == 'spam'
    assert dictionary['bar'] == 'ham'
    assert dictionary['foo'] == merging_dictionary['foo']
    assert dictionary['bar'] == merging_dictionary['bar']