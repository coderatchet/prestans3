class _PropertyRulesProperty(object):
    # noinspection PyUnusedLocal
    def __get__(self, cls, _mcs):
        return _mcs._property_rule_graph[cls]


class _ConfigChecksProperty(object):
    # noinspection PyUnusedLocal
    def __get__(self, cls, _mcs):
        return _mcs._config_check_graph[cls]


class _PrepareFunctionsProperty(object):
    # noinspection PyUnusedLocal
    def __get__(self, cls, _mcs):
        return _mcs._prepare_functions_graph[cls]


class _PrestansTypeMeta(type):
    property_rules = _PropertyRulesProperty()  # type: dict[str, (T <= ImmutableType, any) -> None]
    config_checks = _ConfigChecksProperty()  # type: dict[str, (type, any) -> None]
    prepare_functions = _PrepareFunctionsProperty()  # type: dict[str, (T <= ImmutableType) -> T]
    _prepare_functions_graph = None
    _config_check_graph = None
    _property_rule_graph = None
