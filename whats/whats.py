#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import sys
from argparse import ArgumentParser
import re

from . import __version__

if sys.version_info.major < 3:
    from urllib import quote as url_quote
    from urlparse import urljoin
    def force_text(string):
        if not isinstance(string, (str, unicode)):
            return unicode(string)
        if not isinstance(string, unicode):
            return string.decode('utf-8')
        return string
else:
    from urllib.parse import quote as url_quote
    from urllib.parse import urljoin
    def force_text(string):
        if not isinstance(string, (str, bytes)):
            return str(string)
        if not isinstance(string, str):
            return string.decode('utf-8')
        return string

import requests
from readability import Document
from lxml import html

SEARCH_URLS = dict(
    google='https://www.google.com/search?q={0}',
)


def _get_first_link(response):
    doc = html.fromstring(response.text)
    doc.xpath('//*[@class="l"]')
    links = ([a.attrib['href'] for a in doc.xpath('//*[@class="l"]')] or
             [a.attrib['href'] for a in doc.xpath('//*[@class="r"]/a')])
    return links[0] if links else None


def tellme(word):
    search_url = SEARCH_URLS['google'].format(url_quote(word.encode('utf-8')))
    search_response = requests.get(search_url, timeout=15)
    assert search_response.status_code == 200

    first_link = _get_first_link(search_response)
    first_link = urljoin(search_url, first_link)
    answer_response = requests.get(first_link, timeout=15)
    assert answer_response.status_code == 200

    doc = Document(answer_response.text)
    answer = doc.summary()
    if answer:
        answer = html.fromstring(answer).xpath('//body')[0].text_content().strip()
        answer = re.sub(r'\n{3,}', '\n\n', answer)
    else:
        pass
    return answer


def main():
    parser = ArgumentParser()
    parser.add_argument('word', nargs='?', help='what do you want to know?')
    parser.add_argument('-v', '--version', action='store_true', help='show current version')
    args = parser.parse_args()

    if args.version:
        print("whats {}".format(__version__))
        return

    if args.word:
        print(tellme(force_text(args.word)))
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
