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

class Factory:
    def create(self, ansiColors = True):
        if ansiColors:
            colorizer = AnsiColorizer()
        else:
            colorizer = NullColorizer()
        return Styler(colorizer)

class Styler:
    def __init__(self, colorizer):
        self.__dict__.update(locals())
    def color(self, string, color):
        return self.colorizer.color(string, color)

class Colorizer:
    def color(self, string, color):
        raise Exception('Not implemented')

class NullColorizer:
    def color(self, string, color):
        return string

class AnsiColorizer:
    def __init__(self):
        self.colors = {
            'purple': '\033[95m',
            'blue': '\033[94m',
            'green': '\033[92m',
            'yellow': '\033[93m',
            'red': '\033[91m',
        }
        self.endc = '\033[0m'

    def color(self, string, color):
        return "%s%s%s" % (self.colors[color], string, self.endc)
