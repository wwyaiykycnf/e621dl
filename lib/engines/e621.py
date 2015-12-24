#!/usr/bin/env python3

from .engine_base import Engine

import urllib.parse 
from requests import session
import xml.etree.ElementTree as ET

DEFAULT_TAG_FILE = '''### e621 taglist ###
# Note: All lines in this file that begin with # are treated as comments
#
# Add tags/artists to track to this file, one group per line.  Any tag
# combination that works on the site should work here, including multiple 
# search terms and meta-tags
#
# All lines in this file that begin with # are treated as comments
#
# List any tags, artists, meta-tags, or groups of tags to track below:
'''

DEFAULT_BLACKIST_FILE = '''### e621 blacklist ###
# Note: All lines in this file that begin with # are treated as comments
# 
# Add tags/artists to blacklist to this file, one group per line.  Most tag
# combinations should work here, but meta-tags have limited support and their
# use is not reccomended.
#
# The blacklist automatically skips the download of any post which contains 
# matches for ALL of the tags on ANY single line of the blacklist.
# 
# List any tags, artists, meta-tags, or groups of tags to blacklist below:
'''

class e621(Engine):

    def get_default_tagfile_contents(self):
        return DEFAULT_TAG_FILE

    def get_default_blacklist_contents(self):
        return DEFAULT_BLACKIST_FILE

    def get_query(query_str):
        '''returns a list of tuples, each containing (pathname, url), where:
            - pathname is the full path and formatted name
            - url is the complete, raw url where the file can be downloaded from
        returns None when query_str yeilds no valid* results
            *: depending on program config, previously-seen files can be omitted'''
    
        return False