from bsdapi import BsdApiAuth
from requests import Request
import urlparse


def test_auth_properties():
    auth = BsdApiAuth('abc', '123')

    assert auth.api_id == 'abc'
    assert auth.api_secret == '123'


def test_auth_adds_expected_parameters():
    r = Request(
        method='GET',
        url='https://foo.bar/',
        params={'baz': 'qux'},
        auth=BsdApiAuth('abc', '123')
    )

    # check that only the parameters we explicitly placed there are in the request
    assert r.params['baz'] == 'qux'
    assert 'api_mac' not in r.params

    p = r.prepare()
    query_params = {p[0]: p[1] for p in urlparse.parse_qsl(urlparse.urlparse(p.url).query)}

    # check that the auth method has added the correct parameters to the response
    assert 'api_mac' in query_params
    assert 'api_ts' in query_params
    assert query_params['api_ver'] == '2'
