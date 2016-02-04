#!/usr/bin/env python3

from abc import (abstractmethod, ABCMeta)
from collections import OrderedDict

MAX_CACHE_ITEMS = 100000

class EngineUtils(object):
    common_config = None
    BOOLEAN_STATES = {
        'true'  : True,
        'false' : False,
        'yes'   : True,
        'no'    : False,
        'on'    : True,
        'off'   : False,
        '1'     : True,
        '0'     : False
    }

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
        eng_config['enabled'] = 'off'
        eng_config['taglist'] = '{}_taglist.txt'.format(name)
        eng_config['fastforwardlist'] = '{}_fastforwardlist.txt'.format(name)
        eng_config['blacklist'] = '{}_blacklist.txt'.format(name)
        # next, merge in custom settings
        eng_config.update(eng.get_custom_defaults_OrderedDict())
        
        # finally, nest the above under a key of the engine name
        common_config = OrderedDict()
        common_config[eng.get_name()] = eng_config
        return common_config

    @staticmethod
    def read_common_tagfiles(engine, TagUtil):
        eng_config = {}
        abort = False
        name = engine.get_name()
        cc = engine.get_comment_char()
        try:
            eng_config['tags'] = TagUtil.read_file(name, 'taglist', cc)
        except FileNotFoundError:
            TagUtil.write_file(name, 'taglist', engine.get_taglist_text(), cc)
            abort = True
        try:
            eng_config['fast'] = TagUtil.read_file(name, 'fastforwardlist', cc)
        except FileNotFoundError:
            TagUtil.write_file(name, 'fastforwardlist', engine.get_fastforward_text(), cc)
            abort = True
        try:
            eng_config['black'] = TagUtil.read_file(name, 'blacklist', cc)
        except FileNotFoundError:
            TagUtil.write_file(name, 'blacklist', engine.get_blacklist_text(), cc)
            abort = True
        if abort:
            exit(-1)
        else:
            return eng_config

    @staticmethod
    def to_bool(value):
        if value.lower() not in EngineUtils.BOOLEAN_STATES:
            raise ValueError('Not a boolean: %s' % value)
        return EngineUtils.BOOLEAN_STATES[value.lower()]

class EngineBase(object):
    @classmethod
    def get_name(self):
        ''' returns the name of the engine.'''
        raise NotImplmentedError

    @classmethod
    def get_taglist_text(self):
        ''' 
        returns a string of text that will be put in blank taglist files when 
        they are created
        '''
        raise NotImplmentedError

    @classmethod
    def get_blackist_text(self):
        ''' 
        returns a string of text that will be put in blank blacklist files when 
        they are created
        '''
        raise NotImplmentedError

    @classmethod
    def get_fastforward_text(self):
        '''
        returns the character/string which designates that a line in a tagfile
        (blacklist or taglist) should be fast-forwarded, meaning last_run is 
        ignored for these lines and all files EVER UPLOADED are downloaded. 
        '''
        raise NotImplmentedError    

    @classmethod
    def get_comment_char(self):
        ''' 
        returns the character/string which designates that a line in a tagfile
        (blacklist or taglist) is a comment and should not be read by the engine
        '''
        raise NotImplmentedError

    @staticmethod
    def get_custom_defaults_OrderedDict(self):
        '''
        returns an OrderedDict containing any custom settings (and default 
        values) used by the engine.  These settings will be written to/read from
        the upscrape config file, but will not be validated in any way, so use
        prepare(self, **kwargs) for this purpose
        '''
        raise NotImplmentedError

    @classmethod
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





