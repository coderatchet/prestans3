# -*- coding: utf-8 -*-
"""
    tests.types.test_string
    ~~~~~~~~~~~~~~~~~~~~~~~

    A WSGI compliant REST micro-framework.

    :copyright: (c) 2016 Anomaly Software
    :license: Apache 2.0, see LICENSE for more details.
"""
import pytest

from prestans3.errors import ValidationException, PropertyConfigError
from prestans3.future import PYPY
from prestans3.types import Model
from prestans3.types import String
from prestans3.types.string import _prepare_trim, _prepare_normalize_whitespace


def test_can_create_string():
    String()


def test_can_init_string():
    String("init")


def test_string_can_eq_native():
    assert String("special") == 'special'
    assert not String("no") == 'special'


def test_string_can_ne_native():
    assert String("no") != "yes"
    assert not String("yes") != "yes"


def test_string_can_call_startswith():
    assert String("yes").startswith("ye")
    assert not String("no").startswith("o")


def test_from_value_works():
    String.from_value('string') == 'string'
    string = String('string')
    String.from_value(string) == string


def test_from_value_does_not_accept_non_string():
    with pytest.raises(TypeError) as error:
        String.from_value(1)
    assert '{} of type {} is not coercible to {}'.format(1, int.__name__, String.__name__) in str(error.value)


def test_min_length_works():
    class _Model(Model):
        string = String.property(min_length=3)

    model = _Model.mutable()
    model.string = 'str'
    model.validate()
    model.string = 'no'
    with pytest.raises(ValidationException) as exception:
        model.validate()
    assert '{} min_length config is {} however len("{}") == {}'.format(String.__name__, 3, 'no', 2) \
           in str(exception)


def test_max_length_works():
    class _Model(Model):
        string = String.property(max_length=2)

    model = _Model.mutable()
    model.string = 'no'
    model.validate()
    model.string = 'str'
    with pytest.raises(ValidationException) as exception:
        model.validate()
    assert '{} max_length config is {} however len("{}") == {}'.format(String.__name__, 2, 'str', 3) \
           in str(exception)


# noinspection PyUnusedLocal
def test_str_max_and_min_are_compatible_values():
    class _Model(Model):
        string = String.property(min_length=3, max_length=3)

    with pytest.raises(PropertyConfigError) as error:
        class __Model(Model):
            string = String.property(min_length=3, max_length=2)
    assert 'invalid {} property configuration: ' + \
           'min_length config of {} is greater than max_length config of {}'.format(String.__name__, 3, 2)


def test_str_regex_property_rule_works():
    class _Model(Model):
        string = String.property(format_regex=r'[abc][123]')

    model = _Model.mutable()
    model.string = 'a1'
    model.validate()
    model.string = 'c2'
    model.validate()
    model.string = 's1'
    with pytest.raises(ValidationException) as exception:
        model.validate()
    assert '{} does not match the format_regex {}'.format('s1', r'[abc][123]')


def test_prepare_trim_works():
    assert _prepare_trim(' hello') == 'hello'
    assert _prepare_trim(' hello ') == 'hello'
    assert _prepare_trim('hello ') == 'hello'


def test_prepare_trim_works_on_property():
    class _M(Model):
        my_string = String.property(prepare='trim')

    model = _M.mutable()
    model.my_string = ' hello'
    assert model.my_string == 'hello'
    model.my_string = 'hello '
    assert model.my_string == 'hello'
    model.my_string = '   hello        '
    assert model.my_string == 'hello'


def test_remove_whitespace():
    assert _prepare_normalize_whitespace('my        name is    bob   ') == 'my name is bob'


def test_remove_whitespace_works_on_property():
    class _M(Model):
        my_string = String.property(prepare='normalize_whitespace')

    model = _M.mutable()
    model.my_string = '   hello world      of white     space  removal         !  '
    assert model.my_string == 'hello world of white space removal !'


def test_string_accepts_unicode():
    String(u'unicode string')


def test_string_unicode_comparison_works():
    assert String('hello') == u'hello'
    assert String(u'hello') == String('hello')
    assert String(u'hello') == 'hello'
    assert String(u'hello') == u'hello'
    assert String('hello') != u'world'
    assert String(u'hello') != String('world')
    assert String(u'hello') != 'world'
    assert String(u'hello') != u'world'


def test_unicode_special_character_comparison_works():
    assert String(u'きたないのよりきれいな方がいい\n') == u'きたないのよりきれいな方がいい\n'
    assert String(u'きたないのよりきれいな方がいい\n') != u'きたないのよりきれいな方がい\n'


def test_encode_decode_property():
    string = String('utf-8')
    assert string.encode('utf-8').decode('utf-8') == string


def test_native_value():
    assert String("ok").native_value == "ok"
