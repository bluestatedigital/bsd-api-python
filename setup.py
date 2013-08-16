import os
from setuptools import setup, find_packages

version = '2'
README = os.path.join(os.path.dirname(__file__), 'README')
long_description = 'Command line client for making API calls.'

setup(
    name='bsdapi',
    version=version,
    description=long_description,
    author='Blue State Digital',
    author_email='help@bluestatedigital.com',
    packages=['bsdapi'],
    package_dir={'bsdapi': 'bsdapi'},
    entry_points={
      'console_scripts': [
            'bsdapi = bsdapi.Main:Cli'
        ]
      },
    license = "Apache",
    keywords = "API, Client, HTTP",
    url = "http://tools.bluestatedigital.com/",
    classifiers=[
          "Programming Language :: Python",
          "Development Status :: 4 - Beta",
          "Intended Audience :: Developers",
          "Natural Language :: English",
      ]
    )
