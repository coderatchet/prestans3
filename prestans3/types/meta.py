# -*- coding: utf-8 -*-
"""
    prestans.types.meta
    ~~~~~~~~~~~~~~~~~~~

    A WSGI compliant REST micro-framework.

    :copyright: (c) 2016 Anomaly Software
    :license: Apache 2.0, see LICENSE for more details.
"""


class _PropertyRulesProperty(object):
    """ property descriptor for class-local, base-class-proxied property rule storage """

    # noinspection PyUnusedLocal
    def __get__(self, cls, _mcs):
        return _mcs._property_rule_graph[cls]


class _ConfigChecksProperty(object):
    """ property descriptor for class-local, base-class-proxied config check storage """

    # noinspection PyUnusedLocal
    def __get__(self, cls, _mcs):
        return _mcs._config_check_graph[cls]


class _PrepareFunctionsProperty(object):
    """ property descriptor for class-local, base-class-proxied prepare function storage """

    # noinspection PyUnusedLocal
    def __get__(self, cls, _mcs):
        return _mcs._prepare_functions_graph[cls]


class PrestansTypeMeta(type):
    """
    Each |type| has this class as its metaclass. when the following attributes are access on the class object,
    the returning object is an editble dictionary with a proxied reference to its base class's value for this call.
    changes in the

    see |MergingProxyDictionary|
    """

    property_rules = _PropertyRulesProperty()  # type: dict[str, (T <= ImmutableType, any) -> None]
    """ getter for |type|\ 's property rule registry'"""

    config_checks = _ConfigChecksProperty()  # type: dict[str, (type, any) -> None]
    """ getter for |type|\ 's config check registry'"""

    prepare_functions = _PrepareFunctionsProperty()  # type: dict[str, (T <= ImmutableType) -> T]
    """ getter for |type|\ 's prepare functions registry'"""

    _prepare_functions_graph = None
    _config_check_graph = None
    _property_rule_graph = None
