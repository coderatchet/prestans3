PEP 3 - Request Router and Handlers
===================================


Preamble
--------
Request redirection and content propagation should be simple yet as configurable as needed. The way a ReST api is
constructed should not inhibit scalability and promote good practices. In Prestans 3's implementation of request and
route handling, conforming to our suggested process of endpoint creation should result in a ReST conformant,
"good-citizen" API. Given the high level of misunderstanding about what ReST actually is, using the Prestans 3 route and
handler interface will help enforce the true concepts of ReST without inhibiting the creativity of the API developer.

Abstract
--------

Defines the implementation and intended use of the Prestans 3 |RequestRouter| and |BaseRequestHandler|\ .


Copyright/Public domain
-----------------------
All Prestans 3 literature is licenced under `Apache Licence 2.0`_

:copyright: |copy| 2016 Anomaly Software

.. _Apache Licence 2.0: https://www.apache.org/licenses/LICENSE-2.0


Specification
-------------

.. py:currentmodule:: prestans3.wsgi

The interface consists of a main entry point wsgi application router:|RequestRouter|  and a base class for implementing
custom endpoint handlers: |BaseRequestHandler|\ .

Router
^^^^^^

The RequestRouter is an object that, when instansiated, provides the entry point to an application. It is the front door
to your API. configuration is provided for serializing, deserializing, application wide handler settings and logging.

The router visually acts as a glossary of url patterns to their respective handlers. A route is defined as a tuple pair:
(:class:`str`, T <= |BaseRequestHandler|\ ).

The most simple use case will appear like this (note that handlers are defined alongside this code for example's sake)::

    from prestans3.wsgi.request_router import RequestRouter, BaseRequestHandler

    class MyHandler(BaseRequestHandler):
        ...

    class MySpamHandler(BaseRequestHandler):
        ...

    application = RequestRouter(application_name="my_first_prestans3_app",
        routes=[
            ('/', MyHandler),
            ('/spam', MySpamHandler),
            ...
        ])

.. _regular expression: https://docs.python.org/3/library/re.html

The first argument for a route pair is a python `regular expression`_ `str`. the string should represent a path endpoint
with optional parameter groups marked by regular expression groups. Regex groups will be passed as arguments to the
appropriate handler method of the handler class. named regex groups will be passed as keyword arguments to the handler
method::

    application = RequestRouter(routes=[
        ('/ham/([0-9]+)/spam/(?P<foo>[a-zA-Z_]+)', MyHamSpamHandler),
        ...
    ])
    calling GET '/ham/123/spam/bar'
    # calls MyHamSpamHandler.some_get_method(123, foo='bar')

Path expressions have implicit ``^`` and ``$`` markers on the start and end of the str respectively. If these markers
already exist, they are ignored::

    ['^/$', '^/', '/$', '/'] # these path expressions all result in '^/$'

Handler
^^^^^^^

Each handler should extend |BaseRequestHandler|. methods are defined at the HTTP verb level::

    class FooHandler(BaseRequestHandler):
        @response(response_template=Array.property(Integer))
        def my_get(arg1, arg2):
            return [1,2,3]

Part of Prestans 3's value is the ability to define well-defined contracts for both requests and responses. By default,
calling the ``OPTIONS`` http method on an endpoint will retrieve its |blueprint|\ . An |blueprint| is a well-defined
, computer-parsable |IDL| for describing ReST endpoints. The blueprint provides a list of available HTTP verbs for
an endpoint, the expected request and response format and any conditions that apply to the content of any properties in
the request (such as ``min_length`` and ``required``).

|blueprints| are built-in to the standard |types| and are enabled by default. A developer may add keyword arguments to
custom |Model| definitions (through the :meth:`ImmutableType.property()<prestans3.types.ImmutableType.property>` method)
and ``[request/response]_template`` property definitions in order to provide information for each of the |Model|\ 's
|attributes| when querying its blueprint.

Defining a Handler Method
"""""""""""""""""""""""""

A request handler method is unique for each permutation of url path, query parameters and http verb. the name of a
method is arbitrary but should indicate what verb it supports e.g. ``def get_with_search_keywords(...)``. Methods
defined on the |BaseRequestHandler| may be configured to handle requests and constrain responses using the |@request|
and |@response| decorators.

Request Decorator
"""""""""""""""""


Backwards Compatibility
-----------------------

The current implementation of request handlers and routers should support Python 2.7+, 3.4+ and PyPy.


Reference Implementation
------------------------

see :mod:`~prestans3.wsgi`.