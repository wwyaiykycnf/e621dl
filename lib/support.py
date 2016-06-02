# pylint: disable=missing-docstring,line-too-long,too-many-public-methods,

import argparse
import logging
import json
import FixedFifo
import default
import re
from types import IntType, BooleanType
from urllib import FancyURLopener
import cPickle as pickle
import os

class SpoofOpen(FancyURLopener):
    version = 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.8.0.12) Gecko/20070731 Ubuntu/dapper-security Firefox/1.5.0.12'

def get_verbosity_level():

    # build the parser
    parser = argparse.ArgumentParser(prog='e621dl',
        description='automated e621 downloader.\
        add artists/tags to tags.txt and run!')

    # add mutually exclusive options verbose/quiet
    verbosity = parser.add_mutually_exclusive_group(required=False)
    verbosity.add_argument('-v', '--verbose', action='store_true',
        help='display debug information while running')
    verbosity.add_argument('-q', '--quiet', action='store_true',
        help='display no output while running (except errors)')

    # parse using argparser
    args = parser.parse_args()

    if args.quiet:
        return logging.ERROR
    elif args.verbose:
        return logging.DEBUG
    else:
        return logging.INFO

def make_default_configfile(filename):
    log = logging.getLogger('configfile')
    log.error('new default file created: ' + filename)
    log.error('\tverify this file and re-run the program')
    with open(filename, 'w') as outfile:
        json.dump(default.CONFIG_FILE, outfile, indent=4, sort_keys=True,)
    return default.CONFIG_FILE

def get_configfile(filename):
    log = logging.getLogger('configfile')
    if not os.path.isfile(filename):
        return make_default_configfile(filename)
    else:
        with open(filename, 'r') as infile:
            log.debug('opened ' + filename)
            return json.load(infile)

def make_default_tagfile(filename):
    log = logging.getLogger('tagfile')
    with open(filename, 'w') as outfile:
        outfile.write(default.TAG_FILE)

    log.error('new default file created: ' + filename)
    log.error('\tadd to this file and re-run the program')

def get_tagfile(filename):
    log = logging.getLogger('tag_file')

    if not os.path.isfile(filename):
        make_default_tagfile(filename)
        return default.TAG_FILE
    else:
        # read out all lines not starting with #
        tag_list = []
        for line in open(filename):
            raw_line = line.strip()
            if not raw_line.startswith("#") and raw_line != '':
                tag_list.append(raw_line)

        log.debug('opened %s and read %d items', filename, len(tag_list))
        return tag_list

def get_cache(filename, size):
    log = logging.getLogger('cache')
    try:
        cache = pickle.load(open(filename, 'rb'))
        cache.resize(int(size))
        log.debug('loaded existing cache')
        log.debug('capacity = %d (of %d)', len(cache), cache.size())
        log.debug('size on disk = %f kb', os.path.getsize(filename)/1024)

    except IOError:
        cache = FixedFifo.FixedFifo(size)
        log.debug('new blank cache created. size = %d', size)

    return cache


def sub_char(char):
    illegal = ['\\', '/', ':', '*', '?', '"', '<', '>', '|', ' ']
    return '_' if char in illegal else char

def safe_filename(tag_line, item, config_dict):
    safe_tagline = ''.join([sub_char(c) for c in tag_line])

    name = str(getattr(item, config_dict['part_used_as_name']))
    if config_dict['create_subdirectories'] == True:
        if not os.path.isdir(config_dict['download_directory'] + safe_tagline.decode('utf-8')):
            os.makedirs(config_dict['download_directory'] + safe_tagline)
        safe_filename = safe_tagline + '/' + name + '.' + item.ext

    else:
        safe_filename = safe_tagline.decode('utf-8') + '_' + name + '.' + item.ext.decode('utf-8')

    return safe_filename

def validate_tagfile(tags, filename):
    if len(tags) == 0:
        log = logging.getLogger('tag_file')
        log.error('no tags found in %s', filename)
        log.error('\tadd lines to this file and re-run program')
        return False
    return True

def validate_config(c):
    log = logging.getLogger('config_file')
    try:
        assert type(c['create_subdirectories']) is BooleanType, \
            "'create_subdirectories' must be set to true or false"
        assert c['parallel_downloads'] in range(1, 17),\
            "'parallel_downloads' must be a number from 1 to 16 (no quotes)"

        assert type(c['cache_size']) is IntType and \
            c['cache_size'] > 0, \
            "'cache_size' must be a number greater than 0 (no quotes)"

        assert bool(re.match(r'\d{4}-\d{2}-\d{2}', c['last_run'])) == True, \
            "'last_run' format must be: \"YYYY-MM-DD\" (quotes required"

        assert c['part_used_as_name'] == "id" or \
            c['part_used_as_name'] == "md5", \
            "'part_used_as_name' must be 'id' or 'md5'"

        if not os.path.exists(c['download_directory']):
            log.info('empty download directory created')
            os.makedirs(c['download_directory'])

        return True

    except AssertionError as ex_msg:
        log.error("could not parse config file")
        log.error(ex_msg)
        return False
