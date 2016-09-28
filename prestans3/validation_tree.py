from prestans3.types import Property, Structure
import re


class ValidationTreeNode(object):
    """
    Abstract Base Class of a Validation Tree Node. Do not instantiate this class directly, instead use a subclass
    (|ValidationTree| or |LeafValidationException|)
    """

    def __init__(self, of_type):
        """
        :param of_type: the class this Validation Tree Node refers to.
        :type of_type: T <= |MutableType|
        """
        self._of_type = of_type

    @property
    def property_type(self):
        return self._of_type


class ValidationTree(ValidationTreeNode):
    """
    A |Structure| validation result, contains a dictionary of attribute names to their
    |ValidationTreeNodes| or |LeafValidationException| for |Structure| and |Scalar| attributes respectively
    """

    def __init__(self, of_type, validation_node):
        """
        :type validation_node: (``str``, ``ValidationTreeNode``)
        :rtype: ``ValidationTree``
        """
        if not issubclass(of_type, Structure):
            raise TypeError('validation trees are only valid for Types with configured prestans attributes')
        super(ValidationTree, self).__init__(of_type)
        key, node = validation_node
        self.validation_exceptions = {}
        self.add_validation_exception(key, node)

    def add_validation_exception(self, key, node):
        """
        :param key: the attribute name whose validation failed. This name must be a configured attribute property of
                    this tree's ``self._of_type``
         :type key: ``str``
        :param node:
        """
        if not isinstance(node, ValidationTreeNode) or ValidationTreeNode == node.__class__:
            raise TypeError
        if key not in self._of_type.__dict__ or not isinstance(self._of_type.__dict__[key], Property):
            raise AttributeError(
                '{} is not a configured prestans attribute of {} class, when trying to set Validation Exception'.format(
                    key, self._of_type.__name__))
        elif self._of_type.__dict__[key].property_type is not node._of_type:
            raise TypeError(('validation exception for {qProp} was of type {actual_type}, ' +
                             'however {qProp} is a {expected_type} Property').format(
                qProp="{}.{}".format(self._of_type.__name__, key),
                expected_type=self._of_type.__dict__[key].property_type.__name__,
                actual_type=node._of_type.__name__
            ))
        self.validation_exceptions.update({key: node})

    def head(self):
        if self.validation_exceptions:
            return list(self.__iter__())[0]
        else:
            return None

    def __getitem__(self, item):
        return list(self.__iter__())[item]

    def __iter__(self):
        """
        iterates through the exceptions and produces a list of |LeafValidationSummaries|\ .

        :yields: the next summarised exception (|LeafValidationSummaries|)
        :rtype: list[|LeafValidationSummary|]
        """
        for key, node in list(self.validation_exceptions.items()):  # type: (str, LeafValidationException)
            if isinstance(node, LeafValidationException):
                yield LeafValidationSummary(self.property_type.__name__, key, node)
            else:
                for sub_summary in node:
                    yield LeafValidationSummary(self.property_type.__name__, key, node, sub_summary)


class LeafValidationSummary(tuple):
    """
    Returned when iterating through a |ValidationTree|. Each LeafValidationSummary is a
    (``str``, |LeafValidationException|)
    """

    def __new__(cls, property_name, attribute_name, leaf_exception, sub_summary=None, direct_child=True):
        """
        :param str property_name: the name of the root class of this exception
        :param str attribute_name: The attribute of the |type| of which this exception refers to
        :param |LeafValidationException| leaf_exception: The exception detailing the leaf property and it's validation message
        :param bool direct_child: whether this summary represents a direct child attribute of the root class or a nested
                             attribute. Affects the display of the summarised message
        """
        if sub_summary is None:
            return super(LeafValidationSummary, cls).__new__(cls, (
                "{}.{}".format(property_name, attribute_name), leaf_exception))
        else:
            _replace_regex = r'^[^.]*'
            return cls.__new__(cls, property_name, re.sub(_replace_regex, attribute_name, sub_summary[0]),
                               sub_summary[1], direct_child=False)

    # noinspection PyMissingConstructor,PyUnusedLocal
    def __init__(self, property_name, attribute_name, leaf_exception, sub_summary=None, direct_child=True):
        self._direct_child = direct_child

    @property
    def message(self):
        """
        The end user friendly formatted message for this leaf exception

        :rtype: str
        """
        return "{} was invalid: {}".format(self[0], self[1].message)


class LeafValidationException(ValidationTreeNode):
    """
    leaf of the validation tree. represents a validation failure of a scalar type
    """

    def __init__(self, of_type, message=None):
        super(LeafValidationException, self).__init__(of_type)
        if message is None:
            message = self._default_message()
        self.message = message

    def _default_message(self):
        return "validation error for type {}".format(self._of_type.__name__)
