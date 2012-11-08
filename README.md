easymail
========

The email package in pythons standard library is pretty low level.
Easymail aims to add an abstraction layer on top that sets some (hopefully) sane
defaults.

These defaults include:


    * using utf-8 encoding by default. 
    * settings important headers (like Date)


A simple example:

    from easymail import Email
    from smtplib import SMTP
    e = Email('mymail@somedomain.com', 'recipient@otherdomain.org')
    e.subject = 'hello world'
    e.body = 'with some non-äscii charöcters'

    smtp = SMTP('mymailserver.com')
    smtp.sendmail(*e.args)

This is a work in progress. The API is unstable, so best not use this just yet.

You've been warned.

Dependencies
============

Not sure yet. Probably going to require at least Python 3.2

License
=======

Easymail is licensed under the MIT license.
