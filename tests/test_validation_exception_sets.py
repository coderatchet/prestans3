# -*- coding: utf-8 -*-
"""
    tests.types.test_validation_exception_set
    ~~~~~~~~~~~~~~

    A WSGI compliant REST micro-framework.

    :copyright: (c) 2016 Anomaly Software
    :license: Apache 2.0, see LICENSE for more details.
"""

# should be able to easily identity which nested property is wrong and why should report all failures, not just the
# first. an exception should be "aware" of what namespace it's in a property name should be relative to the root object

# scalars produce leaf exceptions
# structures produce a set of named leaf exceptions
# nested structures append it's namespace to nested sets of exceptions
# the 'namespace' of an object is it's class name
# but when nesting exceptions, the class name of the original validation exception, becomes the property name of the
# owning class


# e.g, should have an end result that produces error like: MyClass.sub_thing.some_attr was invalid because "min
# length of SubThingClass.some_attr min_length is 10 and len('doofus') is 6"
from prestans3.types import String
from prestans3.validation_exception_set import LeafException, DEFAULT_VALIDATION_MESSAGE


def test_leaf_exception_has_reference_to_type_class():
    exception = LeafException(String)
    assert exception._of_type == String
    pass


def test_leaf_exception_has_default_error_message():
    exception = LeafException(String)
    assert exception.message is not None and exception.message == DEFAULT_VALIDATION_MESSAGE
