#!/usr/bin/env python
# -*- coding: utf-8 -*-

from easymail import __version__

import os
from distutils.core import setup

if os.path.isfile('README.md'):
    readme = open('README.md').read()
else:
    readme = ''


setup(
    name='easymail',
    version=__version__,
    author='Mathias Fussenegger',
    author_email='pip@zignar.net',
    url='http://pypi.python.org/pypi/easymail/',
    license='MIT',
    description='abstraction layer on top of the email package to make sending\
    emails a little bit easier',
    long_description=readme,
    packages=['easymail'],
    platforms=['any'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: MIT License',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Software Development',
        'Topic :: System :: Networking',
    ],
)
