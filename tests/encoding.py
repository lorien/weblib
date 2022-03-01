# coding: utf-8
from unittest import TestCase

from weblib.encoding import (
    make_str, make_unicode, fix_special_entities
)


class EncodingTestCase(TestCase):
    def test_make_str_from_str(self):
        self.assertEqual(
            make_str(u'фыва'.encode('utf-8')),
            u'фыва'.encode('utf-8'),
        )

    def test_make_str_from_unicode(self):
        self.assertEqual(
            make_str(u'фыва'),
            u'фыва'.encode('utf-8'),
        )

    def test_make_str_from_int(self):
        self.assertEqual(
            make_str(1),
            b'1',
        )

    def test_make_str_from_none(self):
        self.assertEqual(
            make_str(None),
            b'None',
        )

    def test_make_str_cp1251_from_unicode(self):
        self.assertEqual(
            make_str(u'фыва', encoding='cp1251'),
            u'фыва'.encode('cp1251'),
        )

    def test_make_unicode_from_str(self):
        self.assertEqual(
            make_unicode(u'фыва'.encode('utf-8')),
            u'фыва',
        )

    def test_make_unicode_from_unicode(self):
        self.assertEqual(
            make_unicode(u'фыва'),
            u'фыва',
        )

    def test_make_unicode_from_int(self):
        self.assertEqual(
            make_unicode(1),
            u'1',
        )

    def test_make_unicode_from_none(self):
        self.assertEqual(
            make_unicode(None),
            u'None',
        )

    def test_fix_special_entities(self):
        # just test it not fails
        # I forgot what does it do exactly
        fix_special_entities(b'&#128;')
