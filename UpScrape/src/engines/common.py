#!/usr/bin/env python3

from abc import (abstractmethod, ABCMeta)
from collections import OrderedDict
import logging
from os import path
from os import makedirs

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
    def to_bool(value):
        '''helper method to convert from standard ini states to 
        boolean values.  raises ValueError on lookup failure'''
        if value.lower() not in EngineUtils.BOOLEAN_STATES:
            raise ValueError('Not a boolean: %s' % value)
        return EngineUtils.BOOLEAN_STATES[value.lower()]

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
        '''given an engine, returns a dictionary of all the engines settings and
        the default value of these settings.  the resulting dictionary will 
        contain all common settings as well as any custom settings returned by 
        eng.get_custom_defaults_OrderedDict(), and will resemble the following:
        {
            'engine_name': 
            {
                'common1' : 'default_for_common1'
                'commonN' : 'default_for_commonN'
                'custom1' : 'default_for_custom_setting_1'
            }
        } 
        '''

        # first, make a dict with common settings
        name = eng.get_name()
        eng_config = OrderedDict()
        eng_config['enabled'] = 'off'
        eng_config['taglist'] = '{}_taglist.txt'.format(name)
        eng_config['fastforwardlist'] = '{}_fastforwardlist.txt'.format(name)
        eng_config['blacklist'] = '{}_blacklist.txt'.format(name)
        eng_config['download_dir'] = 'downloads'
        # next, merge in custom settings
        eng_config.update(eng.get_custom_defaults_OrderedDict())
        
        # finally, nest the above under a key of the engine name
        common_config = OrderedDict()
        common_config[eng.get_name()] = eng_config
        return common_config

    @staticmethod
    def validate_common_defaults(engine, **kwargs):
        '''parses kwargs to validate the runtime config and create/open any 
        files required for the operation of all engines. 

        specifically:
        - opens (or creates, if missing) the 3 files common to all engines
        - reads the above 3 files into eng_config['taglist'], 
            eng_config['blacklist'], and eng_config['fastforwardlist']
        - converts kwargs['enabed'] to a boolean
        - if any validation error occurs, the returned dictionary will have its 
        'enabled' key set to False.
        '''

        eng_config = {}
        abort = False
        name = engine.get_name()
        cc = engine.get_comment_char()
        try:
            eng_config['taglist'] = EngineUtils.read_file(name, 'taglist', cc)
        except FileNotFoundError:
            EngineUtils.write_file(name, 'taglist', engine.get_taglist_text(), cc)
            abort = True
        try:
            eng_config['fastforwardlist'] = EngineUtils.read_file(name, 'fastforwardlist', cc)
        except FileNotFoundError:
            EngineUtils.write_file(name, 'fastforwardlist', engine.get_fastforward_text(), cc)
            abort = True
        try:
            eng_config['blacklist'] = EngineUtils.read_file(name, 'blacklist', cc)
        except FileNotFoundError:
            EngineUtils.write_file(name, 'blacklist', engine.get_blacklist_text(), cc)
            abort = True

        eng_config['download_dir'] = kwargs['download_dir']
        makedirs(eng_config['download_dir'], exist_ok=True)

        try:
            eng_config['enabled'] = EngineUtils.to_bool(kwargs['enabled'])
        except ValueError:
            abort = True

        if abort:
            eng_config['enabled'] = False

        return eng_config

    @staticmethod
    def read_file(engine_name, file_type, comment_char):
        ''' helper method for reading tagfiles
        given an engine name, file type, and comment char, returns contents 
        of file as a list.  ignores lines starting with comment_char.
        '''

        log = logging.getLogger('common')
        filename = '{}_{}.txt'.format(engine_name, file_type)        
        tag_list = []
        for line in open(filename, 'r'):
            raw_line = line.strip()
            if not raw_line.startswith(comment_char) and raw_line != '':
                tag_list.append(raw_line)
        log.debug('opened %s and read %d items', filename, len(tag_list))
        return tag_list
    
    @staticmethod
    def write_file(engine_name, file_type, contents, comment_char):
        ''' helper method for creating tagfiles in a standard format.  

        example: assuming the comment character is '#':

            <-- start of file: engine_name_file_type.txt
            # === engine_name_file_type ===
            #
            # content 
            # (lines starting with # are ignored)
            <-- end of file

        content may be a single string, or a list of lines.
        '''
        filename = '{}_{}.txt'.format(engine_name, file_type)        
        log = logging.getLogger('common')
        header = '=== {} {} ==='.format(engine_name, file_type)
        comment_info = '(lines starting with {} are ignored)'.format(comment_char)

        with open(filename, 'w') as fp:
            fp.write('{} {}\n'.format(comment_char, header))
            fp.write('{}\n'.format(comment_char))
            fp.write('{} {}\n'.format(comment_char, comment_info))
            if type(contents) is list:
                for line in contents:
                    fp.write('{} {}\n'.format(comment_char, line))
            else:
                fp.write('{} {}\n'.format(comment_char, contents))

        log.error('%s was created from defaults. inspect the generated'
                ' file and re-run the program', filename)        

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
        returns a string of text that will be put in blank fastforwardlist files
        when they are created
        '''
        raise NotImplmentedError    

    @classmethod
    def get_comment_char(self):
        ''' 
        returns the character/string which designates that a line in a tagfile
        (blacklist/taglist/fastforwardlist) is a comment and should not be used
        by the engine
        '''
        raise NotImplmentedError

    @staticmethod
    def get_custom_defaults_OrderedDict(self):
        '''
        returns an OrderedDict containing any custom settings (and default 
        values) used by the engine.  
    
        These settings will be written to/read from the upscrape config file, 
        but will not be validated in any way, so use 
        validate_custom_defaults() for this purpose
        '''
        raise NotImplmentedError

    @classmethod
    def validate_custom_defaults(self, **kwargs):
        ''' 
        performs any neccesary preparation needed before scrape() is called

        kwargs contains all settings from the config file.  all common settings
        have been vailidated by the time this method is called, but any settings
        returned by get_custom_defaults_OrderedDict() have not.  

        this method should return a dictionary consisting of any custom settings
        and their validated values.  if any error is encountered, the 'enabled'
        key in the returned dictionary should be set to False.
        '''
        raise NotImplmentedError

    @classmethod
    def scrape(self, last_run, **kwargs):
        ''' 
        perform a full update.

        for each line in the taglist, all files uploaded since kwargs['last_run']
        are downloaded.  any post which contains a blacklisted tag (or group of
        tags) in its metadata is skipped. 

        the fastforwardlist is processed in the same way as the taglist except 
        last_run is ignored. 
        '''
        raise NotImplmentedError
