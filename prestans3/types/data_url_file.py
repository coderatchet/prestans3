# -*- coding: utf-8 -*-
"""
    prestans.types.string
    ~~~~~~~~~~~~~~~~~~~~~
    
    A WSGI compliant REST micro-framework.

    :copyright: (c) 2016 Anomaly Software
    :license: Apache 2.0, see LICENSE for more details.
"""
import codecs

import prestans3
from prestans3.errors import ValidationException
from prestans3.future import istext, isbytes
from . import ImmutableType
import re


class DataURLFile(ImmutableType):
    """
    Implements a `Data URI string`_\ . The |DataURLFile| embeds a mime type, encoding and content into a string and is
    supported by HTML, CSS and Javascript for embedded content (e.g. a `png`_).

    .. _Data URI string: http://en.wikipedia.org/wiki/Data_URI_scheme
    .. _png: https://en.wikipedia.org/wiki/Data_URI_scheme#HTML
    """

    regex = re.compile(r'^data:([\w/\-.]+);(\w+),(.*)$')

    @property
    def native_value(self):
        return self.to_native_value(self.contents, self.encoding, self.mime_type)

    @classmethod
    def generate_filename(cls):
        import uuid
        return uuid.uuid4().hex

    @classmethod
    def from_value(cls, value):
        try:
            return super(DataURLFile, cls).from_value(value)
        except NotImplementedError:
            # py2to3 replace istext(value) with isinstance(value, str)
            if not istext(value):
                raise TypeError("{} of type {} is not coercible to type {}".format(value, value.__class__.__name__,
                                                                                   cls.__name__))
            else:
                return DataURLFile(value)

    @classmethod
    def create(cls, contents, mime_type, encoding='base64'):
        """
        create a |DataURLFile| instance from raw contents

        :param contents: the raw contents to encode
        :type contents: str or bytes or bytearray
        :param str mime_type: mime type of encoding
        :param str encoding: codec for encoding
        :rType: DataURLFile
        """

        # py2to3 replace `istext(contents) or isbytes(contents) or isinstance(contents, bytearray)`
        # with `isinstance(contents, (str, bytes, bytearray))`
        if not istext(contents) or not istext(mime_type) or not istext(encoding):
            raise TypeError("contents, mime_type and encoding should all be strings")
        else:
            return DataURLFile(DataURLFile.to_native_value(contents, encoding, mime_type))

    @classmethod
    def to_native_value(cls, contents, encoding, mime_type):
        return "data:{mime_type};{encoding},{contents}".format(mime_type=mime_type, encoding=encoding,
                                                               contents=contents)

    def __init__(self, encoded_data):
        self._encoded_data = encoded_data
        match = self.regex.match(encoded_data)
        if match:
            [a, b, c] = match.groups()
            self._mime_type = a
            self._encoding = b
            self._contents = c
        else:
            raise ValueError("encoded_data was not in the expected format. for an explaination of how to format a "
                             "data url file, see https://en.wikipedia.org/wiki/Data_URI_scheme")
        super(DataURLFile, self).__init__()

    @property
    def mime_type(self):
        """
        IANA compliant media type for this content. See https://en.wikipedia.org/wiki/Media_type for more details
        """
        return self._mime_type

    @property
    def encoding(self):
        """ encoding of the text (separate from the encoding of the page). e.g. base64 """
        return self._encoding

    @property
    def contents(self):
        """ the encoded contents of this media type """
        return self._contents

    @property
    def decoded_contents(self):
        """ attempts to decode the contents according to the configured encoding """
        # py2to3 remove else statement and PY3 check
        if prestans3.future.PY3:
            contents_ = bytes(self.contents, encoding='utf-8')
        else:
            contents_ = self.contents
        return codecs.lookup(self.encoding).decode(contents_)[0]

    def __eq__(self, other):
        if isinstance(other, DataURLFile):
            return (
                self.mime_type == other.mime_type and
                self.contents == other.contents and
                self.encoding == other.encoding
            )
        # py2to3 replace with isinstance(other, str)
        elif istext(other):
            return self == DataURLFile.from_value(other)
        else:
            return False

    def __ne__(self, other):
        return not self == other


def _allowed_mime_types(instance, config):
    """
    checks whether the |DataURLFile|\ 's mime_type is in the configured list of strings

    :type instance: |DataURLFile|
    :param list[str] config: list of allowed mime types
    :raises ValidationException: if instsance.mime_type isn't in the config
    """
    if instance.mime_type not in config:
        raise ValidationException(instance.__class__,
                                  "{} is an invalid mime type, valid types are [{}]".format(instance.mime_type,
                                                                                            ", ".join(config)))


DataURLFile.register_property_rule(_allowed_mime_types, name="allowed_mime_types")
