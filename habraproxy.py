#!/usr/bin/env python
# coding: utf-8
import re
import requests
from bottle import route, run, response, request
from bs4 import BeautifulSoup, Comment, Doctype


SITE_URL = 'https://habr.com/ru/company/yandex/blog/258673/'
HOST = 'localhost'
PORT = 8088


def main():
    run(host=HOST, port=PORT)


@route('/')
@route('/<path:path>')
def index(path=None):
    print request.url
    print request.query.url
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

    # for row in soup.find_all('div'):
        #print row.text
        #print type(row.text)
        # for word in row.text:
        #     print word
    # for a in soup('a'):
    #     href = a.get('href')
    #     if href:
    #         a['href'] = href.replace(SITE_URL, '')
    #
    for a in soup.find_all('a', href=True):
        if 'https://habr.com' in a['href']:
            a['href'] = 'http://localhost:8088/?url='+a['href']

    for tag in soup.find_all(string=lambda s: not isinstance(s, (Comment, Doctype))):
    # for tag in soup.find_all('div'):
    #     print(parent.name)
        if tag.parent.name not in ('style', 'script', 'noscript', 'head', '[document]'):
        #     continue
        # print tag.text
            text = tag.string.strip()
        # print tag.text
        #text = tag.text
            if text is not None:
                #print add_trademark(text)
                try:

                    regex = re.compile(r'\b\w{6}\b', re.UNICODE )
                    # myfile =  'foo"s bar'
                    # myfile2 = regex.sub(lambda m: m.group().replace(r'\b\w{6}\b',"1",1), myfile)

                    newtext = regex.sub(lambda m: m.group()+unicode('™', "utf-8"), text)
                    tag.string.replaceWith(newtext)
                    # matches = re.findall(r'\b\w{6}\b',text, re.MULTILINE)
                    # # print matches
                    # if len(matches)>0:
                    #     # print len(matches)
                    #     # print matches
                    #     newtext = re.sub(r'\b\w{6}\b', 'abc' , text)
                    #     print(newtext)
                    #     tag.string.replaceWith(newtext)
                    #     # print(text2)
                except Exception as e:
                    print e
    return soup.prettify().encode('utf-8')


def add_trademark(text):
    # regex = re.compile(u'(?<=\b)(?<!-)(\w{6})(?!-)(?=\b)', re.UNICODE)
    # print regex.sub(u'\\1™', text)
    # return regex.sub(u'\\1™', text)
    # regex = re.compile('\b\w{6}\b', re.UNICODE)
    # print re.sub('\b\w{6}\b', '1™' , text)
    # return re.sub('\b\w{6}\b', 'abc' , text)
    matches = re.findall(r'\b\w{6}\b',text, re.MULTILINE)
    # print matches
    if len(matches)>0:
        print len(matches)
        print matches
    return re.sub('\b\w{6}\b', 'abc' , text)

# def parse_links():

if __name__ == '__main__':
    main()
