#!/usr/bin/env python3
''' This module exposes a function used to parse the ini config file and
return it as dictionary, as well as several program constants '''

import configparser
import os
from datetime import datetime
import logging

from .engines import get_engine_defaults

# Program constants
VERSION = '3.0.0a'
DEFAULT_INI_NAME = 'config.ini'
DATETIME_FMT = '%Y-%m-%d'

def enable_logging():
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
    
    def create_ini_from_defaults(self):
        ''' creates blank config.ini file from defaults.  
        - creates a [general] section with upscrape settings
        - creates a section for each engine with settings return from 
            EngineUtils.get_engine_defaults(), which includes settings common
            to all engines, and any engine-specific custom settings supported
        '''
        # construct the first section of ini file with general settings
        main_section = 'general'
        blank = configparser.SafeConfigParser()
        blank.add_section(main_section)
        blank.set(main_section, 'lastrun',     value=datetime.now().strftime(DATETIME_FMT))

        # construct a section for each registered engine
        for eng_dict in get_engine_defaults():
            print(eng_dict)
            for eng_name in eng_dict:
                blank.add_section(eng_name)
                for opt in eng_dict[eng_name]:
                    blank.set(eng_name, eng_dict[eng_name][opt])
        
        # write the ini file out to disk
        with open(DEFAULT_INI_NAME, 'w') as fp:
            blank.write(fp)   

#a = { 'a': { 'a1': 'z', 'a2': 'x'  }  }
#b = { 'b': { 'b1': 'y', 'b2': 'w'  }  }
#l = [a,b]
#
#for d in l:
#    for name in d:
#        print('eng_name = ' + name)
#        for set in d[name]:
#            print(set + ' is ' + d[name][set])


#         for engine_name in list(ENGINES.keys()):
#             blank.add_section(engine_name)
#             blank.set(engine_name, 'state',     value='Off')
#             blank.set(engine_name, 'tags',      value='{}_tags.txt'.format(engine_name))
#             blank.set(engine_name, 'blacklist', value='{}_blacklist.txt'.format(engine_name))
# 
#         with open(DEFAULT_INI_NAME, 'w') as fp:
#             blank.write(fp)
# 
#         return False

    def ini_to_dict(self, fp):
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

        # general settings and default values
        config['lastrun']     = parser.get('general','lastrun')

        # for engine in get_engine_defaults():


            # engine_section = {}
            # error = None
            # try:
            #     engine_section['state']       = parser.getboolean(engine_name, 'state')
            #     engine_section['tags']        = parser.get(engine_name,'tags')
            #     engine_section['blacklist']   = parser.get(engine_name,'blacklist')
            # except (configparser.Error) as e:
            #     error = str(e)
            # except KeyError as e:
            #     error = "section [{}] not found in config file".format(e)
            # except ValueError as e:
            #     error = 'error processing section [{}]: {}'.format(engine_name, e)
            # else:
            #     LOG.debug('successfully parsed [%s] section in %s', engine_name, DEFAULT_INI_NAME)
            #     config[ENG][engine_name] = engine_section
            # if error:
            #     LOG.error(error)
            #     error_str = "problem parsing [{}], this engine will be skipped.".format(engine_name)
        # return config        



#    def __init__(self, filename):
#        ''' opens the ini file and converts it to a dict for later use'''
#        try:
#            with open(DEFAULT_INI_NAME, 'r') as fp:
#                LOG.debug('file exists:  %s', DEFAULT_INI_NAME)
#                config = self.ini_to_dict(fp)
#
#         except FileNotFoundError as e:            
#            with open(DEFAULT_INI_NAME, 'w') as fp:
#                fp.write(self.blank_ini())
#
#            LOG.error('%s not found. a new file has been created.  '
#                'please review the generated file and retry', DEFAULT_INI_NAME)
#            exit()
#
#     def get_general_config(self):
#         ''' returns the [general] section of the ini file '''
#         return None
# 
#     def get_engine_config(self, engine):
#         ''' returns a flat dict containing config for <engine> and all items in
#             the [general] section of the ini'''
#         return None
# 
#     def get_engine_
# 
# 
# 
#     def __init_ini__(self):
#         blank = configparser.SafeConfigParser()
#         blank.add_section(GEN)
#         blank.set(GEN, 'lastrun',     value=datetime.now().strftime(DATETIME_FMT))
#         blank.set(GEN, 'format',      value='IgnoredForNow')
#         blank.set(GEN, 'duplicates',  value='Off')
# 
#         for engine_name in list(ENGINES.keys()):
#             blank.add_section(engine_name)
#             blank.set(engine_name, 'state',     value='Off')
#             blank.set(engine_name, 'tags',      value='{}_tags.txt'.format(engine_name))
#             blank.set(engine_name, 'blacklist', value='{}_blacklist.txt'.format(engine_name))
# 
#         with open(DEFAULT_INI_NAME, 'w') as fp:
#             blank.write(fp)
# 
#     def __ini_to_dict__(self, fp):
#         config = {}
#         parser = configparser.SafeConfigParser()
#         
#         parser.read_file(fp)
# 
#         config['lastrun']     = parser.get(GEN,'lastrun')
#         config['format']      = parser.get(GEN,'format')
#         config['duplicates']  = parser.getboolean(GEN,'duplicates')
# 
#         config[ENG] = {}
# 
#         for engine_name in ENGINES.keys():
#             engine_section = {}
#             error = None
#             try:
#                 engine_section['state']       = parser.getboolean(engine_name, 'state')
#                 engine_section['tags']        = parser.get(engine_name,'tags')
#                 engine_section['blacklist']   = parser.get(engine_name,'blacklist')
#             except (configparser.Error) as e:
#                 error = str(e)
#             except KeyError as e:
#                 error = "section [{}] not found in config file".format(e)
#             except ValueError as e:
#                 error = 'error processing section [{}]: {}'.format(engine_name, e)
#             else:
#                 LOG.debug('successfully parsed [%s] section in %s', engine_name, DEFAULT_INI_NAME)
#                 config[ENG][engine_name] = engine_section
#             if error:
#                 LOG.error(error)
#                 error_str = "problem parsing [{}], this engine will be skipped.".format(engine_name)
#         return config
# 
#     def get_config(self):

# 
#     def get_logger(self):
#         return logging.getLogger('main')
#     
#     def get_engines(self):
#         return None

