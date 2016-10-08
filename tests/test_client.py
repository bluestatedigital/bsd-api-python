from bsdapi import BsdApiClient


def test_client_sets_constructor_attributes():
    client = BsdApiClient('https://foo.bar', 'abc', '123')

    assert client.api_id == 'abc'
    assert client.api_secret == '123'
    assert client.base_url == 'https://foo.bar'


def test_client_handles_extra_slashes():
    client_a = BsdApiClient('https://foo.bar', 'abc', '123')
    client_b = BsdApiClient('https://foo.bar/', 'abc', '123')

    assert client_a.base_url == client_b.base_url
