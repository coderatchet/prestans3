# -*- coding: utf-8 -*-
"""
    tests.types.test_data_url_file
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    A WSGI compliant REST micro-framework.

    :copyright: (c) 2016 Anomaly Software
    :license: Apache 2.0, see LICENSE for more details.
"""
import base64

import pytest

from prestans3.types.data_url_file import DataURLFile


def test_can_create_data_url_file():
    # small red dot png
    data_url_file = DataURLFile("data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAUAAAAFCAYAAACNbyblAAAAHElEQVQI12P4//8"
                                "/w38GIAXDIBKE0DHxgljNBAAO9TXL0Y4OHwAAAABJRU5ErkJggg==")
    assert data_url_file.__class__ is DataURLFile


def test_can_create_uuid():
    uuid = DataURLFile.generate_filename()
    assert isinstance(uuid, str)
    assert len(uuid) == 32


def test_can_extract_parts():
    data_url_file = DataURLFile("data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAUAAAAFCAYAAACNbyblAAAAHElEQVQI12P4//8"
                                "/w38GIAXDIBKE0DHxgljNBAAO9TXL0Y4OHwAAAABJRU5ErkJggg==")
    assert data_url_file.mime_type == 'image/png'
    assert data_url_file.encoding == 'base64'
    assert data_url_file.contents == "iVBORw0KGgoAAAANSUhEUgAAAAUAAAAFCAYAAACNbyblAAAAHElEQVQI12P4//8" + \
                                     "/w38GIAXDIBKE0DHxgljNBAAO9TXL0Y4OHwAAAABJRU5ErkJggg=="


def test_raises_error_if_data_is_invalid():
    with pytest.raises(ValueError) as error:
        DataURLFile("")
    assert "encoded_data was not in the expected format. for an explaination of how to format a data url file, see " + \
           "https://en.wikipedia.org/wiki/Data_URI_scheme" in str(error.value)
    with pytest.raises(ValueError) as error:
        DataURLFile(
            "invalidprependdata:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAUAAAAFCAYAAACNbyblAAAAHElEQVQI12P4//8"
            "/w38GIAXDIBKE0DHxgljNBAAO9TXL0Y4OHwAAAABJRU5ErkJggg==")
    assert "encoded_data was not in the expected format. for an explaination of how to format a data url file, see " + \
           "https://en.wikipedia.org/wiki/Data_URI_scheme" in str(error.value)


def test_can_get_decoded_contents():
    url_file = DataURLFile("data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAUAAAAFCAYAAACNbyblAAAAHElEQVQI12P4//8"
                           "/w38GIAXDIBKE0DHxgljNBAAO9TXL0Y4OHwAAAABJRU5ErkJggg==")
    assert url_file.decoded_contents == base64.decodestring(
        "iVBORw0KGgoAAAANSUhEUgAAAAUA AAAFCAYAAACNbyblAAAAHElEQVQI12P4//8"
        "/w38GIAXDIBKE0DHxgljNBAAO9TXL0Y4OHwAAAABJRU5ErkJggg==")
