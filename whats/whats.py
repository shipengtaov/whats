#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import sys
from argparse import ArgumentParser
import re
import random

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

USER_AGENTS = (
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.7; rv:11.0) Gecko/20100101 Firefox/11.0',
    'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:22.0) Gecko/20100 101 Firefox/22.0',
    'Mozilla/5.0 (Windows NT 6.1; rv:11.0) Gecko/20100101 Firefox/11.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_4) AppleWebKit/536.5 (KHTML, like Gecko)'
        'Chrome/19.0.1084.46 Safari/536.5',
    'Mozilla/5.0 (Windows; Windows NT 6.1) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.46'
        'Safari/536.5',
)
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
    search_response = requests.get(
                        search_url,
                        headers={'User-Agent': random.choice(USER_AGENTS)},
                        timeout=15)
    if not search_response.ok:
        raise SystemExit('response error from url: {}, status_code: {}'.format(
                search_url,
                search_response.status_code))

    first_link = _get_first_link(search_response)
    first_link = urljoin(search_url, first_link)
    answer_response = requests.get(
                        first_link,
                        headers={'User-Agent': random.choice(USER_AGENTS)},
                        timeout=15)
    if not answer_response.ok:
        raise SystemExit('response error from url: {}, status_code: {}'.format(
                first_link,
                answer_response.status_code))

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
