import hmac, hashlib, unittest
from time import time

try:
    import urllib.parse
except ImportError:
    import urllib

from bsdapi.URL import URL

class RequestGenerator:

    def __init__(self, api_id, api_secret, api_host, https = False):
        self.__dict__.update(locals())
        self.api_base   = '/page/api'

    def _query_str(self, api_params, quote=False):
        if quote:
            try:
                urlQuoteFunc = urllib.parse.quote
            except AttributeError:
                urlQuoteFunc = urllib.quote
        else:
            urlQuoteFunc = lambda x: x

        return '&'.join(["%s=%s" % (k, urlQuoteFunc(v)) for k, v in api_params])

    def _signing_string(self, api_ts, api_call, api_params):
        string = "\n".join([
            self.api_id,
            api_ts,
            self.api_base + api_call,
            self._query_str(api_params, quote=False)
        ])
        return hmac.new(self.api_secret.encode(), string.encode(), hashlib.sha1).hexdigest()

    def getUrl(self, api_call, api_params = []):
        api_ts = str(int(time()))

        #Set defaults
        api_params.setdefault('api_ver', '1')
        api_params.setdefault('api_id', self.api_id)
        api_params.setdefault('api_ts', api_ts)

        params = sorted(api_params.items())

        params.append(('api_mac', self._signing_string(api_ts, api_call, params)))

        protocol = 'https' if self.https else 'http'
        query = self._query_str(params, quote=True)
        return URL(protocol=protocol, host=self.api_host, path=self.api_base + api_call, query=query)

class TestRequestGenerator(unittest.TestCase):

    def setUp(self):
        self.host = 'enoch.bluestatedigital.com:17260'
        self.secret = '7405d35963605dc36702c06314df85db7349613f'
        self.api_id = 'sfrazer'

    def test_hmacGenerateProperlyWhenAPIHasNoParams(self):
        request = RequestGenerator(self.api_id, self.secret, self.host)
        signing_string = request._signing_string('1272659462', '/circle/list_circles', [])
        self.assertEqual(signing_string, '13e9de81bbdda506b6021579da86d3b6edea9755')

    def test_hmacGenerateProperlyWhenAPIHasParams(self):
        request = RequestGenerator(self.api_id, self.secret, self.host)
        params = [('cons_ids', '1,2,3,4,5')]
        signing_string = request._signing_string('1272662274', '/cons/get_constituents_by_id', params)
        self.assertEqual(signing_string, 'c2af877085bcb5390aed0c8256b14ad05f2e3ef1')

if __name__ == '__main__':
    unittest.main()
