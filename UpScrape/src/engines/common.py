#!/usr/bin/env python3

from abc import (abstractmethod, ABCMeta)
from collections import OrderedDict

MAX_CACHE_ITEMS = 100000

class EngineUtils(object):
    common_config = None

    @staticmethod
    def make_file(name, filetype, contents):
        ''' creates a file <engine_name>_<filetype>.txt with <contents> as a 
        comment on the first line'''
        full_name = '{}_{}.txt'.format(name, filename)
        with open(full_name, 'w') as outfile:
            outfile.write('# {}'.format(contents))  

    @staticmethod
    def is_blacklisted(self, blacklist, metadata):
        ''' checks a query_result against the engine blacklist (if present).
            
            a default implementation of this method is provided in EngineBase,
            but it can be overridden if needed. 
        
        returns 
            - True      query_result is blacklisted (do not download)
            - False     query_result is not blacklisted (proceed with download)
        '''
        # TODO: default blacklist code here
        return False

    @staticmethod
    def make_filename(self, query_result):
        ''' given a single query_result, creates a proper filename, taking user
            specified format and other program settings into account''' 
        return False   

    @abstractmethod
    def download_file(self, **kwargs):
        ''' downloads a single file.  is called once for each file found during
            the update.

            returns true/false indicating whether success of file download'''
        return False

    @staticmethod
    def get_engine_defaults(eng):
        # first, make a dict with common settings
        name = eng.get_name()
        eng_config = OrderedDict()
        eng_config['state'] = 'off'
        eng_config['tags'] = '{}_taglist.txt'.format(name)
        eng_config['blacklist'] = '{}_blacklist'.format(name)
        eng_config['duplicates'] = 'off'
        # next, merge in custom settings
        eng_config.update(eng.get_custom_defaults_OrderedDict())
        
        # finally, nest the above under a key of the engine name
        common_config = OrderedDict()
        common_config[eng.get_name()] = eng_config
        return common_config


class EngineBase(object):
    @staticmethod
    def get_name():
        raise NotImplmentedError

    @staticmethod
    def get_custom_defaults_OrderedDict():
        raise NotImplmentedError

    @classmethod
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
        raise NotImplmentedError

    @classmethod
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
        raise NotImplmentedError





