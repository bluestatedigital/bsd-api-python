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

import logging

class Factory:
    logMap = {
        'debug': logging.DEBUG,
        'info': logging.INFO,
        'error': logging.ERROR,
        'warning': logging.WARNING,
        'critical': logging.CRITICAL
    }

    def create( self, level ):
        try:
            llevel = self.logMap[level.lower()]
        except KeyError:
            llevel = logging.WARNING

        logger = logging.getLogger('pageload')
        logger.setLevel(llevel)
        ch = logging.StreamHandler()
        ch.setLevel(llevel)
        formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(message)s')
        ch.setFormatter(formatter)
        logger.addHandler(ch)
        return logger
