Blue State Digital Python API Client
====================================

Requirements
------------

* Python 2.7+

Installing
----------

    $ cd /path/to/setup.py
    $ python setup.py install

The executable's path might not be in your PATH.  In the output for the installer, there is a line that says where the executable is located.  It should say something like 'Installing bsdapi script to /usr/local/bin'.

Configuration File
------------------
The configuration file describes how to connect to your API host and the credentials by which to authenticate. All data needed for this configuration file can be obtained from the Control Panel under **Advanced** -> **Manage API Users**. A sample configuration file is listed below

    [basic]
    host: you.bsd.net
    port: 80
    username: basic_user
    password: basic_pass
    api_id: your_api_id
    secret: 74d5d37963105dc36702f0631adf85db7389613f

The `api_id` and `secret` are taken directly from the Manage API Users page.

The username and password fields are only if HTTP basic authentication is required to access the API.  For most cases, these variables can be left out.

Usage
-----
To display usage options use the `--help` flag

    $ bsdapi --help
    usage: bsdapi [-h] [-L LOG_LEVEL] [-c] [-v] CONFIG

    Blue State Digital API Client

    positional arguments:
      CONFIG                Configuration file

    optional arguments:
      -h, --help            show this help message and exit
      -L LOG_LEVEL, --log-level LOG_LEVEL
                            'debug', 'error', 'warning', 'info', or 'critical'
      -c, --color           Display with ANSI terminal colors.
      -v, --verbose         Show verbose output.

    (c) 2011 Blue State Digital

Raw API Call Example
--------------------
The following walks through making a simple API call to list out all signup forms using the BSD Interactive API shell.

First start the shell.

    $ bsdapi /path/to/config.cfg
    Blue State Digital API Client
    api>

Issue the following command and you should get results similar to what is shown.

    api> print(api.doRequest('/signup/list_forms', {}, api.GET, None))
    HTTP/1.1 200 OK
    Date: Tue, 15 Jun 2010 18:21:54 GMT
    Server: Apache/2.0.63 (Unix) mod_ssl/2.0.63 OpenSSL/0.9.7g PHP/5.2.6
    X-Powered-By: PHP/5.2.6
    Content-Length: 2134
    Content-Type: application/xml; charset=utf-8

    <?xml version="1.0" encoding="UTF-8"?>
    <api>
        <signup_form id="1" modified_dt="1267728690">
            <signup_form_name>Default Signup Form</signup_form_name>
            <signup_form_slug/>
            <form_public_title>This is the public form title</form_public_title>
            <create_dt>2010-02-08 18:33:11</create_dt>
        </signup_form>
        <signup_form id="3" modified_dt="1269523250">
            <signup_form_name>signup form</signup_form_name>
            <signup_form_slug>form</signup_form_slug>
            <form_public_title>This is a signup form</form_public_title>
            <create_dt>2010-03-25 13:20:50</create_dt>
        </signup_form>
    </api>

Python Library Usage
--------------------

The bsdapi can be included as a module and used to build larger applications.  Building a `BsdApi` object is simple using the the factory:

```python
from xml.etree.ElementTree import ElementTree
from StringIO import StringIO
from bsdapi.BsdApi import Factory as BsdApiFactory

api = BsdApiFactory().create(
    id = '',
    secret = '',
    host = 'client.bsd.net',
    port = 80,
    securePort = 443
)

apiResult = api.signup_listForms()
tree = ElementTree().parse( StringIO(apiResult.body) )

print('All Signup Forms:')
for index, signupForm in enumerate(tree.findall('signup_form')):
        print('%d.  %s' % (index+1, signupForm.find('signup_form_name').text))
```

Raw API Method
--------------
To issue a raw API request use the `api.doRequest` method, which will always return a `ApiResult` object. This method accepts 4 parameters as listed below:

* **api_call**

  *Required*

  The RESTful url of the API call without the `/page/api` part.

* **api_params**

  *Optional* -- defaults to `{}`

  The parameters to pass to the API.

* **request_type**

  *Optional* -- defaults to `api.GET`

  The method to use to submit the RESTful call. Can be either `api.GET` or `api.POST`

* **body**

  *Optional* -- defaults to `None`

  You can set the body of a POST request by specifying the fourth parameter.

* **headers**

  *Optional* -- defaults to `None`

* **https**

  *Optional* -- defaults to `False`

  Set this to `True` to send the API call securely using SSL.

API Call Using Helper Methods Example
-------------------------------------
The following walks through making a simple API call to list out all signup forms using the helper methods included with the BSD Interactive API shell.

First start the shell.

    $ bsdapi /path/to/config.cfg
    Blue State Digital API Client
    api>

Issue the following command and you should get results similar to what is shown.

    api> print(api.signup_listForms())
    HTTP/1.1 200 OK
    Date: Tue, 15 Jun 2010 18:21:54 GMT
    Server: Apache/2.0.63 (Unix) mod_ssl/2.0.63 OpenSSL/0.9.7g PHP/5.2.6
    X-Powered-By: PHP/5.2.6
    Content-Length: 2134
    Content-Type: application/xml; charset=utf-8

    <?xml version="1.0" encoding="UTF-8"?>
    <api>
        <signup_form id="1" modified_dt="1267728690">
            <signup_form_name>Default Signup Form</signup_form_name>
            <signup_form_slug/>
            <form_public_title>This is the public form title</form_public_title>
            <create_dt>2010-02-08 18:33:11</create_dt>
        </signup_form>
        <signup_form id="3" modified_dt="1269523250">
            <signup_form_name>signup form</signup_form_name>
            <signup_form_slug>form</signup_form_slug>
            <form_public_title>This is a signup form</form_public_title>
            <create_dt>2010-03-25 13:20:50</create_dt>
        </signup_form>
    </api>

API Helper Methods Documentation
--------------------------------
The following methods are available for use. All methods return a `BsdApiResults` object unless noted otherwise.

* **Account API Calls**
    * `account_checkCredentials(userid, password)`
    * `account_createAccount(email, password, firstname, lastname, zip)`
    * `account_resetPassword(userid)`
    * `account_setPassword(userid, password)`
* **Constituent (cons) API Calls**
    * `cons_getConstituents(filter, bundles=None)`
    * `cons_getConstituentsById(cons_ids, filter=None, bundles=None)`
    * `cons_getConstituentsByExtId(ext_type, ext_ids, filter=None, bundles=None)`
    * `cons_getUpdatedConstituents(changed_since, filter=None, bundles=None)`
    * `cons_setExtIds(ext_type, cons_id__ext_id)`
    * `cons_deleteConstituentsById(cons_ids)`
    * `cons_getBulkConstituentData(format, fields, cons_ids=None, filter=None)`
    * `cons_setConstituentData(xml_data)`
* **Constituent Group (cons_group) API Calls**
    * `cons_group_listConstituentGroups()`
    * `cons_group_getConstituentGroup(cons_group_id)`
    * `cons_group_addConstituentGroup(xml_data)`
    * `cons_group_deleteConstituentGroup(cons_group_ids)`
    * `cons_group_getConsIdsForGroup(cons_group_id)`
    * `cons_group_getExtIdsForGroup(cons_group_id, ext_type)`
    * `cons_group_setExtIdsForGroup(cons_group_id, ext_type, ext_ids)`
    * `cons_group_addConsIdsToGroup(cons_group_id, cons_ids)`
    * `cons_group_addExtIdsToGroup(cons_group_id, ext_type, ext_ids)`
    * `cons_group_removeConsIdsToGroup(cons_group_id, cons_ids)`
    * `cons_group_removeExtIdsToGroup(cons_group_id, ext_type, ext_ids)`
* **Deferred Results API Calls**
    * `getDeferredResults(deferred_id)`
* **Event RSVP API Calls**
    * `event_rsvp_list(event_id)`
* **Outreach (outreach) API Calls**
    * `outreach_getPageById(outreach_page_id)`
    * `outreach_setPageData(xml_data)`
* **Signup (signup) API Calls**
    * `signup_listForms()`
    * `signup_listFormFields(signup_form_id)`
    * `signup_signupCount(signup_form_id, signup_form_field_ids=None)`
    * `signup_countByField(signup_form_id, signup_form_field_id)`
    * `signup_form_id, signup_form_field_id`
* **Wrappers (wrappers) API Calls**
    * `wrappers_listWrappers()`

License
-------

Copyright 2013 Blue State Digital

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
