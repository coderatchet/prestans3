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


def test_can_compile_data_url_from_value():
    existing_ = DataURLFile("data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAUAAAAFCAYAAACNbyblAAAAHElEQVQI12P4//8" \
                            "/w38GIAXDIBKE0DHxgljNBAAO9TXL0Y4OHwAAAABJRU5ErkJggg==")
    assert DataURLFile.from_value(existing_) is existing_
    data_url_file = DataURLFile.from_value("data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAUAAAAFCAYAAACNbyblAAAAHElEQ"
                                           "VQI12P4//8/w38GIAXDIBKE0DHxgljNBAAO9TXL0Y4OHwAAAABJRU5ErkJggg==")
    assert data_url_file.mime_type == 'image/png'
    assert data_url_file.encoding == 'base64'
    assert data_url_file.contents == "iVBORw0KGgoAAAANSUhEUgAAAAUAAAAFCAYAAACNbyblAAAAHElEQVQI12P4//8" + \
                                     "/w38GIAXDIBKE0DHxgljNBAAO9TXL0Y4OHwAAAABJRU5ErkJggg=="
    with pytest.raises(TypeError) as error:
        DataURLFile.from_value(123)
    assert "{} of type {} is not coercible to type {}".format(123, int.__name__, DataURLFile.__name__) \
           in str(error.value)


def test_can_eq():
    assert DataURLFile("data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAUAAAAFCAYAAACNbyblAAAAHElEQVQI12P4//8"
                       "/w38GIAXDIBKE0DHxgljNBAAO9TXL0Y4OHwAAAABJRU5ErkJggg==") == \
           DataURLFile("data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAUAAAAFCAYAAACNbyblAAAAHElEQVQI12P4//8"
                       "/w38GIAXDIBKE0DHxgljNBAAO9TXL0Y4OHwAAAABJRU5ErkJggg==")

    # different contents
    assert not DataURLFile("data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAUAAAAFCAYAAACNbyblAAAAHElEQVQI12P4//8"
                           "/NOTTHESAME==") == \
               DataURLFile("data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAUAAAAFCAYAAACNbyblAAAAHElEQVQI12P4//8"
                           "/w38GIAXDIBKE0DHxgljNBAAO9TXL0Y4OHwAAAABJRU5ErkJggg==")

    # different encoding
    assert not DataURLFile("data:image/png;base32,ABC=") == \
               DataURLFile("data:image/png;base64,ABC=")

    # different mime type
    assert not DataURLFile(("data:image/jpg;base64,iVBORw0KGgoAAAANSUhEUgAAAAUAAAAFCAYAAACNbyblAAAAHElEQVQI12P4//8"
                            "/w38GIAXDIBKE0DHxgljNBAAO9TXL0Y4OHwAAAABJRU5ErkJggg==")) == \
               DataURLFile(("data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAUAAAAFCAYAAACNbyblAAAAHElEQVQI12P4//8"
                            "/w38GIAXDIBKE0DHxgljNBAAO9TXL0Y4OHwAAAABJRU5ErkJggg=="))

    assert not DataURLFile("data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAUAAAAFCAYAAACNbyblAAAAHElEQVQI12P4//8"
                           "/w38GIAXDIBKE0DHxgljNBAAO9TXL0Y4OHwAAAABJRU5ErkJggg==") == 1


def test_can_ne():
    assert not DataURLFile("data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAUAAAAFCAYAAACNbyblAAAAHElEQVQI12P4//8"
                           "/w38GIAXDIBKE0DHxgljNBAAO9TXL0Y4OHwAAAABJRU5ErkJggg==") != \
               DataURLFile("data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAUAAAAFCAYAAACNbyblAAAAHElEQVQI12P4//8"
                           "/w38GIAXDIBKE0DHxgljNBAAO9TXL0Y4OHwAAAABJRU5ErkJggg==")

    # different contents
    assert DataURLFile("data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAUAAAAFCAYAAACNbyblAAAAHElEQVQI12P4//8"
                       "/NOTTHESAME==") != \
           DataURLFile("data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAUAAAAFCAYAAACNbyblAAAAHElEQVQI12P4//8"
                       "/w38GIAXDIBKE0DHxgljNBAAO9TXL0Y4OHwAAAABJRU5ErkJggg==")

    # different encoding
    assert DataURLFile("data:image/png;base32,ABC=") != \
           DataURLFile("data:image/png;base64,ABC=")

    # different mime type
    assert DataURLFile(("data:image/jpg;base64,iVBORw0KGgoAAAANSUhEUgAAAAUAAAAFCAYAAACNbyblAAAAHElEQVQI12P4//8"
                        "/w38GIAXDIBKE0DHxgljNBAAO9TXL0Y4OHwAAAABJRU5ErkJggg==")) != \
           DataURLFile(("data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAUAAAAFCAYAAACNbyblAAAAHElEQVQI12P4//8"
                        "/w38GIAXDIBKE0DHxgljNBAAO9TXL0Y4OHwAAAABJRU5ErkJggg=="))

    assert DataURLFile("data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAUAAAAFCAYAAACNbyblAAAAHElEQVQI12P4//8"
                       "/w38GIAXDIBKE0DHxgljNBAAO9TXL0Y4OHwAAAABJRU5ErkJggg==") != 1


def test_can_compile_data_url_from_parts():
    data_url_file = DataURLFile.create(
        contents='abc', encoding='base64', mime_type='image/png')
    assert data_url_file.contents == 'YWJj'
    assert data_url_file.encoding == 'base64'
    assert data_url_file.mime_type == 'image/png'


def test_create_url_from_parts_raises_error_on_invalid_params():
    with pytest.raises(TypeError) as error:
        DataURLFile.create(contents=123, encoding='base64', mime_type='image/png')
    assert "contents, mime_type and encoding should all be strings" in str(error.value)
    with pytest.raises(TypeError) as error:
        DataURLFile.create(contents='ABC=', encoding=5.2, mime_type='image/png')
    assert "contents, mime_type and encoding should all be strings" in str(error.value)
    with pytest.raises(TypeError) as error:
        DataURLFile.create(contents='ABC=', encoding='base64', mime_type=[])
    assert "contents, mime_type and encoding should all be strings" in str(error.value)


def test_create_url_from_parts_accepts_bytes():
    bytearray_data = DataURLFile.create(bytearray(b'abc'), encoding='base64', mime_type='image/png')
    assert bytearray_data.contents == 'YWJj'
    assert bytearray_data.encoding == 'base64'
    assert bytearray_data.mime_type == 'image/png'
    bytes_data = DataURLFile.create(b'abc', encoding='base64', mime_type='image/png')
    assert bytes_data.contents == 'YWJj'
    assert bytes_data.encoding == 'base64'
    assert bytes_data.mime_type == 'image/png'
