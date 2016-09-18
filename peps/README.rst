Prestans Enhancement Proposal (PEP)
===================================

The purpose of these PEPs are more or less the same as the official Python Enhancement Proposals. Thus for consistency's
and simplicity's sake we will maintain the guides set by PEP 1. for reference, an `excerpt from PEP`_ below summarises
the contents of a typical PEP.

.. _excerpt from PEP: https://www.python.org/dev/peps/pep-0001/#what-belongs-in-a-successful-pep

  **What belongs in a successful PEP**

  Each PEP should have the following parts:

  :Preamble:
    RFC 822 style headers containing meta-data about the PEP, including the PEP number, a short descriptive
    title (limited to a maximum of 44 characters), the names, and optionally the contact info for each author, etc.

  :Abstract:
    a short (~200 word) description of the technical issue being addressed.

  :Copyright/public domain:
    Each PEP must either be explicitly labeled as placed in the public domain (see this PEP as
    an example) or licensed under the Open Publication License [7] .

  :Specification:
    The technical specification should describe the syntax and semantics of any new language feature.
    The specification should be detailed enough to allow competing, interoperable implementations for at least the
    current major Python platforms (CPython, Jython, IronPython, PyPy).

  :Motivation:
    The motivation is critical for PEPs that want to change the Python language. It should clearly explain
    why the existing language specification is inadequate to address the problem that the PEP solves. PEP submissions
    without sufficient motivation may be rejected outright.

  :Rationale:
    The rationale fleshes out the specification by describing what motivated the design and why particular
    design decisions were made. It should describe alternate designs that were considered and related work, e.g. how the
    feature is supported in other languages.

    The rationale should provide evidence of consensus within the community and discuss important objections or concerns
    raised during discussion.

  :Backwards Compatibility:
    All PEPs that introduce backwards incompatibilities must include a section describing
    these incompatibilities and their severity. The PEP must explain how the author proposes to deal with these
    incompatibilities. PEP submissions without a sufficient backwards compatibility treatise may be rejected outright.

  :Reference Implementation:
    The reference implementation must be completed before any PEP is given status "Final",
    but it need not be completed before the PEP is accepted. While there is merit to the approach of reaching consensus
    on the specification and rationale before writing code, the principle of "rough consensus and running code" is still
    useful when it comes to resolving many discussions of API details.

  The final implementation must include test code and documentation appropriate for either the Python language reference
  or the standard library reference.
