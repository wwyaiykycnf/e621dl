#!/usr/bin/env python3

from collections import OrderedDict
from .common import EngineBase, EngineUtils

NAME = 'e621'
DEFAULTS = OrderedDict()

DEFAULTS['format']   = '${tag}_${id}'

class e621_Engine(EngineBase):
    def get_name(self):
        return "e621"

    def prepare(self, **kwargs):
        ''' called during creation of engine.  kwargs is a dict containing all
            config items in [general] as well as all items in the engine-
            specific section of the config file. this method does the following:

            - checks kwargs for errors
            - gets blacklist from disk or remote and checks it for errors
            - performs other engine-specific checks to ensure readiness

            Should raise NotImplmentedError if any error occurs which prevents
            the engine from functioning. 
        '''
        print "called e621 prepare"

    def get_custom_defaults_OrderedDict():
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
        print "called e621 scrape"

