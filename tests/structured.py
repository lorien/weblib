# coding: utf-8
from unittest import TestCase

from weblib.etree import parse_html
from weblib.structured import TreeInterface


XML = b'''
    <issue index="2">
        <title>XML today</title>
        <date>12.09.98</date>
        <about>XML</about>
        <home-url>www.j.ru/issues/</home-url>
        <number>448</number>
        <detail>
            <description>

                issue 2
                detail description

            </description>
            <number>445</number>
        </detail>
        <articles>
            <article ID="3">
                <title>Issue overview</title>
                <url>/article1</url>
                <hotkeys>
                    <hotkey>language</hotkey>
                    <hotkey>marckup</hotkey>
                    <hotkey>hypertext</hotkey>
                </hotkeys>
                <article-finished/>
            </article>
            <article>
                <title>Latest reviews</title>
                <url>/article2</url>
                <author ID="3"/>
                <hotkeys>
                    <hotkey/>
                </hotkeys>
            </article>
            <article ID="4">
                <title/>
                <url/>
                <hotkeys/>
            </article>
        </articles>
    </issue>
'''


class StructuredTestCase(TestCase):
    def test_it_works(self):
        tree = parse_html(XML)
        result = TreeInterface(tree).structured_xpath(
            '//issue',
            title='./title/text()',
            date='./date/text()',
            about='./about/text()',
            number=('./number/text()', int),
            home_url='./home-url/text()',
        )
        self.assertEqual(
            result,
            [
                {
                    "date": "12.09.98",
                    "about": "XML",
                    "home_url": "www.j.ru/issues/",
                    "number": 448,
                    "title": "XML today"
                }
            ]
        )

