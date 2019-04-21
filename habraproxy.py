#!/usr/bin/env python
# coding: utf-8
import re
import requests
from bottle import route, run, response, request
from bs4 import BeautifulSoup, Comment, Doctype


SITE_URL = 'https://habrahabr.ru'
HOST = 'localhost'
PORT = 8088


def main():
    run(host=HOST, port=PORT)


@route('/')
@route('/<path:path>')
def index(path=None):
    if request.query.url:
        url = request.query.url
    else:
        url = '%s/%s' % (SITE_URL, path) if path else SITE_URL
    r = requests.get(url)
    content = r.content
    content_type = r.headers['content-type']
    response.content_type = content_type

    if 'text/html' in content_type:
        content = parse(content)
    return content


def parse(content):
    soup = BeautifulSoup(content, "lxml")
    for a in soup.find_all('a', href=True):
        if 'https://habr.com' in a['href']:
            a['href'] = 'http://localhost:8088/?url='+a['href']

    for tag in soup.find_all(string=lambda s: not isinstance(s, (Comment, Doctype))):
        if tag.parent.name not in ('style', 'script', 'noscript', 'head', '[document]'):
            text = tag.string.strip()
            if text:
                tag.string.replace_with(add_trademark(text))
        else:
            continue
    return soup.prettify().encode('utf-8')


def add_trademark(text):
    regex = re.compile(r'\b\w{6}\b', re.UNICODE )
    return regex.sub(lambda m: m.group()+unicode('™', "utf-8"), text)


if __name__ == '__main__':
    main()
