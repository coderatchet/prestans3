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


class ContainerValidationException(ValidationException):
    def __init__(self, of_type, message_or_key_exception_tuple=None):
        """
        :param of_type: |type| in error.
        :type of_type: T <= |Model|
        :param message_or_key_exception_tuple:
        :type message_or_key_exception_tuple: str or (str, ValidationException)
        """
        from prestans3.utils import is_str
        self.validation_exceptions = {}
        if isinstance(message_or_key_exception_tuple, tuple):
            super(ContainerValidationException, self).__init__(of_type)
            self.add_validation_exception(message_or_key_exception_tuple[0],
                                          message_or_key_exception_tuple[1])  # when message_or... is tuple
        elif is_str(message_or_key_exception_tuple):
            super(ContainerValidationException, self).__init__(of_type, message_or_key_exception_tuple)
        else:
            super(ContainerValidationException, self).__init__(of_type)

    def __iter__(self):
        """ iterate through the summaries for this exception """
        for summary in list(super(ContainerValidationException, self).__iter__()):
            yield summary
        for key, validation_exception in list(self.validation_exceptions.items()):  # type: (str, ValidationException)
            for summary in list(validation_exception):
                yield ContainerValidationExceptionSummary(self.property_type.__name__, key, summary)

    def add_validation_exception(self, key, validation_exception):
        """
        :param str key: the attribute name whose validation failed. This name must be a configured attribute property of
                    this tree's ``self._of_type``
        :param |ValidationException| validation_exception: the validation_exception to add to this |ValidationException|\ 's list of exceptions
        """
        self.check_validation_exception(key, validation_exception)
        self.validation_exceptions.update({key: validation_exception})

    def check_validation_exception(self, key, validation_exception):
        from prestans3.types import Container
        if not isinstance(validation_exception, ValidationException):
            raise TypeError("Expected validation_exception to be subclass of {} but received instance of {}"
                            .format(ValidationException.__name__, validation_exception.__class__.__name__))
        if not issubclass(self._of_type, Container):
            raise TypeError("only subclasses of {} may have dependants".format(Container.__name__))


class ContainerValidationExceptionSummary(ValidationExceptionSummary):
    # noinspection PyInitNewSignature
    def __new__(cls, class_name, attribute_name, summary):
        """
        adjusts the key of the provided summary and returns a newly created exception with the properly referenced
        |attribute|\ or array element:

        >>> from prestans3.errors import ValidationExceptionSummary, ContainerValidationExceptionSummary
        >>> summary1 = ValidationExceptionSummary('MyClass.some_string', ['String was invalid'])
        >>> super_summary = ContainerValidationExceptionSummary('MySuperModel', 'my_sub_attr', summary1)
        >>> assert "MySuperModel.my_sub_attr.some_string" in str(super_summary)
        >>> assert "String was invalid" in str(super_summary)

        :param str class_name: the |type|\ 's class that owns the sub |attribute|
        :param str attribute_name: the name of the configured |attribute| on the owning |type|
        :param |ValidationExceptionSummary| summary: the summary of one of this containers validation exceptions
        """
        _replace_regex = r'^[^.]*'
        return super(ContainerValidationExceptionSummary, cls).__new__(cls,
                                                                       re.sub(_replace_regex, "{}.{}".format(class_name,
                                                                                                             attribute_name),
                                                                              summary[0]),
                                                                       summary[1])
