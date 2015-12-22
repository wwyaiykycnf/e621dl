#!/usr/bin/env python3
''' todo '''
import abc
import lib.config
import os
import pickle
import logging

class EngineCache(object):    
    '''
    A simple fixed-length FIFO of size N, which automatically pops the oldest 
    element when the N+1st element is pushed.
    '''
    def __init__(self, max_size):
        self.max_size = max_size
        self.contents = []

    def __contains__(self, key):
        return key in self.contents

    def __len__(self):
        return len(self.contents)

    def pop(self):
        return self.contents.pop()

    def push(self, key):
        self.contents.insert(0, key)
        return self.pop() if len(self.contents) > self.max_size else None

class Engine(object, metaclass=abc.ABCMeta):
    '''all new engines must derive from this class and implement their own 
    verisons of:
        - get_login(): returns true if login was successful, false if it failed
        - get_query(query_str): performs a query for query_str
    ''' 

    def __init__(self, config, key):
        self.name       = key.split('_')[0]
        self.log        = logging.getLogger(self.name)
        self.nameformat = config['format']
        self.lastrun    = config['lastrun']
        self.state      = config[lib.config.ENG][key]['state']
        self.username   = config[lib.config.ENG][key]['user']
        self.password   = config[lib.config.ENG][key]['pass']

        self.cachesize  = 1<<20
        self.cachename  = os.path.join('engines', '{}.cache'.format(self.name))
        try:
            self.cache = pickle.load(open(self.cachename, 'rb'))
            self.log.debug('file exists:  %s (%d items, %fMb on disk)', 
                self.cachename, len(self.cache), os.path.getsize(self.cachename)/1048576)

        except IOError:
            self.cache = EngineCache(self.cachesize)
            self.log.debug('file created: %s', self.cachename)
            pickle.dump(self.cache, open(self.cachename, 'wb'))


        self.tagfile   = 'tags_{}.txt'.format(self.name)
        self.tags      = []
        for line in open(self.tagfile):
            raw_line = line.strip()
            if not raw_line.startswith("#") and raw_line != '':
                self.tags.append(raw_line)

    def __save_cache__(self):
        self.log.debug('saving %s', self.cachename)
        pickle.dump(CACHE, open(self.cachename, 'wb'), pickle.HIGHEST_PROTOCOL)

    @abc.abstractmethod
    def get_login(self):
        ''' returns true if login was successful, false if it failed for any reason '''

    @abc.abstractmethod
    def get_query(self, query_str):
        '''returns a list of tuples, each containing (uuid, pathname, url), where:
            - pathname is the full path and formatted name
            - url is the complete, raw url where the file can be downloaded from
        returns None when query_str yeilds no valid* results
            *: depending on program config, previously-seen files can be omitted'''

    def update(self):
        '''calls get_query for every tag in the tagfile.  returns one list
        of tuples, each containing (uuid, pathname, url)'''
        new_files = []

        for tag in self.tags:
            new_files += get_query(tag)

        return new_files


