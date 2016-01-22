#!/usr/bin/env python3
''' This module exposes a function used to parse the ini config file and
return it as dictionary, as well as several program constants '''

import configparser
import os
from datetime import datetime
import logging

# Program constants
VERSION = '3.0.0b'
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


# class IniUtil(object):
#     '''methods for working with ini files, and converting between ini<-->dict'''
# 
# 
# 
# class ConfigUtil(object):
#     def __init__(self):
# 
# 
#     def __init__(self, filename):
#         ''' opens the ini file and converts it to a dict for later use'''
#         return None
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
#         try:
#             with open(DEFAULT_INI_NAME, 'r') as fp:
#                 LOG.debug('file exists:  %s', DEFAULT_INI_NAME)
#                 return self.__ini_to_dict__(fp)
# 
#         except FileNotFoundError as e:            
#             self.__init_ini__()
#             LOG.error('%s not found. a new file has been created.  '
#                 'please review the generated file and retry', DEFAULT_INI_NAME)
#             exit()
# 
#     def get_logger(self):
#         return logging.getLogger('main')
#     
#     def get_engines(self):
#         return None

