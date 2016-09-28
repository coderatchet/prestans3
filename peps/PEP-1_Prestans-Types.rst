PEP: 1
Title: Prestans Types
Version: 1.0_DRAFT
Last-Modified: 19/09/2016
Author: Jared Nagle <jared@anomaly.net.au>
Discussions-To: support@anomaly.com.au
Status: Draft
Type: Standards Track
Created: 19/09/2016

PEP 1 - Prestans Types
======================

.. _abstract:

Abstract
--------
This PEP defines the types &mdash; both on server and client &mdash; that the end user will encounter whilst programming against the
Prestans 3 API. This explains how a Prestans type should behave and how it can be extended as well as any rationale
for restrictions placed on the capabilities of these types.

.. _copyright_public_domain:

Copyright/Public domain
-----------------------
All Prestans 3 literature is licenced under `Apache Licence 2.0`_

.. _Apache Licence 2.0: https://www.apache.org/licenses/LICENSE-2.0

.. _specification:

Specification
-------------

.. _main_goals:

Main Goals
^^^^^^^^^^

A Prestans Configuration Property should:
    - contain validation rules
    - provide sensible defaults e.g. Integer, String, etc |hellip|
    - represent itself in blueprint
    - validate itself |emdash| using user defined rules
        - as a developer of a prestans client
            I want to see a collection of all validation errors for a submitted request
            I want to know what nested variable went wrong and how

    - Serialize itself |emdash| using plugin serializer
    - work with their contextual magic methods; interchangeable with native python objects/scalars.
        >>> import prestans3.types
        >>> Integer(1) == 1 == True
        >>> +Integer(1) == 2 == True
        etc |hellip|

A Prestans Configuration Property should:
    - contain validation rules
    - provide sensible defaults e.g. ``required=False``

.. _base_types:

Base types
^^^^^^^^^^

.. _type_properties:

Type Properties
^^^^^^^^^^^^^^^

Base Type Property
    - can be a member of a class or instantiated on its own.


.. _motivation:

Motivation
----------
As the main purpose of Prestans is to be a *micro rest framework*, It is important to formalise the types and means of
extending these types that end users will have to create and deal with.

.. _rationale:

Rationale
---------

.. _backwards_compatibility:

Backwards Compatibility
-----------------------

.. _ref_impl:

Reference Implementation
------------------------
