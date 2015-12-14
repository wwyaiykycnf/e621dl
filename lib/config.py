#!/usr/bin/env python3
#pylint: disable=bad-whitespace
''' This module exposes a function used to parse the ini config file and
return it as dictionary, as well as several program constants '''

import configparser
import os
from datetime import datetime
import logging

DEFAULT_INI_NAME = 'config.ini'
DATETIME_FMT = '%Y-%m-%d'
ENGINES = ['e621_engine']

GEN = 'general'
ENG = 'engines'

LOG = logging.getLogger('config')

DEFAULT_TAG_FILE = '''### Instructions ###
#
#
# Add tags/artists to download to this file, one group per line.  Any tag
# combination that works on the site should work here, including multiple 
# search terms and meta-tags
#
# All lines in this file that begin with # are treated as comments
#
# List any tags, artists, meta-tags, or groups of tags to track below:
'''

def __make_tagfile_if_missing__(engine_name):
    filename = 'tags_{}.txt'.format(engine_name.split('_')[0])
    if os.path.exists(filename):
        LOG.debug('tagfile %s exists', filename)
        return False
    else:
        with open(filename, 'w') as fp:
            fp.write(DEFAULT_TAG_FILE)
        LOG.info('new (empty) tagfile %s created', filename)
        return True

def __make_ini_if_missing__():
    if os.path.exists(DEFAULT_INI_NAME):
        LOG.debug('%s exists', DEFAULT_INI_NAME)
        return False
    else:
        blank = configparser.SafeConfigParser()
        blank.add_section(GEN)
        blank.set(GEN, 'lastrun',     value=datetime.now().strftime(DATETIME_FMT))
        blank.set(GEN, 'format',      value='IgnoredForNow')
        blank.set(GEN, 'duplicates',  value='Off')
        blank.set(GEN, 'debug',       value='Off')

        for engine_name in ENGINES:
            blank.add_section(engine_name)
            blank.set(engine_name, 'state', value='Off')
            blank.set(engine_name, 'user',  value='none')
            blank.set(engine_name, 'pass',  value='none')

        with open(DEFAULT_INI_NAME, 'w') as fp:
            blank.write(fp)
        LOG.info('new %s created using program defaults', DEFAULT_INI_NAME)
        return True

def __ini_to_dict__():

    config = {}
    parser = configparser.SafeConfigParser()
    parser.read(DEFAULT_INI_NAME)

    config['lastrun']     = parser.get(GEN,'lastrun')
    config['format']      = parser.get(GEN,'format')
    config['duplicates']  = parser.getboolean(GEN,'duplicates')
    config['debug']       = parser.getboolean(GEN,'debug')

    engines = parser.sections()
    engines.remove(GEN)

    config[ENG] = {}

    for engine_name in engines:
        config[ENG][engine_name] = {}
        config[ENG][engine_name]['state']  = parser.getboolean(engine_name, 'state')
        config[ENG][engine_name]['user']   = parser.get(engine_name,'user')
        config[ENG][engine_name]['pass']   = parser.get(engine_name,'pass')

    return config

def get_config():
    '''reads ini file and returns it as a dictionary. throws GetConfigException on error'''

    missing_configfile = __make_ini_if_missing__()
    missing_tagfile = False

    for engine_name in ENGINES:
        missing_tagfile = __make_tagfile_if_missing__(engine_name)

    if missing_tagfile or missing_configfile:
        raise IOError('Required file(s) were not found.  Review the generated files and retry')

    try:
        return __ini_to_dict__()

    except (configparser.NoSectionError, configparser.NoOptionError, TypeError, ValueError) as e:
        LOG.error('%s could not be parsed.  correct the errors or delete it, then retry', DEFAULT_INI_NAME)
        raise e

