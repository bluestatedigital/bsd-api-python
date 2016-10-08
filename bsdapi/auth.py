import hmac
import hashlib
from time import time
import urllib
import urlparse
from requests.auth import AuthBase


class BsdApiAuth(AuthBase):
    """Generates URL Signing Parameters for the BSD API"""

    def __init__(self, api_id, api_secret):
        self.api_id = api_id
        self.api_secret = api_secret

    def __call__(self, request):
        # break the request URL down into components we can manpulate
        parsed = urlparse.urlparse(request.url)
        query_parsed = [(p[0], p[1]) for p in urlparse.parse_qsl(parsed.query)]

        # add required parameters
        api_ts = str(int(time()))

        query_parsed.extend([
            ('api_ver', '2'),  # order matters so we MUST use tuples and not a dict
            ('api_ts', api_ts),
            ('api_id', self.api_id)
        ])
        query_parsed.append(('api_mac', self._generate_api_mac(api_ts, parsed.path, query_parsed)))

        request.url = urlparse.urlunparse(
            (parsed.scheme, parsed.netloc, parsed.path, parsed.params, urllib.urlencode(query_parsed), parsed.fragment)
        )

        # modify and return the request
        return request

    def _generate_api_mac(self, api_ts, api_call, api_params):
        signing_string = "\n".join([
            self.api_id,
            api_ts,
            api_call,
            urllib.unquote_plus(urllib.urlencode(api_params))
        ])

        return hmac.new(self.api_secret.encode(), signing_string.encode(), hashlib.sha1).hexdigest()
