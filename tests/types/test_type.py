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

#
# def test_required_returns_true_if_provided_instance_is_none_and_config_is_False():
#     assert _required(None, False)
#
# def test_required_returns_false_if_provided_instance_is_false_and_config_is_True():
#     assert not _required(None, True)

# def test_invalid_instantiated_type_raises_exception():
#     # depends on validation conditions present
#     pass
#
# def test_immutable_model_cant_set_attributes():
#     # depends on above test
#     my_class = MyClass()
#     with pytest.raises(Exception):
#         my_class.some_string = "jum"
#
#
# def test_prestans_attribute_is_instance_of_ImmutbaleType():
#     my_class = MyClass()
#     my_class.some_string = "jum"
#     assert isinstance(my_class.some_string, String)
#
# def test_required_rule():
#     class MyModel(Model):
#         some_string = String.property(required=True)
#
#     my_class = MyModel()
#     validation = my_class.validate()
#     # assert validation is not None and not validation
