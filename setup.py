#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup


try:
    with open('README.md', encoding='utf-8') as f:
        readme = f.read()
except IOError:
    readme = ''


setup(
    name='easymail',
    author='Mathias Fussenegger',
    author_email='pip@zignar.net',
    url='https://github.com/mfussenegger/easymail',
    license='MIT',
    description='abstraction layer on top of the email package to make sending\
    emails a little bit easier',
    long_description=readme,
    py_modules=['easymail'],
    platforms=['any'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.5',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: MIT License',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Software Development',
        'Topic :: System :: Networking',
    ],
    use_scm_version=True,
    setup_requires=['setuptools_scm']
)
