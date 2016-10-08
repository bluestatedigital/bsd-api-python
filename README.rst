Blue State Digital Python API Client
====================================

A Python SDK for the Blue State Digital API. Stay Progressive.

.. image:: https://travis-ci.org/bmd/bsd-api-python.svg?branch=master
    :target: https://travis-ci.org/bmd/bsd-api-python


Requirements
============

* Python 2.7+
* Python 3.3+

Installing
==========

Install via PyPI.

.. code-block:: bash

    $ pip install bluestatedigital-api

Using the library
=================

Configuring Your API User
-------------------------

Before you can use the Tools API Library, you'll need to configure an API user in the Tools. You can edit an existing user or create a new one from the "Administrator Tools > Manage API Users" page. The ``api_id`` and ``secret`` are taken directly from the Manage API Users page.

API Users in the Tools are granted granular permissions, and can be configured to access - or be prevented from accessing - each API endpoint. You can find a complete list of Tools API endpoints `here <http://tools.bluestatedigital.com/page/api/doc>`_.


Using the library
-----------------

Basic usage
~~~~~~~~~~~

.. code-block:: python

    from bsdapi import BsdApiClient

    # instantiate the API Client
    client = new BsdApiClient(
        'MY_API_ID',
        'MY_API_SECRET',
        'https://my.tools.url.net/'
    )

    # list constituent groups
    resp = client.get('cons_group/list_constituent_groups')

    print resp.status   # 200
    print resp.content  # XML-encoded response body


The API library offers convenience methods for ``get``, ``post``, ``put``, and ``delete`` requests that shadow the native ``requests`` methods of the same name. The main difference is that the BSD API sets a custom authorization driver using ``requests.AuthBase`` that automatically generates the api signing parameters (``api_ts``, ``api_ver``, and ``api_mac``) behind the scenes on each request.

Handling Deferred Responses
~~~~~~~~~~~~~~~~~~~~~~~~~~~

By default, the BSD API library will block on a deferred response (202 status), polling for 30 seconds, at three second intervals until the response is resolved, or throwing an exception if a 200 status response is not received in that time. There are a number of ways that you can control this behavior.

.. code-block:: python

    # 1. turn off blocking entirely. You'll need to make subsequent requests to
    #    the /get_deferred_results endpoint to ensure that your requests were
    #    processed successfully.
    client.block_on_deferred_response = False

    # 2. wait longer between deferral polls
    client.deferred_poll_interval = 10  # interval in seconds

    # 3. allow more poll attempts
    client.deferred_result_max_attempts = 20

Contributing
============

Pull requests are welcome. Issues can be filed in Github or by emailing help@bluestatedigital.com. Please include your Python version, along with a code sample that allows us to reproduce your error.

Changelog
=========

3.0
---

* Removed REPL-style API explorer
* Removed custom logging and message factories - use stdlib ``logging`` module via ``requests``.
* Now uses ``requests``, the excellent python HTTP library
* Removed convenience methods - endpoints are called directly by providing the URL path, body, and query parameters.
* Removed custom ``BsdApiResponse`` object.
* Published on PyPI for improved install experience