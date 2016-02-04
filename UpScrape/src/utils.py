#!/usr/bin/env python3
''' This module exposes a function used to parse the ini config file and
return it as dictionary, as well as several program constants '''

import configparser
import os
from datetime import datetime
import logging

from engines.common import EngineUtils
from engines import get_engines

# Program constants
VERSION = '3.0.0a'
DEFAULT_INI_NAME = 'config.ini'
DATETIME_FMT = '%Y-%m-%d'

def setup_logging():
    # see docs.python.org/2/howto/logging-cookbook.html#logging-to-multiple-destinations
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                        datefmt='%m-%d %H:%M',
                        filename='debug.log',
                        filemode='w')
    # define a Handler which writes INFO messages or higher to the sys.stderr
    console = logging.StreamHandler()
    console.setLevel(logging.DEBUG) # change this to INFO for release
    # set a format which is simpler for console use
    formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
    # tell the handler to use this format
    console.setFormatter(formatter)
    # add the handler to the root logger
    logging.getLogger('').addHandler(console)
    # get the logger used for main


class IniUtil(object):
    '''methods for working with ini files, and converting between ini<-->dict'''
    
    @staticmethod
    def _make_ini_from_defaults():
        ''' creates blank config.ini file from defaults.  
        - creates a [general] section with upscrape settings
        - creates a section for each engine with settings return from 
            EngineUtils.get_common_defaults(), which includes settings common
            to all engines, and any engine-specific custom settings supported
        '''
        # construct the first section of ini file with general settings
        # this must be modified when general UpScrape settings are altered
        ini_log = logging.getLogger('make_ini')

        main_section = 'general'
        blank = configparser.SafeConfigParser()
        blank.add_section(main_section)
        blank.set(main_section, 'lastrun',     value=datetime.now().strftime(DATETIME_FMT))
        ini_log.debug('done creating general section')


        # construct a section for each registered engine
        for eng in get_engines():
            eng_name = eng.get_name()
            blank.add_section(eng_name)
            ini_log.debug('found engine %s with the following options:', eng_name)
            eng_log = logging.getLogger('make_{}'.format(eng_name))
            eng_dict = EngineUtils.get_common_defaults(eng)[eng_name]
            eng_log.debug('  start creating %s section', eng_name)
            for opt in eng_dict:
                
                eng_log.debug('  | %s: %s', opt, eng_dict[opt])
                blank.set(eng_name, opt, eng_dict[opt])
            eng_log.debug('  done creating %s section', eng_name)
        ini_log.debug('done creating all engine sections')

        with open(DEFAULT_INI_NAME, 'w') as fp:
            blank.write(fp)   

    @staticmethod
    def _ini_to_dict(fp):
        '''converts the entire ini file (general and engine sections) to a 
        dictionary.  resulting dictionary is:
        {
            'general':      { <contents> },
            'eng0_name':    { <contents> },
            'eng1_name':    { <contents> },
            ...
            'engN_name':    { <contents> }
        }
        '''
        config = {}
        parser = configparser.SafeConfigParser()
        parser.read_file(fp)

        # read in the settings from [general]
        config['general'] = {}
        for opt in parser.options('general'):
            config['general'][opt] = parser.get('general',opt)
        
        # remove [general] before iterating over remainder 
        parser.remove_section('general')

        for eng_section in parser.sections():
            config[eng_section] = {}
            for opt in parser.options(eng_section):
                config[eng_section][opt] = parser.get(eng_section,opt)

        return config

    @staticmethod
    def read_ini():
        read_ini = logging.getLogger('utils')
        read_ini.debug('attempting to read %s', DEFAULT_INI_NAME)
        try:
            with open(DEFAULT_INI_NAME, 'r') as fp:
                return IniUtil._ini_to_dict(fp)


        except FileNotFoundError:
            IniUtil._make_ini_from_defaults()
            read_ini.error('%s was not found and was created from defaults. '
                'inspect the generated file and re-run the program', DEFAULT_INI_NAME)
            with open(DEFAULT_INI_NAME, 'r') as fp:
                return IniUtil._ini_to_dict(fp)

class TagUtil(object):
    '''methods for working with tag files (blacklists, taglists, etc)'''



if __name__ == '__main__':
    print("running utils as main")
