import requests_mock
from bsdapi.BsdApi import Factory
from bsdapi.BsdApi import BsdApi
from mock import patch
from mock import Mock
from urllib.parse import urlparse
from urllib.parse import parse_qs
import pytest
import time
from bsdapi.ApiResult import FactoryFactory as ApiResultFactoryFactory
from freezegun import freeze_time

mock_time = Mock()
mock_time.return_value = 1122334455
API_ID = 'my-id'
API_SECRET = 'my-secret'
API_HOST = 'my.client'


@pytest.fixture
def api_client():
    """
    :return: BsdApi
    """
    return Factory().create(API_ID, API_SECRET, API_HOST, 80, 443)


def get_query_parameter_matcher(expected_params):
    """
    Matches the request only if all of the expected GET parameters are present
    """
    return lambda request: all(v in parse_qs(urlparse(request.url).query)[k] for k, v in expected_params.items())


def post_query_parameter_matcher(expected_params):
    """
    Matches the request only if all of the expected POST variables are present
    """
    return lambda request: all(v in parse_qs(request.text)[k] for k, v in expected_params.items())


def test_do_request_secure_url(api_client):
    """
    If secure URLs are requested, then the https protocol is used (this is also the default)
    """
    with requests_mock.Mocker() as m:
        m.register_uri('GET', 'https://my.client/page/api/thing/list_things')
        # Explicit:
        api_client.doRequest('/thing/list_things', None, 'GET', None, None, True)
        # Not provided:
        api_client.doRequest('/thing/list_things', None, 'GET', None, None)


def test_do_request_insecure_url(api_client):
    """
    If insecure URLs are explicitly requested, then the http protocol is used
    """
    with requests_mock.Mocker() as m:
        m.register_uri('GET', 'http://my.client/page/api/thing/list_things')
        api_client.doRequest('/thing/list_things', None, 'GET', None, None, False)


def test_do_request_auth():
    """
    If an HTTP username and password have been assigned, they will be included in the Authorization header
    """
    with requests_mock.Mocker() as m:
        m.register_uri('GET', 'https://my.client/page/api/thing/list_things',
                       additional_matcher=lambda req: req.headers['authorization'] == 'Basic YWRtaW46cGFzc3dvcmQ=')
        api_result_factory = ApiResultFactoryFactory().create(None)
        api_client = BsdApi(API_ID, API_SECRET, API_HOST, api_result_factory, 80, 443, 'admin', 'password')
        api_client.doRequest('/thing/list_things')


@freeze_time('2000-01-01')
def test_do_request_signing_string(api_client):
    """
    The signing string should be the hmac hash of the API id, timestamp, call, and query
    """
    with requests_mock.Mocker() as m:
        hmac = 'cdeeab080173ba36f39b18b8311535bfa5e9b62c'  # Specific to this case
        m.register_uri('GET', 'https://my.client/page/api/thing/list_things',
                       additional_matcher=get_query_parameter_matcher({'api_mac': hmac}))

        api_client.doRequest('/thing/list_things')


@freeze_time('1970-01-02')
def test_do_request_timestamp(api_client):
    """
    API calls must include a timestamp
    """
    with requests_mock.Mocker() as m:
        m.register_uri('GET', 'https://my.client/page/api/thing/list_things',
                       additional_matcher=get_query_parameter_matcher({'api_ts': '86400'}))

        api_client.doRequest('/thing/list_things')


def test_do_request_user_agent(api_client):
    """
    The API client uses a fixed User Agent
    """
    with requests_mock.Mocker() as m:
        m.register_uri('GET', 'https://my.client/page/api/thing/list_things',
                       additional_matcher=lambda req: req.headers['user-agent'] == 'Python API')

        assert api_client.doRequest('/thing/list_things').http_status == 200


def test_get_deferred_results(api_client):
    with requests_mock.Mocker() as m:
        m.register_uri("GET", 'https://my.client/page/api/get_deferred_results',
                       additional_matcher=get_query_parameter_matcher({'deferred_id': '12345'}))

        result = api_client.getDeferredResults('12345')
        assert result.http_status == 200


def test_account_check_credentials(api_client):
    with requests_mock.Mocker() as m:
        m.register_uri('GET', 'https://my.client/page/api/account/check_credentials',
                       additional_matcher=get_query_parameter_matcher({'userid': 'me', 'password': 'mypass'}))

        result = api_client.account_checkCredentials('me', 'mypass')
        assert result.http_status == 200


def test_account_create_account(api_client):
    with requests_mock.Mocker() as m:
        expected_params = {
            'email': 'my@email.bsd',
            'password': 'mypass',
            'firstname': 'John',
            'lastname': 'Doe',
            'zip': '10101'
        }
        m.register_uri('get', 'https://my.client/page/api/account/create_account',
                       additional_matcher=get_query_parameter_matcher(expected_params))

        result = api_client.account_createAccount('my@email.bsd', 'mypass', 'John', 'Doe', '10101')
        assert result.http_status == 200


def test_account_reset_password(api_client):
    with requests_mock.Mocker() as m:
        m.register_uri('GET', 'https://my.client/page/api/account/reset_password',
                       additional_matcher=get_query_parameter_matcher({'userid': 'thisisme'}))

        result = api_client.account_resetPassword('thisisme')
        assert result.http_status == 200


def test_account_set_password(api_client):
    with requests_mock.Mocker() as m:
        m.register_uri('GET', 'https://my.client/page/api/account/set_password',
                       additional_matcher=get_query_parameter_matcher({'userid': 'thisisme', 'password': 'mynewpass'}))

        result = api_client.account_setPassword('thisisme', 'mynewpass')
        assert result.http_status == 200


def test_cons_get_constituents(api_client):
    with requests_mock.Mocker() as m:
        expected_params = {'filter': 'state_cd=FL', 'bundles': 'abcd,efgh'}
        m.register_uri('GET', 'https://my.client/page/api/cons/get_constituents',
                       additional_matcher=get_query_parameter_matcher(expected_params))

        result = api_client.cons_getConstituents({'state_cd': 'FL'}, ['abcd', 'efgh'])
        assert result.http_status == 200


def test_cons_get_constituents_by_id(api_client):
    with requests_mock.Mocker() as m:
        expected_params = {'cons_ids': '1,2,3,4', 'filter': 'state_cd=FL', 'bundles': 'abcd'}
        m.register_uri('GET', 'https://my.client/page/api/cons/get_constituents_by_id',
                       additional_matcher=get_query_parameter_matcher(expected_params))

        result = api_client.cons_getConstituentsById([1, 2, 3, 4], {'state_cd': 'FL'}, ['abcd'])
        assert result.http_status == 200


def test_cons_get_constituents_by_ext_id(api_client):
    with requests_mock.Mocker() as m:
        expected_params = {'ext_ids': '5,4,3', 'ext_type': 'myexternal', 'filter': 'state_cd=ME', 'bundles': 'abc'}
        m.register_uri('GET', 'https://my.client/page/api/cons/get_constituents_by_ext_id',
                       additional_matcher=get_query_parameter_matcher(expected_params))

        result = api_client.cons_getConstituentsByExtId('myexternal', [5, 4, 3], {'state_cd': 'ME'}, ['abc'])
        assert result.http_status == 200


@patch('time.time', mock_time)
def test_cons_get_updated_constituents(api_client):
    with requests_mock.Mocker() as m:
        expected_params = {'changed_since': '1122334455', 'filter': 'state_cd=WI', 'bundles': 'bund'}
        m.register_uri('GET', 'https://my.client/page/api/cons/get_updated_constituents',
                       additional_matcher=get_query_parameter_matcher(expected_params))

        result = api_client.cons_getUpdatedConstituents(time.time(), {'state_cd': 'WI'}, ['bund'])
        assert result.http_status == 200


@patch('time.time', mock_time)
def test_cons_get_updated_constituent_ids(api_client):
    with requests_mock.Mocker() as m:
        expected_params = {'changed_since': '1122334455', 'filter': 'state_cd=NE'}
        m.register_uri('GET', 'https://my.client/page/api/cons/get_updated_constituent_ids',
                       additional_matcher=get_query_parameter_matcher(expected_params))

        result = api_client.cons_getUpdatedConstituentIds(time.time(), {'state_cd': 'NE'})
        assert result.http_status == 200


def test_cons_set_ext_ids(api_client):
    with requests_mock.Mocker() as m:
        m.register_uri('POST', 'https://my.client/page/api/cons/set_ext_ids',
                       additional_matcher=post_query_parameter_matcher({'ext_type': 'someexternal', '12': '34'}))

        result = api_client.cons_setExtIds('someexternal', {12: 34})
        assert result.http_status == 200


def test_cons_delete_constituent_by_id(api_client):
    with requests_mock.Mocker() as m:
        m.register_uri('POST', 'https://my.client/page/api/cons/delete_constituents_by_id',
                       additional_matcher=post_query_parameter_matcher({'cons_ids': '1,3,5'}))

        result = api_client.cons_deleteConstituentsById([1, 3, 5])
        assert result.http_status == 200


def test_cons_get_bulk_constituent_data(api_client):
    with requests_mock.Mocker() as m:
        expected_params = {'format': 'xml', 'fields': 'firstname,lastname', 'cons_ids': '2,4,6',
                           'filter': 'state_cd=VA'}
        m.register_uri('POST', 'https://my.client/page/api/cons/get_bulk_constituent_data',
                       additional_matcher=post_query_parameter_matcher(expected_params))

        result = api_client.cons_getBulkConstituentData('xml', ['firstname', 'lastname'], [2, 4, 6], {'state_cd': 'VA'})
        assert result.http_status == 200


def test_cons_upsert_constituent_data(api_client):
    with requests_mock.Mocker() as m:
        m.register_uri('POST', 'https://my.client/page/api/cons/upsert_constituent_data',
                       additional_matcher=lambda req: req.text == '<?xml blah blah')

        result = api_client.cons_upsertConstituentData('<?xml blah blah')
        assert result.http_status == 200


def match_cons_set_custom_constituent_fields(request):
    query = parse_qs(urlparse(request.url).query)
    return request.text == '<?xml some cons stuff' and '139' in query['cons_id'] and 'False' in query['delete_missing']


def test_cons_set_custom_constituent_fields(api_client):
    with requests_mock.Mocker() as m:
        m.register_uri('POST', 'https://my.client/page/api/cons/set_custom_constituent_fields',
                       additional_matcher=match_cons_set_custom_constituent_fields)

        result = api_client.cons_setCustomConstituentFields('<?xml some cons stuff', 139, False)
        assert result.http_status == 200


def test_cons_get_custom_constituent_fields(api_client):
    """
    Note that this test has no extra query parameters, so it does not need a matcher
    """
    with requests_mock.Mocker() as m:
        m.register_uri('GET', 'https://my.client/page/api/cons/get_custom_constituent_fields')
        result = api_client.cons_getCustomConstituentFields()
        assert result.http_status == 200


def test_cons_merge_constituents_by_id(api_client):
    with requests_mock.Mocker() as m:
        m.register_uri('POST', 'https://my.client/page/api/cons/merge_constituents_by_id',
                       additional_matcher=lambda req: req.text == '12,34,56')

        result = api_client.cons_mergeConstituentsById([12, 34, 56])
        assert result.http_status == 200


def test_cons_merge_constituents_by_email(api_client):
    with requests_mock.Mocker() as m:
        m.register_uri('GET', 'https://my.client/page/api/cons/merge_constituents_by_email',
                       additional_matcher=get_query_parameter_matcher({'email': 'mergeme@client.bsd'}))

        result = api_client.cons_mergeConstituentsByEmail('mergeme@client.bsd')
        assert result.http_status == 200


def test_cons_list_datasets(api_client):
    with requests_mock.Mocker() as m:
        m.register_uri('GET', 'https://my.client/page/api/cons/list_datasets')
        result = api_client.cons_listDatasets()
        assert result.http_status == 200


def test_cons_list_dataset_maps(api_client):
    with requests_mock.Mocker() as m:
        m.register_uri('GET', 'https://my.client/page/api/cons/list_dataset_maps')
        result = api_client.cons_listDatasetMaps()
        assert result.http_status == 200


def test_cons_upload_dataset(api_client):
    with requests_mock.Mocker() as m:
        expected_params = {'slug': 'my-ds', 'map_type': 'csv', 'csv_data': 'a,1,b,2'}
        m.register_uri('POST', 'https://my.client/page/api/cons/upload_dataset',
                       additional_matcher=post_query_parameter_matcher(expected_params))

        result = api_client.cons_uploadDataset('my-ds', 'csv', 'a,1,b,2')
        assert result.http_status == 200


def test_cons_upload_dataset_map(api_client):
    with requests_mock.Mocker() as m:
        m.register_uri('POST', 'https://my.client/page/api/cons/upload_dataset_map',
                       additional_matcher=post_query_parameter_matcher({'csv_data': 'b3,c8'}))

        result = api_client.cons_uploadDatasetMap('b3,c8')
        assert result.http_status == 200


def test_cons_delete_dataset(api_client):
    with requests_mock.Mocker() as m:
        m.register_uri('GET', 'https://my.client/page/api/cons/delete_dataset',
                       additional_matcher=get_query_parameter_matcher({'dataset_id': '8392'}))

        result = api_client.cons_deleteDataset(8392)
        assert result.http_status == 200


def test_cons_delete_dataset_map(api_client):
    with requests_mock.Mocker() as m:
        m.register_uri('GET', 'https://my.client/page/api/cons/delete_dataset_map',
                       additional_matcher=get_query_parameter_matcher({'map_id': '5746'}))

        result = api_client.cons_deleteDatasetMap(5746)
        assert result.http_status == 200


def test_cons_group_list_constituent_groups(api_client):
    with requests_mock.Mocker() as m:
        m.register_uri('GET', 'https://my.client/page/api/cons_group/list_constituent_groups')
        result = api_client.cons_group_listConstituentGroups()
        assert result.http_status == 200


def test_cons_group_get_constituent_groups(api_client):
    with requests_mock.Mocker() as m:
        m.register_uri('GET', 'https://my.client/page/api/cons_group/get_constituent_group',
                       additional_matcher=get_query_parameter_matcher({'cons_group_id': '9876'}))

        result = api_client.cons_group_getConstituentGroup(9876)
        assert result.http_status == 200


def test_cons_group_add_constituent_group(api_client):
    with requests_mock.Mocker() as m:
        m.register_uri('POST', 'https://my.client/page/api/cons_group/add_constituent_groups',
                       additional_matcher=lambda req: req.text == '<?xml add these...')

        result = api_client.cons_group_addConstituentGroup('<?xml add these...')
        assert result.http_status == 200


def test_cons_group_delete_constituent_groups(api_client):
    with requests_mock.Mocker() as m:
        m.register_uri('GET', 'https://my.client/page/api/cons_group/delete_constituent_groups',
                       additional_matcher=get_query_parameter_matcher({'cons_group_ids': '8,3,1'}))

        result = api_client.cons_group_deleteConstituentGroups([8, 3, 1])
        assert result.http_status == 200


def test_cons_group_get_cons_ids_for_group(api_client):
    with requests_mock.Mocker() as m:
        m.register_uri('GET', 'https://my.client/page/api/cons_group/get_cons_ids_for_group',
                       additional_matcher=get_query_parameter_matcher({'cons_group_id': '444'}))

        result = api_client.cons_group_getConsIdsForGroup(444)
        assert result.http_status == 200


def test_cons_group_get_ext_ids_for_group(api_client):
    with requests_mock.Mocker() as m:
        m.register_uri('GET', 'https://my.client/page/api/cons_group/get_ext_ids_for_group',
                       additional_matcher=get_query_parameter_matcher({'cons_group_id': '232323', 'ext_type': 'foo'}))

        result = api_client.cons_group_getExtIdsForGroup(232323, 'foo')
        assert result.http_status == 200


def test_cons_group_set_ext_ids_for_group(api_client):
    with requests_mock.Mocker() as m:
        expected_params = {'cons_group_id': '777', 'ext_type': 'blue', 'ext_ids': '56,100'}
        m.register_uri('POST', 'https://my.client/page/api/cons_group/set_ext_ids_for_group',
                       additional_matcher=post_query_parameter_matcher(expected_params))

        result = api_client.cons_group_setExtIdsForGroup(777, 'blue', [56, 100])
        assert result.http_status == 200


def test_cons_group_add_cons_ids_to_group(api_client):
    with requests_mock.Mocker() as m:
        m.register_uri('POST', 'https://my.client/page/api/cons_group/add_cons_ids_to_group',
                       additional_matcher=post_query_parameter_matcher({'cons_group_id': '9', 'cons_ids': '86,53,21'}))

        result = api_client.cons_group_addConsIdsToGroup(9, [86, 53, 21])
        assert result.http_status == 200


def test_cons_group_set_cons_ids_for_group(api_client):
    with requests_mock.Mocker() as m:
        m.register_uri('POST', 'https://my.client/page/api/cons_group/set_cons_ids_for_group',
                       additional_matcher=post_query_parameter_matcher({'cons_group_id': '842', 'cons_ids': '3,4,55'}))

        result = api_client.cons_group_setConsIdsForGroup(842, [3, 4, 55])
        assert result.http_status == 200


def test_cons_group_add_ext_ids_to_group(api_client):
    with requests_mock.Mocker() as m:
        expected_params = {'cons_group_id': '929', 'ext_type': 'uuid', 'ext_ids': '32,43,54'}
        m.register_uri('POST', 'https://my.client/page/api/cons_group/add_ext_ids_to_group',
                       additional_matcher=post_query_parameter_matcher(expected_params))

        result = api_client.cons_group_addExtIdsToGroup(929, 'uuid', [32, 43, 54])
        assert result.http_status == 200


def test_cons_group_remove_cons_ids_from_group(api_client):
    with requests_mock.Mocker() as m:
        m.register_uri('POST', 'https://my.client/page/api/cons_group/remove_cons_ids_from_group',
                       additional_matcher=post_query_parameter_matcher({'cons_group_id': '101', 'cons_ids': '202,203'}))

        result = api_client.cons_group_removeConsIdsFromGroup(101, [202, 203])
        assert result.http_status == 200


def test_cons_group_remove_ext_ids_from_group(api_client):
    with requests_mock.Mocker() as m:
        expected_params = {'cons_group_id': '838', 'ext_type': 'ssid', 'ext_ids': '34,45'}
        m.register_uri('POST', 'https://my.client/page/api/cons_group/remove_ext_ids_from_group',
                       additional_matcher=post_query_parameter_matcher(expected_params))

        result = api_client.cons_group_removeExtIdsFromGroup(838, 'ssid', [34, 45])
        assert result.http_status == 200


def test_contribution_get_contributions(api_client):
    with requests_mock.Mocker() as m:
        m.register_uri('GET', 'https://my.client/page/api/contribution/get_contributions',
                       additional_matcher=get_query_parameter_matcher({'filter[state_cd]': 'IN'}))

        result = api_client.contribution_getContributions({'state_cd': 'IN'})
        assert result.http_status == 200


def test_event_rsvp_list(api_client):
    with requests_mock.Mocker() as m:
        m.register_uri('POST', 'https://my.client/page/api/event/list_rsvps',
                       additional_matcher=post_query_parameter_matcher({'event_id': '848484'}))

        result = api_client.event_rsvp_list(848484)
        assert result.http_status == 200


def test_mailer_send_triggered_email(api_client):
    with requests_mock.Mocker() as m:
        expected_params = {'mailing_id': '99', 'email': 'me@client.bsd', 'email_opt_in': '1'}
        m.register_uri('GET', 'https://my.client/page/api/mailer/send_triggered_email',
                       additional_matcher=get_query_parameter_matcher(expected_params))

        result = api_client.mailer_sendTriggeredEmail(99, 'me@client.bsd', True)
        assert result.http_status == 200


def test_outreach_get_page_by_id(api_client):
    with requests_mock.Mocker() as m:
        m.register_uri('POST', 'https://my.client/page/api/outreach/get_page_by_id',
                       additional_matcher=post_query_parameter_matcher({'id': '5454'}))

        result = api_client.outreach_getPageById(5454)
        assert result.http_status == 200


def test_outreach_set_page_data(api_client):
    with requests_mock.Mocker() as m:
        m.register_uri('POST', 'https://my.client/page/api/outreach/set_page_data',
                       additional_matcher=lambda req: req.text == '<?xml><some page data/>')

        result = api_client.outreach_setPageData('<?xml><some page data/>')
        assert result.http_status == 200


def test_reference_process_personalization_tag(api_client):
    with requests_mock.Mocker() as m:
        m.register_uri('GET', 'https://my.client/page/api/reference/process_personalization_tag',
                       additional_matcher=get_query_parameter_matcher({'who': 'this-guy'}))

        result = api_client.reference_processPersonalizationTag('this-guy')
        assert result.http_status == 200


def test_signup_process_signup(api_client):
    with requests_mock.Mocker() as m:
        m.register_uri('POST', 'https://my.client/page/api/signup/process_signup',
                       additional_matcher=lambda req: req.text == '<?xml><people/>')

        result = api_client.signup_processSignup('<?xml><people/>')
        assert result.http_status == 200


def test_signup_list_forms(api_client):
    with requests_mock.Mocker() as m:
        m.register_uri('GET', 'https://my.client/page/api/signup/list_forms')

        result = api_client.signup_listForms()
        assert result.http_status == 200


def test_signup_list_form_fields(api_client):
    with requests_mock.Mocker() as m:
        m.register_uri('GET', 'https://my.client/page/api/signup/list_form_fields',
                       additional_matcher=get_query_parameter_matcher({'signup_form_id': '1000'}))

        result = api_client.signup_listFormFields(1000)
        assert result.http_status == 200


def test_signup_signup_count(api_client):
    with requests_mock.Mocker() as m:
        m.register_uri('GET', 'https://my.client/page/api/signup/signup_count',
                       additional_matcher=get_query_parameter_matcher(
                           {'signup_form_id': '50', 'signup_form_field_ids': '2,1'}))

        result = api_client.signup_signupCount(50, [2, 1])
        assert result.http_status == 200


def test_signup_count_by_field(api_client):
    with requests_mock.Mocker() as m:
        m.register_uri('GET', 'https://my.client/page/api/signup/count_by_field',
                       additional_matcher=get_query_parameter_matcher(
                           {'signup_form_id': '52', 'signup_form_field_id': '12'}))

        result = api_client.signup_countByField(52, 12)
        assert result.http_status == 200


def test_wrappers_list_wrappers(api_client):
    with requests_mock.Mocker() as m:
        m.register_uri('GET', 'https://my.client/page/api/wrappers/list_wrappers')

        result = api_client.wrappers_listWrappers()
        assert result.http_status == 200
