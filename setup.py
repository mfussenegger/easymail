#!/usr/bin/env python
# -*- coding: utf-8 -*-

from distutils.core import setup


setup(
    name='easymail',
    version='0.1.0',
    author='Mathias Fussenegger',
    author_email='pip@zignar.net',
    url='http://pypi.python.org/pypi/easymail/',
    license='LICENSE.txt',
    description='abstraction layer on top of the email package to make sending\
    emails a little bit easier',
    packages=['easymail'],
    install_requires=[
    ],
    classifiers=[
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
