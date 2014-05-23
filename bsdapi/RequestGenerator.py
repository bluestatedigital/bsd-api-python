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

    def getUrl(self, api_call, api_params = None):
        if api_params is None: api_params = {}

        api_ts = str(int(time()))

        # Set defaults
        api_params.setdefault('api_ver', '2')
        api_params.setdefault('api_id', self.api_id)
        api_params.setdefault('api_ts', api_ts)

        params = sorted(api_params.items())
        params.append(('api_mac', self._signing_string(api_ts, api_call, params)))

        protocol = 'https' if self.https else 'http'
        query = self._query_str(params, quote=True)
        return URL(protocol=protocol, host=self.api_host, path=self.api_base + api_call, query=query)
