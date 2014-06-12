#!/usr/bin/env python
# pylint: disable=missing-docstring,line-too-long,too-many-public-methods,

import re
import os.path
import init_e621dl
import logging

SPOOF = init_e621dl.SpoofOpen()

PREVIEW_LINK  = '''(?<='preview' src=').*(?=' alt)'''
DOWNLOAD_LINK = '''(?<=href=").*(?=">Download)'''
IMAGE_NAME    = '''\w{10,45}\.(jpg|png|gif|swf|flv)'''
POST_PAGE = '''(?<=href='/post/show)(.+?)(?=' onclick)'''

def get_results_page(search_term, last_run, page_number):
    # construct the url, adding &page=N
    search_url = ('''https://e621.net/post?tags=''' + search_term + \
        '''%20date:>''' + last_run + '''&searchDefault=Search&page=''' + \
        str(page_number))

    # download the results page for the search term
    return SPOOF.open(search_url).read()

def results_exist(page_text):
    return False if 'No posts matched your search' in page_text else True

def get_links(page_text):
    DOWNLOADS_FROM_RESULTS = '''(?<="file_url":")(.+?)(?=",")'''
    return re.findall(DOWNLOADS_FROM_RESULTS, page_text)

def get_filename(link):
    FILENAME = '''[^/]*$'''
    return re.search(FILENAME, link).group(0)
