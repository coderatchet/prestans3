from prestans3.types import Property, Structure
import re


class ValidationTreeNode(object):
    def __init__(self, of_type):
        self._of_type = of_type

    @property
    def property_type(self):
        return self._of_type


class ValidationTree(ValidationTreeNode):
    """
    A |Structure| validation result, contains a dictionary of attribute names to their
    ValidationTreeNodes or LeafValidationException for structure and scalar attributes respectively
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

    def items(self):
        """
        smart dictionary when iterated through
        :return:
        """
        for key, value in list(self.validation_exceptions.items()):  # type: (str, LeafValidationException)
            if isinstance(value, LeafValidationException):
                yield ("{}.{}".format(self.property_type.__name__, key), value)
            else:
                for sub_key, sub_value in list(value.items()):
                    yield ("{}.{}".format(self.property_type.__name__, re.sub(r'^(.*)\.', "{}.".format(key), sub_key)),
                           sub_value)


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
