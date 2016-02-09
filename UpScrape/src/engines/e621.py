#!/usr/bin/env python3

from collections import OrderedDict
from .common import EngineBase, EngineUtils
from pprint import pprint
import os
from pathlib import Path

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

    def scrape(self, **kwargs):
        print("called e621 scrape")

