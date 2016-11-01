==============
Prestans 3 API
==============

.. include all the api documents here

Types
=====

.. py:currentmodule:: prestans3.types

ImmutableType
-------------

.. autoclass:: ImmutableType
    :show-inheritance:
    :members:

_Property
---------

.. autoclass:: _Property
    :members:
    :special-members:
    :exclude-members: __weakref__

PrestansTypeMeta
----------------

.. py:currentmodule:: prestans3.types.meta

.. autoclass:: PrestansTypeMeta

.. autoattribute:: PrestansTypeMeta.property_rules
.. autoattribute:: PrestansTypeMeta.prepare_functions
.. autoattribute:: PrestansTypeMeta.config_checks

String
------

.. py:currentmodule:: prestans3.types.string

.. autoclass:: String
    :show-inheritance:
    :members:
    :exclude-members: __init__

Boolean
-------

.. py:currentmodule:: prestans3.types.boolean

.. autoclass:: Boolean
    :show-inheritance:
    :members:
    :exclude-members: __init__

Number
------

.. py:currentmodule:: prestans3.types.number

.. autoclass:: Number
    :members:
    :show-inheritance:

Integer
~~~~~~~

.. py:currentmodule:: prestans3.types.integer

.. autoclass:: Integer
    :show-inheritance:
    :members:
    :exclude-members: __init__

Float
~~~~~

.. py:currentmodule:: prestans3.types.float

.. autoclass:: Float
    :show-inheritance:
    :members:
    :exclude-members: __init__


Container
---------

.. py:currentmodule:: prestans3.types

.. autoclass:: Container
    :members:
    :special-members:
    :exclude-members: __weakref__

Model
~~~~~

.. autoclass:: Model
    :members:
    :special-members:
    :exclude-members: __weakref__, __init__

Array
~~~~~

.. autoclass:: Array
    :members:
    :exclude-members: __weakref__


Temporal
--------

.. py:currentmodule:: prestans3.types.temporal

.. autoclass:: Temporal
    :show-inheritance:


Date
~~~~

.. py:currentmodule:: prestans3.types.p_date

.. autoclass:: Date
    :show-inheritance:
    :members:
    :exclude-members: __init__

DateTime
~~~~~~~~

.. py:currentmodule:: prestans3.types.p_datetime

.. autoclass:: DateTime
    :show-inheritance:
    :members:
    :exclude-members: __init__

Time
~~~~

.. py:currentmodule:: prestans3.types.p_time

.. autoclass:: Time
    :show-inheritance:
    :members:
    :exclude-members: __init__

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


ContainerValidationException
----------------------------

.. autoclass:: ContainerValidationException
    :show-inheritance:
    :members:
    :special-members:


ContainerValidationExceptionSummary
-----------------------------------

.. py:currentmodule:: prestans3.errors

.. autoclass:: ContainerValidationExceptionSummary
        :show-inheritance:
        :members:
        :special-members: __new__
        :exclude-members: __init__


ModelValidationException
------------------------

.. py:currentmodule:: prestans3.types.model

.. autoclass:: ModelValidationException
        :show-inheritance:
        :members:
        :special-members:
        :exclude-members: __init__


ArrayValidationException
------------------------

.. py:currentmodule:: prestans3.types.array

.. autoclass:: ArrayValidationException
        :show-inheritance:
        :members:
        :special-members:
        :exclude-members: __init__

WSGI
====


.. py:currentmodule:: prestans3.wsgi.request_router

.. autoclass:: RequestRouter


Utils
=====

MergingProxyDictionary
----------------------

.. py:currentmodule:: prestans3.utils

.. autoclass:: MergingProxyDictionary
    :show-inheritance:
    :special-members: __init__

ImmutableMergingDictionary
--------------------------

.. autoclass:: ImmutableMergingDictionary
    :show-inheritance:

inject_class
------------

.. autofunction:: inject_class

LazyOneWayGraph
---------------

.. autoclass:: LazyOneWayGraph
    :show-inheritance:
    :members:

