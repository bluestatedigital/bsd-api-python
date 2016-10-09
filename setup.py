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

# Get the long description from the README file
with open(path.join(path.abspath(path.dirname(__file__)), 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

version = "3.0.0"

setup(
    name='bluestatedigital-api',
    version=version,
    description=long_description,
    author='Blue State Digital',
    author_email='help@bluestatedigital.com',
    packages=[
        'bsdapi'
    ],
    package_dir={
        'bsdapi': 'bsdapi'
    },
    license="Apache",
    keywords="API, Client, HTTP",
    url="http://tools.bluestatedigital.com/",
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
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
