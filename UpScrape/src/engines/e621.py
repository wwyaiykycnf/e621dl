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

    def prepare(self, **kwargs):
        ''' called during creation of engine.  kwargs is a dict containing all
            config items in [general] as well as all items in the engine-
            specific section of the config file. this method does the following:

            - checks kwargs for errors
            - gets blacklist from disk or remote and checks it for errors
            - performs other engine-specific checks to ensure readiness

            Should set self.enabled = False if any error occurs which prevents
            the engine from functioning, else set self.enabled = True
        '''

        # pull out boolean values
        abort = False
        try:
            self.duplicates = EngineUtils.to_bool(kwargs.get('duplicates'))
        except ValueError:
            abort = False

        try:
            self.enabled = EngineUtils.to_bool(kwargs.get('enabled'))
        except ValueError:
            abort = False

        if abort:
            self.enabled = False

        # todo: validate format... maybe this will not happen here
        self.format = kwargs.get('format')

        return self.enabled

    def get_custom_defaults_OrderedDict(self):
        return self.DEFAULTS

    def scrape(self):
        ''' processes the tagfile for the engine and downloads all files that
            have not been previously seen  

            tagfile lines starting with $ are fast-forwarded, meaning last_run 
                date in the config file is ignored for these lines and all files
                EVER UPLOADED are downloaded. 

            blacklist (if one exists) is applied to all files before downloading

            a default implementation of this method is provided in EngineBase,
            but it can be overridden if needed.
        '''
        print("called e621 scrape")

