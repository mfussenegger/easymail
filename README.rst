========
easymail
========

.. image:: https://travis-ci.org/mfussenegger/easymail.svg?branch=master
    :target: https://travis-ci.org/mfussenegger/easymail
    :alt: travis-ci

.. image:: https://img.shields.io/pypi/wheel/easymail.svg
    :target: https://pypi.python.org/pypi/easymail/
    :alt: Wheel

.. image:: https://img.shields.io/pypi/v/easymail.svg
   :target: https://pypi.python.org/pypi/easymail/
   :alt: PyPI Version

.. image:: https://img.shields.io/pypi/pyversions/easymail.svg
   :target: https://pypi.python.org/pypi/easymail/
   :alt: Python Version

The email package in pythons standard library is pretty low level.
Easymail aims to add an abstraction layer on top that sets some (hopefully) sane
defaults.

These defaults include:

- using utf-8 encoding by default. 
- important headers (like Date)


A simple example::

    from easymail import Email
    from smtplib import SMTP
    e = Email('My Name <mymail@somedomain.com>', 'recipient@otherdomain.org')
    e.subject = 'hello world'
    e.body = 'with some non-äscii charöcters'

    smtp = SMTP('mymailserver.com')
    smtp.sendmail(*e.args)

Slightly more advanced::

    from easymail import Email, Attachment
    from smtplib import SMTP
    e = Email('My Name <mymail@somedomain.com>', 'recipient@otherdomain.org')
    e.subject = 'hello world'
    e.body = 'with some non-äscii charöcters'

    e.attachments.append(Attachment('./path/to/picture.png'))
    e.attachments.append(Attachment('./path/to/document.pdf'))

    smtp = SMTP('mymailserver.com')
    smtp.sendmail(*e.args)


Dependencies
============

Pure Python 3.5+
