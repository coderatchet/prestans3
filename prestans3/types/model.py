# -*- coding: utf-8 -*-
"""
    prestans.types.model
    ~~~~~~~~~~~~~~~~~~~~

    A WSGI compliant REST micro-framework.

    :copyright: (c) 2016 Anomaly Software
    :license: Apache 2.0, see LICENSE for more details.
"""

import re

from prestans3.errors import ValidationException, ValidationExceptionSummary
from prestans3.types import Container, _Property
from prestans3.utils import is_str
from copy import copy


class AttributeValidationExceptionSummary(ValidationExceptionSummary):
    # noinspection PyInitNewSignature
    def __new__(cls, class_name, attribute_name, summary):
        """
        adjusts the key of the provided summary and returns a newly created exception with the properly referenced
        |attribute|\ :

        >>> from prestans3.errors import ValidationExceptionSummary
        >>> summary1 = ValidationExceptionSummary('MyClass.some_string', ['String was invalid'])
        >>> super_summary = ValidationExceptionSummary.get_summary_with_new_qualified_name('MySuperModel.my_sub_class', summary1)
        >>> assert super_summary[0] == "MySuperModel == ['String was invalid']"

        :param str class_name: the |type|\ 's class that owns the sub |attribute|
        :param str attribute_name: the name of the configured |attribute| on the owning |type|
        :param |AttributeValidationExceptionSummary| summary: a modified validation summary to qualified with the name
               of the attribute with the parent class
        """
        _replace_regex = r'^[^.]*'
        return super(AttributeValidationExceptionSummary, cls).__new__(cls,
                                                                       re.sub(_replace_regex, "{}.{}".format(class_name,
                                                                                                             attribute_name),
                                                                              summary[0]),
                                                                       summary[1])


class ModelValidationException(ValidationException):
    def __init__(self, of_type, message_or_key_exception_tuple=None):
        """
        :param of_type: |type| in error.
        :type of_type: T <= |Model|
        :param message_or_key_exception_tuple:
        :type message_or_key_exception_tuple: str or (str, ValidationException)
        """
        self.validation_exceptions = {}
        if isinstance(message_or_key_exception_tuple, tuple):
            super(ModelValidationException, self).__init__(of_type)
            self.add_validation_exception(message_or_key_exception_tuple[0],
                                          message_or_key_exception_tuple[1])  # when message_or... is tuple
        elif is_str(message_or_key_exception_tuple):
            super(ModelValidationException, self).__init__(of_type, message_or_key_exception_tuple)
        else:
            super(ModelValidationException, self).__init__(of_type)

    def __iter__(self):
        """ iterate through the summaries for this exception """
        for summary in list(super(ModelValidationException, self).__iter__()):
            yield summary
        for key, validation_exception in list(self.validation_exceptions.items()):  # type: (str, ValidationException)
            for summary in list(validation_exception):
                yield AttributeValidationExceptionSummary(self.property_type.__name__, key, summary)

    def add_validation_exception(self, key, validation_exception):
        """
        :param str key: the attribute name whose validation failed. This name must be a configured attribute property of
                    this tree's ``self._of_type``
        :param |ValidationException| validation_exception: the validation_exception to add to this |ValidationException|\ 's list of exceptions
        """
        if not isinstance(validation_exception, ValidationException):
            raise TypeError("Expected validation_exception to be subclass of {} but received instance of {}" \
                            .format(ValidationException.__name__, validation_exception.__class__.__name__))
        if not issubclass(self._of_type, Model):
            raise TypeError("only subclasses of {} may have child attributes".format(Model.__name__))
        if not self._of_type.is_prestans_attribute(key):
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


# noinspection PyAbstractClass
class Model(Container):
    """
    Base class of complex |types|. may contain other |Models| and/or |Scalars|.
    """

    def __setattr__(self, key, value):

        """
        This is an immutable type, You should not set values directly through here, set them through the main init
        method.

        i.e. We'll fire you if you override this method. `see_stackoverflow`_

        .. _see_stackoverflow: http://stackoverflow.com/a/2425818/735284
        """
        if self.is_prestans_attribute(key):
            raise ("attempted to set value of prestans3 attribute on an immutable Model, "
                   "For a mutable {class_name}, call {class_name}.mutable(...)".format(
                class_name=self.__class__.__name__))
        else:
            super(Model, self).__setattr__(key, value)

    def validate(self, validation_exception=None):
        for key, attribute in self.prestans_attributes:
            try:
                attribute.validate()
            except ValidationException as error:
                if validation_exception is None:
                    validation_exception = ModelValidationException(self.__class__)
                else:
                    validation_exception.add_validation_exception(key, error)
        super(Model, self).validate(validation_exception)

    @classmethod
    def is_prestans_attribute(cls, key):
        """
        Determines if the key provides is a configured |attribute| of this |Model|\ .

        :param str key: name of the attribute
        :return bool: ``True`` if this is a |attribute| or False if otherwise.
        """
        if key in cls.__dict__ and isinstance(cls.__dict__[key], _Property):
            return True
        else:
            return False

    def __getattribute__(self, item):
        """
        will use the |_Property|\ 's __get__ method if the item is a |attribute| otherwise retrieves the regular
        python attribute as normal
        """
        if object.__getattribute__(self, 'is_prestans_attribute')(item):
            return object.__getattribute__(self, '__class__').__dict__[item].__get__(
                object.__getattribute__(self, '_prestans_attributes')[item],
                object.__getattribute__(self, '_prestans_attributes')[item].__class__)
        else:
            return object.__getattribute__(self, item)

    def __init__(self, **kwargs):
        super(Model, self).__init__(**kwargs)
        self._prestans_attributes = {}

    @property
    def prestans_attributes(self):
        """
        returns a dictionary of prestan attribute names to their values

        :rtype: dict[str -> |ImmutableType|\ ]
        """
        return self._prestans_attributes

    @classmethod
    def mutable(cls, **kwargs):
        if cls is Model:
            raise TypeError("mutable called on base Model class. must call mutable on a concrete subclass of Model")
        else:
            # noinspection PyAbstractClass
            _bases = copy(cls.__class__.__bases__)
            index_of_model = _bases.index(Model)
            _bases.insert(index_of_model, _MutableModel)
            __PrivateMutableModel = type(_MutableModel, bases=_bases, dict=copy(cls.__class__.__dict__))
            return __PrivateMutableModel(validate_immediately=False, **kwargs)

    def mutable_copy(self):
        pass


# noinspection PyAbstractClass
class _MutableModel(Model):
    """
    Not instantiated directly, instead call the :func:`.Container.mutable()` method to retrieve an instance of this
    |type| that may be mutated. Validation will now not happen on __init__
    """

    def __setattr__(self, key, value):
        """
        |types| maintain an internal dictionary of attribute names to their values for easy demarcation between prestans
        attributes and native python object attributes. This enables the user to set arbitrary values on the object
        without affecting the final serialization of the object. In other words: regular python properties on an object
        are transient to the client requesting the object.

        :param str key: the name of the attribute or regular python property to set on the object.
        :param value: the value to set on this |MutableModel|. if the key refers a prestans attribute,
                                             it is stored in the internal :attr:`.Model._prestans_attributes` store.
                                             otherwise it is stored in the :attr:`.Model.__dict__` as normal.
        :type value: |ImmutableType| or any
        """
        # if the key being set is a |attribute| then store the value in the self._prestans_attributes dictionary
        if self.is_prestans_attribute(key):
            object.__getattribute__(self, '__class__').__dict__[key].__set__(
                object.__getattribute__(self, '_prestans_attributes'),
                (key, value)
            )
        # else default super behaviour
        else:
            super(_MutableModel, self).__setattr__(key, value)
        pass
