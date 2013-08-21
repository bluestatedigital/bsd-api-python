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

class Filters:

    def __init__(self, filters):
        self.filters = filters

    def getQuery(self):
        return self._collapse()

    def _collapse(self):
        filters = {}
        for key, value in self.filters.items():
            if key not in ['state_cd', 'primary_state_cd', 'is_subscribed', 'has_account', 'signup_form_id', 'email']:
                raise FilterError('Incorrect filter parameter')
            elif key == 'state_cd' and type(value).__name__ == 'list' and len(value) > 1:
                filters[key] = "(%s)" % (','.join(value))
            elif key == 'state_cd' and type(value).__name__ == 'list' and len(value) == 1:
                filters[key] = value[0]
            elif key == 'state_cd' and type(value).__name__ == 'str':
                filters[key] = value
            elif key in ['is_subscribed', 'has_account'] and value == True:
                filters[key] = True
            elif key in ['is_subscribed', 'has_account'] and value == False:
                continue
            elif key == 'primary_state_cd' and type(value).__name__ == 'str':
                filters[key] = value
            elif key == 'signup_form_id':
                filters[key] = str(value)
            elif key == 'email':
                filters[key] = str(value)
            else:
                raise FilterError('Incorrect Filter parameters')

        return filters

    def __str__(self):
        filters = self._collapse()
        return ','.join(["%s%s" % (k, ('=' + v) if v != True else '') for k, v in filters.items()])
