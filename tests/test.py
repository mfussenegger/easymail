#!/usr/bin/env python
# -*- coding: utf-8 -*-

from email.header import decode_header, Header
from email.mime.audio import MIMEAudio
from email.mime.image import MIMEImage
from easymail import Email, Attachment
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

    def test_filename_in_header(self):
        a = Attachment('./tests/440Hz-5sec.mp3')
        msg = str(a.as_msg())
        self.assertTrue('attachment; filename="440Hz-5sec.mp3' in msg[:200])

    def test_msg_contains_body_and_attachment(self):
        e = Email('sender@foo.com', 'recipient@foo.com', 'subject', 'fubar')
        e.attachments.append(Attachment('./tests/440Hz-5sec.mp3'))

        # body will be base64 encoded:
        self.assertTrue('ZnViYXI=' in str(e)[:500])
        self.assertTrue('filename="440Hz' in str(e)[:800])

    def test_msg_contains_html_body_and_attachment(self):
        e = Email('sender@foo.com', 'recipient@foo.com', 'subject')
        e.body = '<html><body><b>fubar</b></body></html>'
        e.body_is_html = True
        e.attachments.append(Attachment('./tests/440Hz-5sec.mp3'))

        # body will be base64 encoded:
        self.assertTrue('PGh0bWw+PGJvZHk+PGI+ZnViYXI8L2I+PC9ib2R5PjwvaHRtbD4='
                        in str(e)[:500])
        self.assertTrue('filename="440Hz' in str(e)[:800])


class TestEmail(TestCase):
    def test_subject_encoding(self):
        e = Email('sender@foo.com', 'recipient@foo.com', 'subject', 'body')
        self.assertEqual('subject', str(e.subject))
        self.assertEqual('utf-8', decode_header(e._subject)[0][1])
        self.assertIsInstance(e._subject, Header)
        self.assertEqual('body', e.body)

    def test_subject_property(self):
        e = Email('sender@foo.com', 'recipient@foo.com')
        e.subject = 'subject'
        self.assertEqual('subject', str(e.subject))
        self.assertEqual('utf-8', decode_header(e._subject)[0][1])
        self.assertIsInstance(e._subject, Header)

    def test_recipients(self):
        e = Email('sender@foo.com', 'recipient1@foo.com')
        self.assertEqual(e.recipients, ['recipient1@foo.com'])

        recipients = ['recipient1@foo.com', 'recipient2@foo.com']
        e = Email('sender@foo.com', recipients)
        self.assertEqual(e.recipients, recipients)

    def test_as_string(self):
        e = Email('sender@foo.com', 'recipient@foo.com')
        e.subject = 'äää ööö üfoo äß'
        e.body = 'ääää'
        self.assertTrue('Content-Type: text/plain; charset="utf-8"' in str(e))

    def test_as_string_empty_body(self):
        e = Email('sender@foo.com', 'recipient@foo.com')
        e.subject = 'äää ööö üfoo äß'
        self.assertTrue('Content-Type: text/plain; charset="us-ascii"' in str(e))

    def test_all_recipients(self):
        e = Email('sender@foo.com', 'recipient@foo.com')
        e.cc.append('cc@foo.com')
        e.bcc.append('bcc@foo.com')
        self.assertEqual(e.all_recipients, ['recipient@foo.com',
                                            'cc@foo.com',
                                            'bcc@foo.com'])
