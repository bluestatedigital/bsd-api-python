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

import unittest

try:
    import urllib.parse
except ImportError:
    import urllib

class URL:

    def __init__(self, protocol = 'http', host = 'localhost', path = '/', query = None):
        self.__dict__.update(locals())
        try:
            urlEncodeFunc = urllib.urlencode
        except AttributeError:
            urlEncodeFunc = urllib.parse.urlencode

        if isinstance(self.query, dict):
            self.query = urlEncodeFunc(self.query)
        if self.path[0] != '/':
            self.path = '/' + self.path

    def __str__(self):
        url = self.protocol + '://' + self.host + self.path
        if self.query and len(self.query):
            url = url + '?' + self.query
        return url

    def getPathAndQuery(self):
        url = self.path
        if self.query and len(self.query):
            url = url + '?' + self.query
        return url

class TestSequenceFunctions(unittest.TestCase):

    def setUp(self):
        self.host = 'enoch.bluestatedigital.com:17260'

    def test_GenerateProperURLWithAllElements(self):
        url = URL(host='test.com', path='/a/b/c', query='a=1&b=2')
        self.assertEqual(str(url), 'http://test.com/a/b/c?a=1&b=2')

    def test_GenerateProperURLWithMissingProtocol(self):
        url = URL(host='test.com', path='/a/b/c', query='a=1&b=2')
        self.assertEqual(str(url), 'http://test.com/a/b/c?a=1&b=2')

    def test_GenerateProperURLWithMissingHost(self):
        url = URL(path='/a/b/c', query='a=1&b=2')
        self.assertEqual(str(url), 'http://localhost/a/b/c?a=1&b=2')
    
    def test_GenerateProperURLWithQueryHash(self):
        url = URL(path='/a/b/c', query={'a': 1, 'b': 2})
        self.assertEqual(str(url), 'http://localhost/a/b/c?a=1&b=2')

    def test_GenerateProperURLWithMissingPath(self):
        url = URL(query={'a': 1, 'b': 2})
        self.assertEqual(str(url), 'http://localhost/?a=1&b=2')
    
    def test_GenerateProperURLWhenPathDoesntStartWithASlash(self):
        url = URL(path='/a/b/c', query={'a': 1, 'b': 2})
        self.assertEqual(str(url), 'http://localhost/a/b/c?a=1&b=2')

    def test_GenerateProperURLWhenAllParamsArentSet(self):
        url = URL()
        self.assertEqual(str(url), 'http://localhost/')

if __name__ == '__main__':
    unittest.main()
