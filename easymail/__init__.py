#!/usr/bin/env python
# -*- coding: utf-8 -*-

__version__ = '0.1.0'
__all__ = ['Attachment', 'Email']

"""
easymail

an abstraction layer on top of the standard email package.
It aims to hide all the troublesome mime stuff and sets some sane defaults.
All to make your life a little bit easier and make sending emails easier.

>>> e = Email('sender@foo.com', 'recipient@foo.com')
>>> e.subject = 'urgent!!!1'
>>> e.body = 'this is very important.'
>>> e.attachments.append(Attachment('/path/to/audiofile.ogg'))

>>> e.sender
'sender@foo.com'
>>> str(e.subject)
'urgent!!!1'
>>> e.recipients
['recipient@foo.com']
"""

import os
import logging
from mimetypes import guess_type
from email import encoders
from email.header import Header
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formatdate
logger = logging.getLogger('easyemail')

try:
    unicode
except NameError:
    # Python3
    basestring = unicode = str


class Attachment(object):
    def __init__(self, path, mimetype=None, filename=None):
        """create an attachment

        path: path to the file on disk
        mimetype: (optional, will be guessed by fileextension
        filename: filename in the email, if None the name from path will be used
        """
        self.path = path
        self.mimetype = mimetype or guess_type(path)[0] or 'application/octet-stream'
        self.filename = filename

    def as_msg(self):
        """return the mime msg.

        the results concrete type depends on the attachments mimetype.
        """
        maintype, subtype = self.mimetype.split('/')
        with open(self.path, 'rb') as fp:
            if maintype == 'image':
                msg = MIMEImage(fp.read(), _subtype=subtype)
            elif maintype == 'audio':
                msg = MIMEAudio(fp.read(), _subtype=subtype)
            else:
                msg = MIMEBase(maintype, subtype)
                msg.set_payload(fp.read())
                encoders.encode_base64(msg)

        msg.add_header('Content-Disposition',
                       'attachment',
                       filename=self.filename or os.path.basename(self.path))
        return msg


class Email(object):
    def __init__(self, sender, recipients, subject='', body=''):
        self.sender = sender

        if isinstance(recipients, basestring):
            self.recipients = [recipients]
        else:
            self.recipients = recipients

        self.subject = subject
        self.attachments = []
        self.reply_to = ''
        self.cc = []
        self.bcc = []
        self.body = body
        self.body_is_html = False

    def __repr__(self):
        return '<Email>'

    def __str__(self):
        return self.get_msg()

    @property
    def all_recipients(self):
        """recipients including cc and bcc"""
        return self.recipients + self.cc + self.bcc

    @property
    def subject(self):
        return unicode(self._subject)

    @subject.setter
    def subject(self, value):
        if isinstance(value, basestring):
            self._subject = Header(value, 'utf-8')
        else:
            self._subject = value
        assert isinstance(self._subject, Header)

    @property
    def args(self):
        return (self.sender, self.all_recipients, self.get_msg())

    def get_msg(self):
        # python 3.3 doesn't like the utf-8 charset if the body is empty.
        charset = self.body != '' and 'utf-8' or 'us-ascii'

        if self.attachments or self.body_is_html:
            msg = MIMEMultipart()
        else:
            msg = MIMEText(self.body, _charset=charset)

        msg['Subject'] = self._subject
        msg['From'] = self.sender
        msg['To'] = ', '.join(self.recipients)
        if self.reply_to:
            msg['Reply-To'] = self.reply_to
        msg['Date'] = formatdate(localtime=True)

        if self.body_is_html:
            body = MIMEText(self.body, 'html', charset)
            msg.attach(body)

        if self.attachments:
            if not self.body_is_html:
                msg.attach(MIMEText(self.body, _charset=charset))

            for attachment in self.attachments:
                msg.attach(attachment.as_msg())

        result = str(msg)
        logger.debug(result)
        return result
