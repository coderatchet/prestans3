# -*- coding: utf-8 -*-
"""
    prestans.types.string
    ~~~~~~~~~~~~~~~~~~~~~
    
    A WSGI compliant REST micro-framework.

    :copyright: (c) 2016 Anomaly Software
    :license: Apache 2.0, see LICENSE for more details.
"""

from . import ImmutableType


class DataURLFile(ImmutableType):
    """
    Implements a `Data URI string`_\ . The |DataURLFile| embeds a mime type, encoding and content into a string and is
    supported by HTML, CSS and Javascript for embedded content (e.g. a `png`_).

    .. _Data URI string: http://en.wikipedia.org/wiki/Data_URI_scheme
    .. _png: https://en.wikipedia.org/wiki/Data_URI_scheme#HTML
    """

    @classmethod
    def generate_filename(cls):
        import uuid
        return uuid.uuid4().hex

    def __init__(self, encoded_data, *args):
        self._as_encoded = encoded_data
        super(DataURLFile, self).__init__()

