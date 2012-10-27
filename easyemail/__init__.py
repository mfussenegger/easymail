#!/usr/bin/env python
# -*- coding: utf-8 -*-

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
        maintype, subtype = self.mimetype.split('/')
        fp = open(self.path, 'rb')
        if maintype == 'image':
            msg = MIMEImage(fp.read(), _subtype=subtype)
        elif maintype == 'audio':
            msg = MIMEAudio(fp.read(), _subtype=subtype)
        else:
            msg = MIMEBase(maintype, subtype)
            msg.set_payload(fp.read())
            encoders.encode_base64(msg)

        fp.close()

        msg.add_header('Content-Disposition',
                       'attachment',
                       filename=self.filename or os.path.basename(self.path))
        return msg


class Email(object):
    def __init__(self, sender, recipients, subject='', body=''):
        self.sender = sender

        if isinstance(recipients, str):
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

    @property
    def subject(self):
        return self._subject

    @subject.setter
    def subject(self, value):
        if isinstance(value, str):
            self._subject = Header(value, 'utf-8')
        else:
            self._subject = value
        assert isinstance(self.subject, Header)

    def as_string(self):
        if self.attachments or self.body_is_html:
            msg = MIMEMultipart()
        else:
            msg = MIMEText(self.body, 'plain')

        msg['Subject'] = self.subject
        msg['From'] = self.sender
        msg['To'] = ', '.join(self.recipients)
        if self.reply_to:
            msg['Reply-To'] = self.reply_to
        msg['Date'] = formatdate(localtime=True)

        if self.body_is_html:
            body = MIMEText(self.body, 'html')
            msg.attach(body)

        if self.attachments:
            for attachment in self.attachments:
                msg.attach(attachment.as_msg())

        result = msg.as_string()
        logger.debug(result)
        return result
