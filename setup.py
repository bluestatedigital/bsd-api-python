# Copyright 2016 Blue State Digital
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

# Always prefer setuptools over distutils
from setuptools import setup
from codecs import open
from os import path
from setuptools import find_packages
from setuptools.command.test import test as TestCommand
import sys

# Get the long description from the README file
with open(path.join(path.abspath(path.dirname(__file__)), 'README.md'), encoding='utf-8') as f:
    long_description = f.read()


class PyTest(TestCommand):
    user_options = [('pytest-args=', 'a', "Arguments to pass into pytest")]

    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.pytest_args = '-n auto'

    def run_tests(self):
        import shlex
        import pytest
        errno = pytest.main(shlex.split(self.pytest_args))
        sys.exit(errno)


setup(
    name='bsdapi',
    version='3.0.0a1',
    description=long_description,
    author='Blue State Digital',
    author_email='help@bluestatedigital.com',
    packages=find_packages(exclude=['tests', 'tests.*']),
    license="Apache",
    keywords="API, Client, HTTP",
    url="http://tools.bluestatedigital.com/",
    project_urls={
        'Bug Tracker': 'https://github.com/bluestatedigital/bsd-api-python/issues',
        'Documentation': 'https://stripe.com/docs/api/python',
        'Source Code': 'https://github.com/bluestatedigital/bsd-api-python',
    },
    tests_require=[
        'pytest >= 3.4',
        'pytest-mock >= 1.7',
        'pytest-xdist >= 1.22',
        'pytest-cov >= 2.5',
    ],
    cmdclass={'test': PyTest},
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    install_requires=[
        'requests'
    ],
    extras_require={
        'test': [
            'pytest',
            'coverage'
        ],
        'dev': [
            'twine'
        ]
    },
)
