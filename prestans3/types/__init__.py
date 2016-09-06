# -*- coding: utf-8 -*-
"""
    prestans.types
    ~~~~~~~~~~~~~~
    
    A WSGI compliant REST micro-framework.

    :copyright: (c) 2016 Anomaly Software
    :license: Apache 2.0, see LICENSE for more details.
"""


class Type(object):

    def __init__(self):        
        self._meta = {}

class Scalar(object):

    def __init__(Type):
        super(Scalar, self).__init__()

class Structure(Type):

    def __init__(Type):
        super(Structure, self).__init__()

class Collection(Type):

    def __init__(Type):
        super(Collection, self).__init__()


from .string import String as String
from .integer import Integer as Integer
from .float import Float as Float
from .boolean import Boolean as Boolean