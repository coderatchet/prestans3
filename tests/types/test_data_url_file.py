# -*- coding: utf-8 -*-
"""
    tests.types.test_data_url_file
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    A WSGI compliant REST micro-framework.

    :copyright: (c) 2016 Anomaly Software
    :license: Apache 2.0, see LICENSE for more details.
"""

from prestans3.types.data_url_file import DataURLFile


def test_can_create_data_url_file():
    model = DataURLFile()
    assert model.__class__ is DataURLFile
