import re

from prestans3.types import _Property, ImmutableType, Structure


class ValidationExceptionSummary(tuple):
    """
    Returned when iterating through a |ValidationTree|. Each ValidationExceptionSummary is a
    (``str``, |ValidationException|)
    """

    # noinspection PyInitNewSignature
    def __new__(cls, fqn, messages):
        """
        :param str property_name: the name of the root class of this exception
        :param str attribute_name: The attribute of the |type| of which this exception refers to
        :param |ValidationException| validation_exception: The exception detailing the leaf property and it's validation message
        """
        return tuple.__new__(cls, (fqn, messages))

    @classmethod
    def get_summary_with_new_qualified_name(cls, class_name, attribute_name, summary):
        _replace_regex = r'^[^.]*'
        return ValidationExceptionSummary(
            re.sub(_replace_regex, "{}.{}".format(class_name, attribute_name), summary[0]), summary[1])

    def __str__(self):
        """
        The end user friendly formatted message for this leaf exception

        for example:

        .. code-block:: python

            "MyClass.sub_attr.some_string was invalid: SubAttrClass.some_string min length is 10, len('foobar') was 6"

        :rtype: str
        """
        return "{} was invalid: {}".format(self[0], '["{}"]'.format('", "'.join(self[1])))


class ValidationException(Exception):
    """
    leaf of the validation tree. represents a validation failure of a scalar type
    """

    def __init__(self, of_type, message_or_key_exception_tuple=None):
        """
        :param of_type
        :type message_or_key_exception_tuple: str or (str, T <= |ValidationException|)
        :param of_type: |type| this validation message applies to.
        :type of_type: T <= |ImmutableType|\ .1
        :param str message_or_key_exception_tuple: validation message, user friendly.
        """
        if not issubclass(of_type, ImmutableType):
            raise TypeError('validation exceptions are only valid for subclasses of {}'.format(ImmutableType.__name__))
        self._of_type = of_type
        super(ValidationException, self).__init__([])
        if message_or_key_exception_tuple is None:
            message = self._default_message()
            self.add_own_validation_message(message)
        self.validation_exceptions = {}
        if isinstance(message_or_key_exception_tuple, tuple):
            self.add_validation_exception(message_or_key_exception_tuple[0],
                                          message_or_key_exception_tuple[1])  # when message_or... is tuple
        elif isinstance(message_or_key_exception_tuple, str):
            self.add_own_validation_message(message_or_key_exception_tuple)

    def add_validation_exception(self, key, validation_exception):
        """
        :param str key: the attribute name whose validation failed. This name must be a configured attribute property of
                    this tree's ``self._of_type``
        :param validation_exception: the validation_exception to add to this |ValidationException|\ 's list of exceptions
        :type validation_exception: |ValidationException|
        """
        if not isinstance(validation_exception, ValidationException):
            raise TypeError("Expected validation_exception to be subclass of {} but received instance of {}" \
                            .format(ValidationException.__name__, validation_exception.__class__.__name__))
        if not issubclass(self._of_type, Structure):
            raise TypeError("only subclasses of {} may have child attributes".format(Structure.__name__))
        if key not in self._of_type.__dict__ or not isinstance(self._of_type.__dict__[key], _Property):
            # see if the type of this validation error contains this configured key as a prestans attribute
            raise AttributeError(
                '{} is not a configured prestans attribute of {} class, when trying to set validation exception'.format(
                    key, self._of_type.__name__))
        elif self._of_type.__dict__[key].property_type is not validation_exception._of_type:
            # determine if the property_type of the class's configured prestans attribute equals the type of the
            # exception provided
            raise TypeError(('validation exception for {qProp} was of type {actual_type}, ' +
                             'however {qProp} is a {expected_type} Property').format(
                qProp="{}.{}".format(self._of_type.__name__, key),
                expected_type=self._of_type.__dict__[key].property_type.__name__,
                actual_type=validation_exception._of_type.__name__
            ))
        self.validation_exceptions.update({key: validation_exception})

    def head(self):
        if self.validation_exceptions:
            return list(self.__iter__())[0]
        else:
            return None

    def __getitem__(self, item):
        return list(self.__iter__())[item]

    def __iter__(self):
        """
        iterates through the exceptions and produces a list of |ValidationExceptionSummaries|\ .

        :yields: the next summarised exception (|ValidationExceptionSummaries|)
        :rtype: list[|ValidationExceptionSummary|]
        """
        for key, validation_exception in list(self.validation_exceptions.items()):  # type: (str, ValidationException)
            for summary in list(validation_exception):
                yield ValidationExceptionSummary.get_summary_with_new_qualified_name(self.property_type.__name__, key,
                                                                                     summary)
        if self.messages:
            yield ValidationExceptionSummary(self.property_type.__name__, self.messages)
        else:
            return

    def _default_message(self):
        return "validation error for type {}".format(self.property_type.__name__)

    def add_own_validation_message(self, message):
        self.args[0].append(message)

    @property
    def messages(self):
        return self.args[0]

    @property
    def property_type(self):
        return self._of_type
