#!/usr/bin/env python

from json import loads
from support import SpoofOpen
from collections import namedtuple
import logging

UPLOAD = namedtuple('Upload', 'id url md5 ext')
SPOOF = SpoofOpen()

LIST_BASE = 'https://e621.net/post/index.json?'
TAGS = 'tags='
DATE = ' date:>'
PAGE = '&page='
MAX = '&limit='

def get_posts(search_term, uploaded_after, page_num, max_results):
    request = LIST_BASE + \
        TAGS + search_term + \
        DATE + str(uploaded_after) + \
        PAGE + str(page_num) + \
        MAX + str(max_results)

    log = logging.getLogger('e621_api')
    log.debug('search url = ' + request)
    results = loads(SPOOF.open(request).read().decode())

    uploads = []
    for post in results:
        uploads.append(UPLOAD(post['id'], post['file_url'], post['md5'], post['file_ext']))
    return uploads

def download(url, filename):
    with open(filename, 'wb') as dest:
        source = SPOOF.open(url)
        dest.write(source.read())
