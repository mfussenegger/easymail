#!/usr/bin/env python
# -*- coding: utf-8 -*-

from email.header import decode_header, Header
from email.mime.audio import MIMEAudio
from email.mime.image import MIMEImage
from easyemail import Email, Attachment
from unittest import TestCase


class TestAttachment(TestCase):
    def test_images(self):
        a = Attachment('./tests/test.png')
        self.assertTrue('image/png' in str(a.as_msg()))
        self.assertIsInstance(a.as_msg(), MIMEImage)

    def test_audio(self):
        a = Attachment('./tests/440Hz-5sec.mp3')
        self.assertTrue('audio/mpeg' in str(a.as_msg()))
        self.assertIsInstance(a.as_msg(), MIMEAudio)


class TestEmail(TestCase):
    def test_subject_encoding(self):
        e = Email('sender@foo.com', 'recipient@foo.com', 'subject', 'body')
        self.assertEqual('subject', str(e.subject))
        self.assertEqual('utf-8', decode_header(e.subject)[0][1])
        self.assertIsInstance(e.subject, Header)
        self.assertEqual('body', e.body)

    def test_subject_property(self):
        e = Email('sender@foo.com', 'recipient@foo.com')
        e.subject = 'subject'
        self.assertEqual('subject', str(e.subject))
        self.assertEqual('utf-8', decode_header(e.subject)[0][1])
        self.assertIsInstance(e.subject, Header)

    def test_recipients(self):
        e = Email('sender@foo.com', 'recipient1@foo.com')
        self.assertEqual(e.recipients, ['recipient1@foo.com'])

        recipients = ['recipient1@foo.com', 'recipient2@foo.com']
        e = Email('sender@foo.com', recipients)
        self.assertEqual(e.recipients, recipients)

    def test_as_string(self):
        e = Email('sender@foo.com', 'recipient@foo.com')
        e.subject = 'foo'
        #self.assertEqual('foo', e.as_string())
