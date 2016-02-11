#!/usr/bin/env python3

from collections import OrderedDict
from .common import EngineBase, EngineUtils
from pprint import pprint
import os
from pathlib import Path
import urllib.request
import urllib.parse
import json

import logging

class e621_Engine(EngineBase):
    name = "e621"
    taglist_text = [
        'list the tags to keep updated below.',
        'each line represents one search performed on the site',        
        'multiple tags are allowed on a line.',
        'any file uploaded since last_run will be downloaded'
        ]

    blacklist_text = [
        'list blacklisted tags below.',
        'multiple tags are allowed on a line.',
        'any post which matches any line in this file will not be not downloaded'
        ]
    ff_text = [
        'list the tags to fast-forward below.',
        'each line represents one search performed on the site',        
        'multiple tags are allowed on a line.',
        'last_run will be ignored for these searches (all matching files will download)',
        'for best performance, remove lines from this file after successful fast-forward'
        ]
    comment_char = '#'
    
    log = logging.getLogger("e621")

    DEFAULTS = OrderedDict()
    DEFAULTS['format'] = '${tag}_${id}'
    DEFAULTS['duplicates'] = 'off'
    max_results = 100

    def get_name(self):
        return self.name

    def get_taglist_text(self):
        return self.taglist_text

    def get_blacklist_text(self):
        return self.blacklist_text

    def get_fastforward_text(self):
        return self.ff_text    

    def get_comment_char(self):
        return self.comment_char

    def read_tagfile(self, filename):
        tag_list = []
        for line in open(filename, 'r'):
            raw_line = line.strip()
            if not raw_line.startswith("#") and raw_line != '':
                tag_list.append(raw_line)
        self.log.debug('opened %s and read %d items', filename, len(tag_list))
        return tag_list

    def validate_custom_defaults(self, **kwargs):
        config = {}

        # pull out boolean values
        abort = False
        try:
            config['duplicates'] = EngineUtils.to_bool(kwargs.get('duplicates'))
            config['enabled'] = EngineUtils.to_bool(kwargs.get('enabled'))

        except ValueError:
            abort = False

        if abort:
            config['enabled'] = False

        # todo: validate format... maybe this will not happen here
        config['format'] = kwargs.get('format')

        return config

    def get_custom_defaults_OrderedDict(self):
        return self.DEFAULTS

    def get_page_posts(self, tag, page, since=None):
        # if 'since' was supplied, append it to the tag
        tag = tag + ' date:>' + since if since else tag 

        search = 'http://e621.net/post/index.json?tags={}&page={}&limit={}'.format(tag, page, self.max_results)

        with urllib.request.urlopen(search) as request:
            response = json.loads(request.read().decode())
            self.log.debug('  url: %s', search)
            self.log.debug('  posts: [%d], page: [%d]', len(response), page)
            return response

    def get_all_posts(self, tag, since=None):
        accumulating = True
        potential_downloads = []
        current_page = 1
        
        if (since):
            self.log.info("finding uploads matching '%s' since %s", tag, since)
        else:
            self.log.info("finding all uploads matching '%s' ever uploaded", tag)

        while (accumulating):
            links_found = self.get_page_posts(tag, current_page, since)
            if not links_found:
                accumulating = False
            else:
                # add links found to list to be downloaded
                potential_downloads += links_found
                # continue accumulating if found == max, else stop accumulation
                accumulating = len(links_found) == self.max_results
                current_page += 1
        return potential_downloads



    def scrape(self, last_run, **kwargs):
        downloads = self.get_all_posts('cat dog fox')#, '2016-2-8')

        #for line in kwargs['fastforwardlist']:
        #    self.get_all_posts(line)
        #
        #for line in kwargs['taglist']:
        #    self.get_all_posts(line, since)






