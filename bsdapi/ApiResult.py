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

import json

class ApiResultPrettyPrintable:
    def __init__(self, styler):
        self.__dict__.update(locals())

    def toString(self, apiResult):
        if apiResult.http_status == 200:
            color = 'green'
        elif apiResult.http_status == 202:
            color = 'yellow'
        else:
            color = 'red'

        status_str = "%s %s %s" % (apiResult.http_version, str(apiResult.http_status), apiResult.http_reason)
        headers_str = '\n'.join(['%s: %s' % (k, v) for k, v in apiResult.headers]) + '\n'

        ''' assume json response body and try to prettyprint, just print plain
        response if fail'''
        try:
            body_str = json.dumps(json.loads(apiResult.body), sort_keys=True, indent=4) 
        except:
            body_str = apiResult.body

        full_str = "%s\n%s\n%s" % (self.styler.color(status_str, color),
                self.styler.color(headers_str, 'purple'),
                body_str)
        return full_str.strip()

class ApiResult:
    def __init__(self, request_url, http_response, headers, body, stringizer = None):
        self.s=http_response
        self.http_status  = http_response.status
        self.http_reason  = http_response.reason
        self.http_version = ('HTTP/1.0' if http_response.version == 10 else 'HTTP/1.1')
        self.__dict__.update(locals())
    def __str__(self):
        if self.stringizer:
            return self.stringizer.toString(self)
        return repr(self)

class Factory:
    def __init__(self, stringizer):
        self.__dict__.update(locals())
    def create(self, url_secure, response, headers, body):
        return ApiResult(url_secure, response, headers, body, self.stringizer)

class FactoryFactory:
    def create(self, stringizer = None):
        return Factory(stringizer)       
