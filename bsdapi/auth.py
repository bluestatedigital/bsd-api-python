import hmac
import hashlib
from time import time

# Make urllib functions compatible across python 2 and 3 with depending on `Six`
try:
    from urllib.parse import urlparse, urlencode, urlunparse, parse_qsl, unquote_plus
except ImportError:
    from urlparse import urlparse, urlunparse, parse_qsl
    from urllib import urlencode, unquote_plus

from requests.auth import AuthBase


class BsdApiAuth(AuthBase):
    """Generates URL Signing Parameters for the BSD API"""

    def __init__(self, api_id, api_secret):
        self.api_id = api_id
        self.api_secret = api_secret

    def __call__(self, request):
        # break the request URL down into components we can manpulate
        parsed = urlparse(request.url)
        query_parsed = [(p[0], p[1]) for p in parse_qsl(parsed.query)]

        # add required parameters
        api_ts = str(int(time()))

        query_parsed.extend([
            ('api_ver', '2'),  # order matters so we MUST use tuples and not a dict
            ('api_ts', api_ts),
            ('api_id', self.api_id)
        ])
        query_parsed.append(('api_mac', self._generate_api_mac(api_ts, parsed.path, query_parsed)))

        request.url = urlunparse(
            (parsed.scheme, parsed.netloc, parsed.path, parsed.params, urlencode(query_parsed), parsed.fragment)
        )

        # modify and return the request
        return request

    def _generate_api_mac(self, api_ts, api_call, api_params):
        signing_string = "\n".join([
            self.api_id,
            api_ts,
            api_call,
            unquote_plus(urlencode(api_params))
        ])

        return hmac.new(self.api_secret.encode(), signing_string.encode(), hashlib.sha1).hexdigest()
