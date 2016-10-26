# -*- coding: utf-8 -*-
"""
    prestans.types.string
    ~~~~~~~~~~~~~~~~~~~~~
    
    A WSGI compliant REST micro-framework.

    :copyright: (c) 2016 Anomaly Software
    :license: Apache 2.0, see LICENSE for more details.
"""
import codecs

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
    def create(cls, contents, mime_type, encoding=None):
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
        if not (istext(contents) or isbytes(contents) or isinstance(contents, bytearray)) or not istext(
                mime_type) or not istext(encoding):
            raise TypeError("contents, mime_type and encoding should all be strings")
        else:
            codec = codecs.lookup(encoding)
            encoded = codec.encode(contents)[0]
            if codec.name == 'base64':
                encoded = re.sub('\n$', '', encoded)
            return DataURLFile("data:{};{},{}".format(mime_type, encoding, encoded))

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
        return self._mime_type

    @property
    def encoding(self):
        return self._encoding

    @property
    def contents(self):
        return self._contents

    @property
    def decoded_contents(self):
        return codecs.lookup(self.encoding).decode(self.contents)[0]

    def __eq__(self, other):
        if isinstance(other, DataURLFile):
            return (
                self.mime_type == other.mime_type and
                self.contents == other.contents and
                self.encoding == other.encoding
            )
        else:
            return False

    def __ne__(self, other):
        return not self == other
