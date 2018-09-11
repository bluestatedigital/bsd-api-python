# Copyright 2013 Blue State Digital
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

from bsdapi.Bundles import Bundles
from bsdapi.Filters import Filters
from bsdapi.RequestGenerator import RequestGenerator
from bsdapi.Styler import Factory as StylerFactory
from bsdapi.ApiResult import FactoryFactory as ApiResultFactoryFactory
from bsdapi.ApiResult import ApiResultPrettyPrintable

import requests

import sys, traceback, base64, logging, email.parser


class BsdApi:
    GET = 'GET'
    POST = 'POST'

    def __init__(self, apiId, apiSecret, apiHost, apiResultFactory, apiPort=80, apiSecurePort=443, httpUsername=None,
                 httpPassword=None, verbose=False):
        self.apiId = apiId
        self.apiSecret = apiSecret
        self.apiHost = apiHost
        self.apiResultFactory = apiResultFactory
        self.apiPort = apiPort
        self.apiSecurePort = apiSecurePort
        self.httpUsername = httpUsername
        self.httpPassword = httpPassword
        self.verbose = verbose

    """
        ***** General *****
    """

    def getDeferredResults(self, deferred_id):
        query = {'deferred_id': deferred_id}
        url_secure = self._generateRequest('/get_deferred_results', query)
        return self._makeGETRequest(url_secure)

    def doRequest(self, api_call, api_params=None, request_type=GET, body=None, headers=None, https=True):
        url = self._generateRequest(api_call, api_params, https)

        if request_type == "GET":
            return self._makeGETRequest(url, https)
        else:
            return self._makePOSTRequest(url, body, https)

    def doRawRequest(self, api_call, api_params=None, request_type=GET, body=None, headers=None, https=True):
        url = self._generateRequest(api_call, api_params, https)
        return self._makeRequest(url, request_type, body, headers, https)

    """
        ***** Account *****
    """

    def account_checkCredentials(self, userid, password):
        query = {'userid': userid, 'password': password}
        url_secure = self._generateRequest('/account/check_credentials', query, https=True)
        return self._makeGETRequest(url_secure, https=True)

    def account_createAccount(self, email, password, firstname, lastname, zipCode):
        query = {'email': email, 'password': password, 'firstname': firstname, 'lastname': lastname, 'zip': zipCode}
        url_secure = self._generateRequest('/account/create_account', query, https=True)
        return self._makeGETRequest(url_secure, https=True)

    def account_resetPassword(self, userid):
        query = {'userid': userid}
        url_secure = self._generateRequest('/account/reset_password', query, https=True)
        return self._makeGETRequest(url_secure, https=True)

    def account_setPassword(self, userid, password):
        query = {'userid': userid, 'password': password}
        url_secure = self._generateRequest('/account/set_password', query, https=True)
        return self._makeGETRequest(url_secure, https=True)

    """
        ***** Cons *****
    """

    def cons_getConstituents(self, request_filter, bundles=None):
        query = {'filter': str(Filters(request_filter))}

        if bundles:
            query['bundles'] = str(Bundles(bundles))

        url_secure = self._generateRequest('/cons/get_constituents', query)
        return self._makeGETRequest(url_secure)

    def cons_getConstituentsById(self, cons_ids, request_filter=None, bundles=None):
        """Retrieves constituents by ID """
        query = {'cons_ids': ','.join([str(elem) for elem in cons_ids])}

        if request_filter:
            query['filter'] = str(Filters(request_filter))

        if bundles:
            query['bundles'] = str(Bundles(bundles))

        url_secure = self._generateRequest('/cons/get_constituents_by_id', query)
        return self._makeGETRequest(url_secure)

    def cons_getConstituentsByExtId(self, ext_type, ext_ids, request_filter=None, bundles=None):
        query = {'ext_type': ext_type, 'ext_ids': ','.join([str(elem) for elem in ext_ids])}

        if request_filter:
            query['filter'] = str(Filters(request_filter))

        if bundles:
            query['bundles'] = str(Bundles(bundles))

        url_secure = self._generateRequest('/cons/get_constituents_by_ext_id', query)
        return self._makeGETRequest(url_secure)

    def cons_getUpdatedConstituents(self, changed_since, request_filter=None, bundles=None):
        query = {'changed_since': str(changed_since)}

        if request_filter:
            query['filter'] = str(Filters(request_filter))

        if bundles:
            query['bundles'] = str(Bundles(bundles))

        url_secure = self._generateRequest('/cons/get_updated_constituents', query)
        return self._makeGETRequest(url_secure)

    def cons_setExtIds(self, ext_type, cons_id__ext_id):
        query = {'ext_type': str(ext_type)}
        query.update(cons_id__ext_id)
        url_secure = self._generateRequest('/cons/set_ext_ids')
        return self._makePOSTRequest(url_secure, query)

    def cons_deleteConstituentsById(self, cons_ids):
        query = {'cons_ids': ','.join([str(cons) for cons in cons_ids])}
        url_secure = self._generateRequest('/cons/delete_constituents_by_id')
        return self._makePOSTRequest(url_secure, query)

    def cons_getBulkConstituentData(self, request_format, fields, cons_ids=None, request_filter=None):
        query = {'format': str(request_format), 'fields': ','.join([str(field) for field in fields])}

        if cons_ids:
            query['cons_ids'] = ','.join([str(cons) for cons in cons_ids])

        if request_filter:
            query['filter'] = str(Filters(request_filter))

        url_secure = self._generateRequest('/cons/get_bulk_constituent_data', {})
        return self._makePOSTRequest(url_secure, query)

    def cons_setConstituentData(self, xml_data):
        """
        This path has been deprecated. Please use cons_upsertConstituentDate() instead.
        """
        url_secure = self._generateRequest('/cons/set_constituent_data')
        return self._makePOSTRequest(url_secure, xml_data)

    def cons_upsertConstituentData(self, xml_data):
        url_secure = self._generateRequest('/cons/upsert_constituent_data')
        return self._makePOSTRequest(url_secure, xml_data)

    def cons_setCustomConstituentFields(self, xml_data, cons_id, delete_missing):
        query = {'cons_id': str(cons_id), 'delete_missing': str(delete_missing)}
        url_secure = self._generateRequest('/cons/set_custom_constituent_fields', query)
        return self._makePOSTRequest(url_secure, xml_data)

    def cons_getCustomConstituentFields(self):
        query = {}
        url_secure = self._generateRequest('/cons/get_custom_constituent_fields', query)
        return self._makeGETRequest(url_secure)

    def cons_mergeConstituentsById(self, ids):
        url_secure = self._generateRequest('/cons/merge_constituents_by_id')
        return self._makePOSTRequest(url_secure, ','.join([str(x) for x in ids]))

    def cons_mergeConstituentsByEmail(self, email):
        url_secure = self._generateRequest('/cons/merge_constituents_by_email', {'email': email})
        return self._makeGETRequest(url_secure)

    def cons_listDatasets(self):
        url_secure = self._generateRequest('cons/list_datasets')
        return self._makeGETRequest(url_secure)

    def cons_listDatasetMaps(self):
        url_secure = self._generateRequest('cons/list_dataset_maps')
        return self._makeGETRequest(url_secure)

    def cons_uploadDataset(self, slug, map_type, csv_data):
        query = {'slug': str(slug),
                 'map_type': str(map_type),
                 'csv_data': str(csv_data)}
        url_secure = self._generateRequest('/cons/upload_dataset')
        return self._makePOSTRequest(url_secure, query)

    def cons_uploadDatasetMap(self, csv_data):
        query = {'csv_data': str(csv_data)}
        url_secure = self._generateRequest('/cons/upload_dataset_map')
        return self._makePOSTRequest(url_secure, query)

    def cons_deleteDataset(self, dataset_id):
        query = {'dataset_id': str(dataset_id)}
        url_secure = self._generateRequest('/cons_group/delete_dataset', query)
        return self._makeGETRequest(url_secure)

    def cons_deleteDatasetMap(self, map_id):
        query = {'map_id': str(map_id)}
        url_secure = self._generateRequest('/cons_group/delete_dataset_map', query)
        return self._makeGETRequest(url_secure)

    """
        ***** Cons_Group *****
    """

    def cons_group_listConstituentGroups(self):
        url_secure = self._generateRequest('/cons_group/list_constituent_groups')
        return self._makeGETRequest(url_secure)

    def cons_group_getConstituentGroup(self, cons_group_id):
        query = {'cons_group_id': str(cons_group_id)}
        url_secure = self._generateRequest('/cons_group/get_constituent_group', query)
        return self._makeGETRequest(url_secure)

    def cons_group_addConstituentGroup(self, xml_data):
        url_secure = self._generateRequest('/cons_group/add_constituent_groups')
        return self._makePOSTRequest(url_secure, xml_data)

    def cons_group_deleteConstituentGroups(self, cons_group_ids):
        query = {'cons_group_ids': ','.join([str(c) for c in cons_group_ids])}
        url_secure = self._generateRequest('/cons_group/delete_constituent_groups', query)
        return self._makeGETRequest(url_secure)

    def cons_group_getConsIdsForGroup(self, cons_group_id):
        query = {'cons_group_id': str(cons_group_id)}
        url_secure = self._generateRequest('/cons_group/get_cons_ids_for_group', query)
        return self._makeGETRequest(url_secure)

    def cons_group_getExtIdsForGroup(self, cons_group_id, ext_type):
        query = {'cons_group_ids': str(cons_group_id), 'ext_type': ext_type}
        url_secure = self._generateRequest('/cons_group/get_ext_ids_for_group', query)
        return self._makeGETRequest(url_secure)

    def cons_group_setExtIdsForGroup(self, cons_group_id, ext_type, ext_ids):
        query = {'cons_group_id': str(cons_group_id),
                 'ext_type': ext_type,
                 'ext_ids': ','.join([str(ext) for ext in ext_ids])}

        url_secure = self._generateRequest('/cons_group/set_ext_ids_for_group')
        return self._makePOSTRequest(url_secure, query)

    def cons_group_addConsIdsToGroup(self, cons_group_id, cons_ids):
        query = {'cons_group_id': str(cons_group_id),
                 'cons_ids': ','.join([str(cons) for cons in cons_ids])}

        url_secure = self._generateRequest('/cons_group/add_cons_ids_to_group')
        return self._makePOSTRequest(url_secure, query)

    def cons_group_setConsIdsForGroup(self, cons_group_id, cons_ids):
        query = {'cons_group_id': str(cons_group_id),
                 'cons_ids': ','.join([str(cons) for cons in cons_ids])}

        url_secure = self._generateRequest('/cons_group/set_cons_ids_for_group')
        return self._makePOSTRequest(url_secure, query)

    def cons_group_addExtIdsToGroup(self, cons_group_id, ext_type, ext_ids):
        query = {'cons_group_id': str(cons_group_id),
                 'ext_type': ext_type,
                 'ext_ids': ','.join([str(ext) for ext in ext_ids])}

        url_secure = self._generateRequest('/cons_group/add_ext_ids_to_group')
        return self._makePOSTRequest(url_secure, query)

    def cons_group_removeConsIdsFromGroup(self, cons_group_id, cons_ids):
        query = {'cons_group_id': str(cons_group_id),
                 'cons_ids': ','.join([str(cons) for cons in cons_ids])}

        url_secure = self._generateRequest('/cons_group/remove_cons_ids_from_group')
        return self._makePOSTRequest(url_secure, query)

    def cons_group_removeExtIdsFromGroup(self, cons_group_id, ext_type, ext_ids):
        query = {'cons_group_id': str(cons_group_id),
                 'ext_type': ext_type,
                 'ext_ids': ','.join([str(ext) for ext in ext_ids])}

        url_secure = self._generateRequest('/cons_group/remove_ext_ids_from_group')
        return self._makePOSTRequest(url_secure, query)

    """
        ***** Contribution *****
    """

    def contribution_getContributions(self, request_filter):
        """
        Get contributions with a filter

        **Does not currently support filtering by source**
        """
        query = {}
        for key, value in request_filter.items():
            query['filter[' + key + ']'] = value

        url_secure = self._generateRequest('/contribution/get_contributions', query)
        print(url_secure)
        return self._makeGETRequest(url_secure)

    """
        ***** Event_RSVP *****
    """

    def event_rsvp_list(self, event_id):
        query = {'event_id': str(event_id)}
        url_secure = self._generateRequest('/event/list_rsvps')
        return self._makePOSTRequest(url_secure, query)

    """
        ***** Mailer *****
    """

    def mailer_sendTriggeredEmail(self, mailing_id, email, email_opt_in=False):
        """Send a triggered email"""
        query = {
            'mailing_id': mailing_id,
            'email': email,
            'email_opt_in': int(email_opt_in)
        }
        url_secure = self._generateRequest('/mailer/send_triggered_email', query)
        return self._makeGETRequest(url_secure)

    """
        ***** Outreach *****
    """

    def outreach_getPageById(self, page_id):
        query = {'id': str(page_id)}
        url_secure = self._generateRequest('/outreach/get_page_by_id')
        return self._makePOSTRequest(url_secure, query)

    def outreach_setPageData(self, xml_data):
        url_secure = self._generateRequest('/outreach/set_page_data', {})
        return self._makePOSTRequest(url_secure, xml_data)

    """
        ***** Reference *****
    """

    def reference_processPersonalizationTag(self, who):
        url_secure = self._generateRequest('/reference/process_personalization_tag', {'who': who})
        return self._makeGETRequest(url_secure)

    """
        ***** Signup *****
    """

    def signup_processSignup(self, xml_data):
        query = {}
        url_secure = self._generateRequest('/signup/process_signup', query)
        return self._makePOSTRequest(url_secure, xml_data)

    def signup_listForms(self):
        query = {}
        url_secure = self._generateRequest('/signup/list_forms', query, True)
        return self._makeGETRequest(url_secure, True)

    def signup_listFormFields(self, signup_form_id):
        query = {'signup_form_id': str(signup_form_id)}
        url_secure = self._generateRequest('/signup/list_form_fields', query)
        return self._makeGETRequest(url_secure)

    def signup_signupCount(self, signup_form_id, signup_form_field_ids=None):
        query = {'signup_form_id': str(signup_form_id)}

        if signup_form_field_ids:
            query['signup_form_field_ids'] = ','.join([str(elem) for elem in signup_form_field_ids])

        url_secure = self._generateRequest('/signup/signup_count', query)
        return self._makeGETRequest(url_secure)

    def signup_countByField(self, signup_form_id, signup_form_field_id):
        query = {'signup_form_id': str(signup_form_id),
                 'signup_form_field_id': str(signup_form_field_id)}

        url_secure = self._generateRequest('/signup/count_by_field', query)
        return self._makeGETRequest(url_secure)

    """
        ***** Wrappers *****
    """

    def wrappers_listWrappers(self):
        url_secure = self._generateRequest('/wrappers/list_wrappers')
        return self._makeGETRequest(url_secure)

    """
        ***** Internal/Helpers *****
    """

    def _makeRequest(self, url_secure, request_type, http_body=None, headers=None, https=True):
        if self.apiPort == 443:
            https = True
        # TODO: support nonstandard ports?  We block them on Akamai anyway.

        composite_url = ("https://" if https else "http://") + self.apiHost + url_secure.getPathAndQuery()

        if headers == None:
            headers = dict()

        headers['User-Agent'] = 'Python API'

        if self.httpUsername:
            auth_string = self.httpUsername
            if self.httpPassword:
                auth_string += ":" + self.httpPassword
            headers["Authorization"] = "Basic " + base64.b64encode(auth_string.encode('utf-8')).decode('utf-8')

        if self.verbose:
            print(request_type + " " + composite_url)
            print('\n'.join(['%s: %s' % (k, v) for k, v in headers.items()]))
            print("\n%s\n\n----\n" % http_body)

        try:
            response = requests.request(request_type, composite_url, data=http_body, headers=headers, verify=True)

            headers = response.headers
            body = response.text

            results = self.apiResultFactory.create(url_secure, response, headers, body)
            return results

        except requests.exceptions.RequestException as error:
            print(error)
            print("Error calling " + url_secure.getPathAndQuery())

    def _generateRequest(self, api_call, api_params=None, https=True):
        if api_params is None:
            api_params = {}
        if self.apiPort == 443:
            https = True

        apiHost = self.apiHost
        if https:
            if self.apiSecurePort != 443:
                apiHost = apiHost + ':' + str(self.apiSecurePort)
        else:
            if self.apiPort != 80:
                apiHost = apiHost + ":" + str(self.apiPort)

        request = RequestGenerator(self.apiId, self.apiSecret, apiHost, https)
        url_secure = request.getUrl(api_call, api_params)
        return url_secure

    def _makeGETRequest(self, url_secure, https=True):
        return self._makeRequest(url_secure, BsdApi.GET, https=https);

    def _makePOSTRequest(self, url_secure, body, https=True):
        headers = {"Content-type": "application/x-www-form-urlencoded",
                   "Accept": "text/xml"}
        return self._makeRequest(url_secure, BsdApi.POST, body, headers, https)


class Factory:
    def __init__(self):
        pass

    def create(self, api_id, secret, host, port, securePort, colorize=False):
        styler = StylerFactory().create(colorize)
        apiResultFactory = ApiResultFactoryFactory().create(ApiResultPrettyPrintable(styler))
        return BsdApi(api_id, secret, host, apiResultFactory, port, securePort)
