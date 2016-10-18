# -*- coding: utf-8 -*-
"""
    tests.types.temporal
    ~~~~~~~~~~~~~~~~~~~~

    A WSGI compliant REST micro-framework.

    :copyright: (c) 2016 Anomaly Software
    :license: Apache 2.0, see LICENSE for more details.
"""
from datetime import date

import pytest
from prestans3.errors import ValidationException
from prestans3.types import Date
from prestans3.types import Model


def test_after_works_property():
    class _Model(Model):
        my_date = Date.property(after=date(2000, 1, 1))

    model = _Model.mutable()
    model.my_date = Date(2000, 1, 2)
    model.validate()
    model.my_date = Date(2000, 1, 1)
    with pytest.raises(ValidationException) as exception:
        model.validate()
    assert "{} is not after configured temporal {}".format(Date(2000, 1, 1), Date(2000, 1, 1)) in str(exception)


def test_before_works_property():
    class _Model(Model):
        my_date = Date.property(before=date(2000, 1, 2))

    model = _Model.mutable()
    model.my_date = Date(2000, 1, 1)
    model.validate()
    model.my_date = Date(2000, 1, 2)
    with pytest.raises(ValidationException) as exception:
        model.validate()
    assert "{} is not before configured temporal {}".format(Date(2000, 1, 2), Date(2000, 1, 2)) in str(exception)
