# -*- coding: utf-8 -*-
"""
    prestans3.utils
    ~~~~~~~~~~~~~~~

    A WSGI compliant REST micro-framework.

    :copyright: (c) 2016 Anomaly Software
    :license: Apache 2.0, see LICENSE for more details.
"""
try:
    # noinspection PyUnresolvedReferences,PyStatementEffect
    basestring
    def is_str(s):
        """python 2.7 safe version"""
        # noinspection PyUnresolvedReferences
        return isinstance(s, basestring)
except NameError:
    def is_str(s):
        """python 3+ safe version"""
        return isinstance(s, str)
