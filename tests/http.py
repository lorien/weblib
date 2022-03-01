# coding: utf-8
from unittest import TestCase
from six.moves.urllib.parse import quote

from weblib.http import (
    normalize_url, RESERVED_CHARS, normalize_http_values,
    normalize_post_data,
)

class HttpTestCase(TestCase):
    def test_normalize_url_idn(self):
        url = 'http://почта.рф/path?arg=val'
        norm_url = 'http://xn--80a1acny.xn--p1ai/path?arg=val'
        self.assertEqual(norm_url, normalize_url(url))

    def test_normalize_url_unicode_path(self):
        url = u'https://ru.wikipedia.org/wiki/Россия'
        norm_url = 'https://ru.wikipedia.org/wiki'\
                   '/%D0%A0%D0%BE%D1%81%D1%81%D0%B8%D1%8F'
        self.assertEqual(norm_url, normalize_url(url))

    def test_normalize_url_unicode_query(self):
        url = 'https://ru.wikipedia.org/w/index.php?title=Заглавная_страница'
        norm_url = 'https://ru.wikipedia.org/w/index.php'\
                   '?title=%D0%97%D0%B0%D0%B3%D0%BB%D0%B0%D0%B2%D0%BD'\
                   '%D0%B0%D1%8F_%D1%81%D1%82%D1%80'\
                   '%D0%B0%D0%BD%D0%B8%D1%86%D0%B0'
        self.assertEqual(norm_url, normalize_url(url))

    def test_normalize_url_with_mix_of_norm_and_unnorm(self):
        url = 'http://test.com/!?%21'
        norm_url = 'http://test.com/!?%21'
        self.assertEqual(norm_url, normalize_url(url))

    def test_normalize_url_normalized_ascii(self):
        url = 'http://test.com/%21?%21'
        norm_url = 'http://test.com/%21?%21'
        self.assertEqual(norm_url, normalize_url(url))


    def test_normalize_normalized_non_ascii(self):
        url = 'http://www.film.ru/movies/a-z/%D0%9F?%d0%9f'
        norm_url = 'http://www.film.ru/movies/a-z/%D0%9F?%d0%9f'
        self.assertEqual(norm_url, normalize_url(url))

    def test_normalize_non_quoted_percent(self):
        url = 'http://test.com/%9z%21'
        norm_url = 'http://test.com/%9z%21'
        self.assertEqual(norm_url, normalize_url(url))

    def test_quoted_query_in_query(self):
        url = (u"https://graph.facebook.com/fql?q=SELECT%20url%20,total_count"
               u"%20FROM%20link_stat%20WHERE%20url%20in%20('http%3A%2F%2F"
               u"www.ksl.com%2F%3Fsid%3D34840696%26nid%3D148')")
        #norm_url = ("https://graph.facebook.com/fql?q=SELECT%20url%20%2C"
        #            "total_count%20FROM%20link_stat%20WHERE%20url%20in"
        #            "%20%28%27http%3A%2F%2Fwww.ksl.com%2F%3Fsid%3D"
        #            "34840696%26nid%3D148%27%29")
        self.assertEqual(url, normalize_url(url))

    def test_reserved_delims(self):
        path = RESERVED_CHARS.replace('/', '')
        query = RESERVED_CHARS.replace('?', '')
        fragment = RESERVED_CHARS.replace('#', '')
        url = 'http://domain.com/%s?%s#%s' % (path, query, fragment)
        self.assertEqual(url, normalize_url(url))

    def test_normalize_http_values_list(self):
        self.assertEqual(
            normalize_http_values([('foo', ['1', '2'])]),
            [(b'foo', b'1'), (b'foo', b'2')]
        )

    def test_normalize_http_values_scalar_and_list(self):
        self.assertEqual(
            normalize_http_values([('foo', '3'), ('foo', ['1', '2'])]),
            [(b'foo', b'3'), (b'foo', b'1'), (b'foo', b'2')]
        )

    def test_normalize_http_values_none(self):
        self.assertEqual(
            normalize_http_values([('foo', None)]),
            [(b'foo', b'')]
        )

    def test_normalize_http_values_number(self):
        self.assertEqual(
            normalize_http_values([('foo', 13)]),
            [(b'foo', b'13')]
        )

    def test_normalize_http_values_unicode(self):
        self.assertEqual(
            normalize_http_values([('foo', u'фыва')]),
            [(b'foo', u'фыва'.encode('utf-8'))]
        )

    def test_normalize_http_values_object(self):
        class Foo(object):
            def __str__(self):
                return 'I am foo'

        self.assertEqual(
            normalize_http_values([('foo', Foo())]),
            [(b'foo', b'I am foo')]
        )

    def test_normalize_http_values_ignore_classes_list(self):
        class Foo(object):
            def __str__(self):
                return 'I am foo'

        class Bar(object):
            pass

        bar = Bar()
        self.assertEqual(
            normalize_http_values(
                [('foo', Foo()), ('bar', bar)],
                ignore_classes=[Bar],
            ),
            [(b'foo', b'I am foo'), (b'bar', bar)]
        )

    def test_normalize_http_values_ignore_classes_scalar(self):
        class Foo(object):
            def __str__(self):
                return 'I am foo'

        class Bar(object):
            pass

        bar = Bar()
        self.assertEqual(
            normalize_http_values(
                [('foo', Foo()), ('bar', bar)],
                ignore_classes=Bar,
            ),
            [(b'foo', b'I am foo'), (b'bar', bar)]
        )

    def test_normalize_post_data_str(self):
        self.assertEqual(
            normalize_post_data(u'фыва'),
            u'фыва'.encode('utf-8'),
        )

    def test_normalize_post_data_bytes(self):
        self.assertEqual(
            normalize_post_data(u'фыва'.encode('utf-8')),
            u'фыва'.encode('utf-8'),
        )

    def test_normalize_post_data_non_text(self):
        self.assertEqual(
            normalize_post_data([('bar', 1), ('bar', [3, 4])]),
            b'bar=1&bar=3&bar=4',
        )

    def test_deprecated_normalize_unicode(self):
        # weblib.http.normalize_unicode is required by grab release
        from weblib.http import normalize_unicode
        self.assertEqual(
            normalize_unicode(u'фыва'),
            u'фыва'.encode('utf-8')
        )
        self.assertEqual(
            normalize_unicode(u'фыва'.encode('utf-8')),
            u'фыва'.encode('utf-8')
        )
        self.assertEqual(normalize_unicode(1), b'1')
