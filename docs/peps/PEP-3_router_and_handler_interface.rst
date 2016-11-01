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


Copyright/Public domain
-----------------------


Specification
-------------

.. py:currentmodule:: prestans3.wsgi

The interface consists of a main entry point wsgi application router
:class:`~request_router.RequestRouter` and a base class for implementing custom endpoint handlers
:class:`~request_handler.BaseRequestHandler`

Router
^^^^^^

The RequestRouter is an object that, when instansiated, provides the entry point to an application. It is the front door
to your API. configuration is provided for serializing, deserializing, application wide handler settings and logging.

The router visually acts as a glossary of url patterns to their respective handlers. A route is defined as a tuple pair:
(:class:`str`, T <= :class:`request_router.BaseRequestHandler`).

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

The first argument for a route pair is a python `regular expression`_ `str`. the string should represent a path endpoint
with optional parameter groups marked by regular expression groups. Regex groups will be passed as arguments to the
appropriate handler method of the handler class. named regex groups will be passed as keyword arguments to the handler
method::

    application = RequestRouter(routes=[
        ('/ham/([0-9]+)/spam/(?P<foo>[a-zA-Z_]+)', MyHamSpamHandler)
    ])

matching of regular expressions is global and not multiline

.. _regular expression: https://docs.python.org/3/library/re.html

Motivation
----------


Rationale
---------


Backwards Compatibility
-----------------------


Reference Implementation
------------------------
