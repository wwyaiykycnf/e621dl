#!/usr/bin/env python3

from collections import OrderedDict
from .common import EngineBase, EngineUtils
from pprint import pprint
import os
from pathlib import Path

import logging

NAME = 'e621'
DEFAULTS = OrderedDict()

DEFAULTS['format'] = '${tag}_${id}'

class e621_Engine(EngineBase):
    name = "e621"
    log = logging.getLogger("e621")

    def get_name(self):
        return self.name

    def read_tagfile(self, filename):
        tag_list = []
        print('read_tagfile: {}'.format(filename))
        upscrape_dir = Path(os.path.dirname(__file__)).parent.parent
        for line in open(os.path.join(upscrape_dir, filename)):
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

            Should set self.state = False if any error occurs which prevents
            the engine from functioning, else set self.state = True
        '''

        # pull out boolean values
        try:
            self.duplicates = EngineUtils.to_bool(kwargs.get('duplicates'))
            self.state = EngineUtils.to_bool(kwargs.get('state'))
        except ValueError as exp:
            self.log.error(exp)
            self.state = False

        # open and read taglist
        self.taglist_filename = kwargs.get('tags')
        try:
            self.tags = self.read_tagfile(self.taglist_filename)
        except FileNotFoundError as exc:
            # create it if it doesn't exist
            EngineUtils.make_file(self.name, 'taglist', 
                'all posts matching any line in this file will be downloaded')
            self.log.error('%s was not found and was created from defaults. '
                'inspect the generated file and re-run the program',
                self.taglist_filename)
            self.state = False

        # open and read blacklist
        self.blacklist_filename = kwargs.get('blacklist')
        try:
            self.blacklist = self.read_tagfile(self.blacklist_filename)
        except FileNotFoundError as exc:
            # create it if it doesn't exist
            EngineUtils.make_file(self.name, 'blacklist', 
                'any post matching any line in this file will be exluded')
            self.log.error('%s was not found and was created from defaults. '
                'inspect the generated file and re-run the program',
                self.blacklist_filename)
            self.log.error('')
            self.state = False

        # todo: validate format... maybe this will not happen here
        self.format = kwargs.get('format')

        print("called e621 prepare")

    def get_custom_defaults_OrderedDict(self):
        return DEFAULTS

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

