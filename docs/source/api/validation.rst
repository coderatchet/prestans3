Validation
==========

These classes make the presentation of validation results easier for a client or api developer to understand. Each
validation will contain a tree structure of validation errors that may be iterated through

.. py:currentmodule:: prestans3.validation_tree

ValidationTreeNode
------------------

.. autoclass:: .ValidationTreeNode
    :members:

ValidationTree
--------------

.. autoclass:: .ValidationTree
    :members:

ValidationException
-----------------------

.. autoclass:: .ValidationException
    :members:

ValidationExceptionSummary
---------------------

.. autoclass:: .ValidationExceptionSummary
    :members:
    :special-members: __new__
    :exclude-members: __init__
