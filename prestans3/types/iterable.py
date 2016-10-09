# -*- coding: utf-8 -*-
"""
    prestans.types.iterable
    ~~~~~~~~~~~~~~~~~~~~~~~

    A WSGI compliant REST micro-framework.

    :copyright: (c) 2016 Anomaly Software
    :license: Apache 2.0, see LICENSE for more details.
"""
from prestans3.types import Container


# noinspection PyAbstractClass
class Iterable(Container):
    # todo construct entire object in __init__
    # todo __setitem__ raises error
    pass


# noinspection PyAbstractClass
class _MutableIterable(Iterable):
    # todo __setitem__ should not raise error.
    pass
