#!/usr/bin/env python3

from .engine_base import Engine

class e621(Engine):
    def get_login():
        ''' returns true if login was successful, false if it failed for any reason '''
        return False

    def get_query(query_str):
        '''returns a list of tuples, each containing (pathname, url), where:
            - pathname is the full path and formatted name
            - url is the complete, raw url where the file can be downloaded from
        returns None when query_str yeilds no valid* results
            *: depending on program config, previously-seen files can be omitted'''
        return False