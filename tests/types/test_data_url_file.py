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
    data_url_file = DataURLFile()
    assert data_url_file.__class__ is DataURLFile

def test_can_create_uuid():
    uuid = DataURLFile.generate_filename()
    assert isinstance(uuid, str)
    assert len(uuid) == 32

