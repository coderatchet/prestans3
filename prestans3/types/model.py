# -*- coding: utf-8 -*-
"""
    prestans.types.model
    ~~~~~~~~~~~~~~~~~~~~

    A WSGI compliant REST micro-framework.

    :copyright: (c) 2016 Anomaly Software
    :license: Apache 2.0, see LICENSE for more details.
"""
from copy import copy

from prestans3.errors import ValidationException, AccessError, ContainerValidationException
from prestans3.types import Container, _Property
from prestans3.utils import inject_class, with_metaclass, ImmutableMergingDictionary, LazyOneWayGraph, \
    _PrestansTypeMeta


class ModelValidationException(ContainerValidationException):
    def check_validation_exception(self, key, validation_exception):
        super(ModelValidationException, self).check_validation_exception(key, validation_exception)
        if not self._of_type.is_prestans_attribute(key):
            # see if the type of this validation error contains this configured key as a prestans attribute
            raise AttributeError(
                '{} is not a configured prestans attribute of {} class, when trying to set validation exception'.format(
                    key, self._of_type.__name__))
        elif self._of_type.get_prestans_attribute_property(key).property_type is not validation_exception._of_type:
            # determine if the property_type of the class's configured prestans attribute equals the type of the
            # exception provided
            raise TypeError(('validation exception for {qProp} was of type {actual_type}, ' +
                             'however {qProp} is a {expected_type} Property').format(
                qProp="{}.{}".format(self._of_type.__name__, key),
                expected_type=self._of_type.__dict__[key].property_type.__name__,
                actual_type=validation_exception._of_type.__name__
            ))


class _PrestansAttributesProperties(object):
    def __init__(self, of_type):
        self._of_type = of_type

    def __get__(self, instance, owner):
        return _prestans_attribute_properties[self._of_type]


class _PrestansModelTypeMeta(_PrestansTypeMeta):
    def __init__(cls, what, bases, attrs, **kwargs):
        cls.prestans_attribute_properties = _PrestansAttributesProperties(cls)
        for attr_name, attr in list(attrs.items()):
            if isinstance(attr, _Property):
                cls.prestans_attribute_properties[attr_name] = attr
        super(_PrestansModelTypeMeta, cls).__init__(what, bases, attrs)


# noinspection PyAbstractClass
class Model(with_metaclass(_PrestansModelTypeMeta, Container)):
    """
    Base class of complex |types|. may contain other |Models| and/or |ImmutableTypes|\ . Initial values may be provided
    in the form of a dict[str -> value] for the prestans attributes, these values will take precedence over those
    provided by a |_Property|\ 's `default` argument.
    """

    def __init__(self, initial_values=None, **kwargs):
        """

        :param dict[str, value] initial_values:
        :param kwargs:
        """
        self._prestans_attributes = {}
        if initial_values is not None:
            for key, value in list(initial_values.items()):
                if self.is_prestans_attribute(key):
                    self.get_prestans_attribute_property(key).__set__(
                        self._prestans_attributes,
                        (key, value)
                    )
                else:
                    raise ValueError("Model.__init__ called with an invalid initial_values parameter: "
                                     "{} is not a configured prestans attribute of {}".format(key,
                                                                                              self.__class__.__name__))

        # for all the prestans attributes in this class, if they don't yet have a value, then set it
        for key, p_attr in list(self.__class__.prestans_attribute_properties.items()):
            if p_attr.default is not None and (
                            key not in self.prestans_attributes or self.prestans_attributes[key] is None):
                p_attr.__set__(self._prestans_attributes, (key, copy(p_attr.default)))

        super(Model, self).__init__(**kwargs)

    def __setattr__(self, key, value):

        """
        This is an immutable type, You should not set values directly through here, set them through the main init
        method.

        i.e. We'll fire you if you override this method. `see_stackoverflow`_

        .. _see_stackoverflow: http://stackoverflow.com/a/2425818/735284
        """
        if self.is_prestans_attribute(key):
            raise AccessError(self.__class__, "attempted to set value of prestans3 attribute on an immutable Model, "
                                              "For a mutable {class_name}, call {class_name}.mutable(...)".format(
                class_name=self.__class__.__name__))
        else:
            super(Model, self).__setattr__(key, value)

    def __delattr__(self, item):
        if self.is_prestans_attribute(item):
            raise AccessError(self.__class__, "attempted to delete value of prestans3 attribute on an immutable Model, "
                                              "For a mutable {class_name}, call {class_name}.mutable(...)".format(
                class_name=self.__class__.__name__))
        else:
            super(Model, self).__delattr__(item)

    def validate(self, config=None, **kwargs):
        validation_exception = None
        for p_attr_name, p_attr in list(self.prestans_attribute_properties.items()):
            try:
                attr = self.prestans_attributes[p_attr_name]  # T <= ImmutableType
                attr.validate(p_attr.rules_config)
            except KeyError:
                pass
            except ValidationException as error:
                if validation_exception is None:
                    validation_exception = ModelValidationException(self.__class__)
                validation_exception.add_validation_exception(p_attr_name, error)
        try:
            default_rules_config = self.__class__.default_rules_config()
            if config is None:
                super(Model, self).validate(default_rules_config)
            else:
                super(Model, self).validate(ImmutableMergingDictionary(config, default_rules_config))
        except ValidationException as error:
            if validation_exception is None:
                validation_exception = ModelValidationException(self.__class__)
            validation_exception.add_validation_messages(error.messages)
        if validation_exception:
            raise validation_exception

    @classmethod
    def is_prestans_attribute(cls, key):
        """
        Determines if the key provides is a configured |attribute| of this |Model|\ .

        :param str key: name of the attribute
        :return bool: ``True`` if this is a |attribute| or False if otherwise.
        """
        if key in cls.prestans_attribute_properties:
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

    @property
    def prestans_attributes(self):
        """
        returns a dictionary of prestan attribute names to their values

        :rtype: dict[str -> |ImmutableType|\ ]
        """
        return ImmutableMergingDictionary(self._prestans_attributes)

    @classmethod
    def mutable(cls, *args, **kwargs):

        _Mutable = cls.mutable_class()
        return _Mutable(*args, **kwargs)

    @classmethod
    def mutable_class(cls):
        if cls is Model:
            raise TypeError("mutable called on base Model class. must call mutable on a concrete subclass of Model")
        new_mutable_model_subclass = inject_class(cls, _MutableModel, Model,
                                                  new_type_name_func=lambda x, _y, _z: "PMutable{}".format(
                                                      x.__name__))
        return new_mutable_model_subclass

    def mutable_copy(self):
        mutable = self.__class__.mutable()
        for key, p_attr in list(self.prestans_attributes.items()):
            mutable.__setattr__(key, copy(self.prestans_attributes[key]))
        return mutable

    @classmethod
    def get_prestans_attribute_property(cls, attr_name):
        p_attrs = cls.prestans_attribute_properties
        if attr_name in cls.__dict__ and attr_name not in p_attrs:
            raise AttributeError(
                "'{}' is a normal python class attribute, not a {} instance".format(attr_name, _Property.__name__))
        else:
            return p_attrs[attr_name]


_prestans_attribute_properties = LazyOneWayGraph(Model)


def check_required_attributes(instance, config=True):
    """ iterates through all prestans attributes and checks if required attributes are not None """
    if config:
        p_attrs = instance.__class__.prestans_attribute_properties
        validation_exception = None
        for p_attr_name, p_attr in list(p_attrs.items()):
            if p_attr.required:
                try:
                    instance.prestans_attributes[p_attr_name]
                except KeyError:
                    if validation_exception is None:
                        validation_exception = ValidationException(instance.__class__)
                    validation_exception.add_validation_message(
                        "required prestans attribute '{}' does not exist on this instance of {}".format(
                            p_attr_name, instance.__class__.__name__)
                    )
        if validation_exception:
            raise validation_exception


Model.register_property_rule(check_required_attributes, name="check_required_attributes", configurable=False,
                             default=True)


# noinspection PyAbstractClass
class _MutableModel(with_metaclass(_PrestansModelTypeMeta, Model)):
    """
    Not instantiated directly, instead call the :func:`.Container.mutable()` method to retrieve an instance of this
    |type| that may be mutated. Validation will now not happen on __init__
    """

    def __init__(self, initial_values=None, **kwargs):
        kwargs.update(validate_immediately=False)
        super(_MutableModel, self).__init__(initial_values, **kwargs)

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
            self.__class__.__dict__[key].__set__(self._prestans_attributes, (key, value))
        # else default super behaviour
        else:
            super(_MutableModel, self).__setattr__(key, value)

    @property
    def prestans_attributes(self):
        return self._prestans_attributes
