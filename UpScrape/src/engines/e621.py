#!/usr/bin/env python3

from collections import OrderedDict
from .common import EngineBase, EngineUtils
from pprint import pprint
import os
from pathlib import Path

import logging

class e621_Engine(EngineBase):
    name = "e621"
    log = logging.getLogger("e621")

    DEFAULTS = OrderedDict()
    DEFAULTS['format'] = '${tag}_${id}'

    def get_name(self):
        return self.name

        full_name = '{}_{}.txt'.format(name, filetype)
        with open(full_name, 'w') as outfile:
            outfile.write('# {}'.format(contents))  

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
            with open(self.taglist_filename, 'w') as fp:
                fp.write('# == e621 taglist ==\n')
                fp.write('# \n')
                fp.write('# each line in this file represents a search on e621\n')
                fp.write('# lines starting with # are ignored\n')
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
            with open(self.blacklist_filename, 'w') as fp:
                fp.write('# == e621 blacklist == \n')
                fp.write('# \n')
                fp.write('# skips download of posts matching any line in this file\n')
                fp.write('# lines starting with # are ignored\n')
            self.log.error('%s was not found and was created from defaults. '
                'inspect the generated file and re-run the program',
                self.blacklist_filename)
            self.state = False

        # todo: validate format... maybe this will not happen here
        self.format = kwargs.get('format')

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

