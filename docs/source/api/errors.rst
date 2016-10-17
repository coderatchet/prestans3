Errors
======

These classes make the presentation of validation results easier for a client or api developer to understand. Each
validation will contain a tree structure of validation errors that may be iterated through

.. py:currentmodule:: prestans3.errors

ValidationException
-------------------

.. autoclass:: ValidationException
    :members:
    :special-members:
    :exclude-members: __weakref__


ValidationExceptionSummary
--------------------------

.. autoclass:: ValidationExceptionSummary
    :members:
    :special-members: __new__
    :exclude-members: __init__


.. py:currentmodule:: prestans3.types.model

ModelValidationException
------------------------

.. autoclass:: ModelValidationException
    :show-inheritance:
    :members:
    :special-members:
    :exclude-members: __init__


ContainerValidationExceptionSummary
-----------------------------------

.. autoclass:: ContainerValidationExceptionSummary
    :show-inheritance:
    :members:
    :special-members: __new__
    :exclude-members: __init__