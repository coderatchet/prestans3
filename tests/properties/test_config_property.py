# coding=utf-8
"""
    tests.test_config_property
    ~~~~~~~~~~~~~~~~~~~~~

    A WSGI compliant REST micro-framework.

    :copyright: (c) 2016 Anomaly Software
    :license: Apache 2.0, see LICENSE for more details.
"""
from prestans3.types.properties import TypeProperty

import pytest


def test_cannot_instantiate_base_property_abstract_class():
    with pytest.raises(Exception) as error:
        TypeProperty()
    assert str(error.value) == "Should not instantiate this class directly"
