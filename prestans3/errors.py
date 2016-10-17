# -*- coding: utf-8 -*-
"""
    prestans3.errors
    ~~~~~~~~~~~~~~~~

    A WSGI compliant REST micro-framework.

    :copyright: (c) 2016 Anomaly Software
    :license: Apache 2.0, see LICENSE for more details.
"""
import re


class ValidationExceptionSummary(tuple):
    """
    Returned when iterating through a |ValidationException|. Each ValidationExceptionSummary is a
    (``str``, |list[str]|) which represents a fully qualified name and its list of exception messages
    """

    # noinspection PyInitNewSignature
    def __new__(cls, fqn, messages):
        """
        :param str fqn: the fully qualified name of the class or property with an exception
        :param messages: The exception detailing the leaf property and it's validation message
        :type messages: list[str]
        """
        return tuple.__new__(cls, (fqn, messages))

    def __str__(self):
        """
        The end user friendly formatted message for this leaf exception

        for example:

        .. code-block:: python

            "MyClass.sub_attr.some_string was invalid: SubAttrClass.some_string min length is 10, len('foobar') was 6"

        :rtype: str
        """
        return "{} is invalid: {}".format(self[0], '["{}"]'.format('", "'.join([str(item) for item in self[1]])))


class ValidationException(Exception):
    """
    leaf of the validation tree. represents a validation failure of a scalar type
    """

    def __init__(self, of_type, message=None):
        """
        :param of_type: |type| this validation message applies to.
        :type of_type: class<T <= |ImmutableType|\ >
        :param str message: validation message, user friendly.
        """
        from prestans3.types import ImmutableType
        if not issubclass(of_type, ImmutableType):
            raise TypeError('validation exceptions are only valid for subclasses of {}'.format(ImmutableType.__name__))
        self._of_type = of_type
        super(ValidationException, self).__init__([])
        if message is not None:
            self.add_validation_message(message)

    @property
    def head(self):
        """
        :return: the head of the list of summaries
                 see :func:`~prestans3.errors.ValidationException.__iter__`
        """
        return list(self.__iter__())[0]

    def __getitem__(self, item):
        return list(self.__iter__())[item]

    def __iter__(self):
        """
        iterates through the exceptions and produces a list of |ValidationExceptionSummaries|\ .

        :yields: the next summarised exception (|ValidationExceptionSummaries|)
        """
        if self.messages:
            yield ValidationExceptionSummary(self.property_type.__name__, self.messages)
        else:
            return

    def _default_message(self):
        return "validation error for type {}".format(self.property_type.__name__)

    def add_validation_message(self, message):
        """ adds a validation message regarding this current |type| (not one of its |attributes|\ ) """
        self.args[0].append(message)

    def add_validation_messages(self, iterable):
        """ adds a list of messages regarding this current |type| (not one of its |attributes|\ ) """
        for item in iterable:
            self.add_validation_message(item)

    def __str__(self):
        return "[ ({}) ]".format("), (".join([str(summary) for summary in self]))

    @property
    def messages(self):
        return self.args[0]

    @property
    def property_type(self):
        return self._of_type


class InvalidMethodUseError(Exception):
    def __init__(self, method, message=None):
        self._method = method
        if message is None:
            message = ""
        super(InvalidMethodUseError, self).__init__(message)


class AccessError(Exception):
    def __init__(self, cls, message=None):
        if message is None:
            message = "invalid access on class: {}".format(cls.__name__)
        super(AccessError, self).__init__(message)


class PropertyConfigError(Exception):
    def __init__(self, cls, property_rule_name, message=None):
        if message is None:
            message = "error whilst configuring the property rule name {} on class {}".format(
                property_rule_name, cls.__name__)
        super(PropertyConfigError, self).__init__(message)


class ContainerValidationExceptionSummary(ValidationExceptionSummary):
    # noinspection PyInitNewSignature
    def __new__(cls, class_name, attribute_name, summary):
        """
        adjusts the key of the provided summary and returns a newly created exception with the properly referenced
        |attribute|\ :

        >>> from prestans3.errors import ValidationExceptionSummary
        >>> summary1 = ValidationExceptionSummary('MyClass.some_string', ['String was invalid'])
        >>> super_summary = ValidationExceptionSummary.get_summary_with_new_qualified_name('MySuperModel.my_sub_class' \
        ...     , summary1)
        >>> assert super_summary[0] == "MySuperModel == ['String was invalid']"

        :param str class_name: the |type|\ 's class that owns the sub |attribute|
        :param str attribute_name: the name of the configured |attribute| on the owning |type|
        :param |ContainerValidationExceptionSummary| summary: a modified validation summary to qualified with the name
               of the attribute with the parent class
        """
        _replace_regex = r'^[^.]*'
        return super(ContainerValidationExceptionSummary, cls).__new__(cls,
                                                                       re.sub(_replace_regex, "{}.{}".format(class_name,
                                                                                                             attribute_name),
                                                                              summary[0]),
                                                                       summary[1])