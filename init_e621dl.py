#!/usr/bin/env python
# pylint: disable=missing-docstring,line-too-long,too-many-public-methods,

import argparse
import logging
import FixedFifo
from urllib import FancyURLopener
import cPickle as pickle

def get_args():
    parser = argparse.ArgumentParser(prog='e621dl',
        description='automated e621 downloader.\
        add artists/tags to tags.txt and run!')

    verbosity = parser.add_mutually_exclusive_group(required=False)
    verbosity.add_argument('-v', '--verbose', action='store_true',
        help='display debug information while running')
    verbosity.add_argument('-q', '--quiet', action='store_true',
        help='display no output while running (except errors)')

    return parser.parse_args()

def get_log_level(args):

    if args.verbose:
        lvl = logging.DEBUG
    elif args.quiet:
        lvl = logging.ERROR
    else:
        lvl = logging.INFO

    return lvl

def get_downloads_list(path):
    # open the cachefile
    log = logging.getLogger('e621dl')
    try:
        cache = pickle.load(open(path, 'rb'))
        log.debug('opened recent downloads list')

    except IOError:
        cache = FixedFifo.FixedFifo(65536)
        log.error("couldn't open " + path + "  starting new recent downloads list")
    return cache


def read_tags_file(filename):
    with open(filename, 'r') as tagfile:
        tags = [item.rstrip() for item in tagfile.readlines()]
        tags.sort(key=lambda y: y.lower())
    return tags

class SpoofOpen(FancyURLopener):
    version = 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.8.0.12) Gecko/20070731 Ubuntu/dapper-security Firefox/1.5.0.12'

