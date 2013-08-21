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

import argparse, logging, sys, readline, atexit, os, rlcompleter
from code import InteractiveConsole

try:
    import configparser
except ImportError:
    import ConfigParser as configparser

from bsdapi.URL import URL
from bsdapi.RequestGenerator import RequestGenerator
from bsdapi.ApiResult import ApiResultPrettyPrintable
from bsdapi.ApiResult import FactoryFactory as ApiResultFactoryFactory
from bsdapi.BsdApi import Factory as BsdApiFactory
from bsdapi.Logger import Factory as LoggerFactory
from bsdapi.Styler import Factory as StylerFactory

class Console(InteractiveConsole):
    def __init__(self, localVars=None, filename="<console>", histfile=os.path.expanduser("~/.bsdapi_history")):
        InteractiveConsole.__init__(self, localVars, filename)
        self.initHistory(histfile)

    def initHistory(self, histfile):
        readline.parse_and_bind("tab: complete")
        if hasattr(readline, "read_history_file"):
            try:
                readline.read_history_file(histfile)
            except IOError:
                pass
            atexit.register(self.saveHistory, histfile)

    def saveHistory(self, histfile):
        readline.write_history_file(histfile)

    def run(self):
        sys.ps1 = 'api> '
        self.interact('Blue State Digital API Client')

def Cli():
    ver = sys.version_info

    if ver.major < 2 or (ver.major == 3 and ver.minor < 2) or (ver.major == 2 and ver.minor < 7):
        print("Python 2.7+ required. %d.%d.%d installed" %(ver.major, ver.minor, ver.micro))
        sys.exit(-1)

    parser = argparse.ArgumentParser(
        description = 'Blue State Digital API Client',
        epilog = '(c) 2011 Blue State Digital')

    parser.add_argument('config',
        nargs = 1,
        metavar = 'CONFIG',
        help='Configuration file')

    parser.add_argument('-L', '--log-level',
        default = 'warning',
        help = "'debug', 'error', 'warning', 'info', or 'critical'")

    parser.add_argument('-c', '--color',
        action = 'store_true',
        default = False,
        help = 'Display with ANSI terminal colors.')

    parser.add_argument('-v', '--verbose',
        action = 'store_true',
        default = False,
        help = 'Show verbose output.')

    cli = parser.parse_args()
    logger = LoggerFactory().create(cli.log_level)
    logger.debug( 'CLI: %s' % (cli) )

    if not os.path.exists(cli.config[0]):
        logger.error("Error: configuration file %s does not exist." % (cli.config[0]))
        sys.exit(1)

    config = configparser.RawConfigParser()
    config.read(cli.config[0])

    settings = {
        'basic' : {
            'host': 'localhost',
            'port': '80',
            'secure_port': '443'
        }
    }

    for key, value in config.items('basic'):
        settings['basic'][key] = value

    logger.debug( 'Settings: %s' % (settings) )

    apiFactory = BsdApiFactory()
    api = apiFactory.create(
        id = settings['basic']['api_id'], \
        secret = settings['basic']['secret'], \
        host = settings['basic']['host'], \
        port = settings['basic']['port'], \
        securePort = settings['basic']['secure_port'],
        colorize = cli.color
    )

    console = Console({
        'api': api,
        'settings': settings
    })

    console.run()
