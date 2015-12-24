#!/usr/bin/env python3
''' todo '''
import abc
import lib.config
import os
import pickle
import logging
import configparser

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
        - get_default_tagfile_contents(): returns contents of a new, blank tagfile
        - get_default_blacklist_contents(): returns contents of a new, blank blacklist
        - get_query(query_str, use_blacklist): performs a query for query_str
    ''' 

    @abc.abstractmethod
    def get_default_tagfile_contents(self):
        '''returns contents of a new, blank tagfile'''

    @abc.abstractmethod
    def get_default_blacklist_contents(self):
        '''returns contents of a new, blank blacklist'''

    def __init_file__(self, filename, contents):
        ''' returns True if file was found, False if new one was made'''
        lines = []
        if os.path.exists(filename):
            self.log.debug('file exists:  %s', filename)
        else:
            with open(filename, 'w') as fp:
                fp.write(contents())
            self.log.debug('file created: %s', filename)

        for line in open(filename):
            raw_line = line.strip()
            if not raw_line.startswith("#") and raw_line != '':
                lines.append(raw_line)
        return lines

    def __save_cache__(self):
        self.log.debug('saving %s', self.cachename)
        pickle.dump(self.cache, open(self.cachename, 'wb'), pickle.HIGHEST_PROTOCOL)

    def __init_cache__(self, filename):
        cachesize = 1<<20
        try:
            fp = open(filename, 'rb')
            cache = pickle.load(fp)
            self.log.debug('file exists:  %s (%d items, %fMb on disk)', 
                filename, len(cache), os.path.getsize(filename)/1048576)
        except FileNotFoundError:
            cache = EngineCache(cachesize)
            self.log.debug('file created: %s', filename)
            pickle.dump(cache, open(filename, 'wb'), pickle.HIGHEST_PROTOCOL)

        return (filename, cache)

    def __init__(self, config, key):
        self.name       = key
        self.log        = logging.getLogger(self.name)
        self.error      = None
        
        self.nameformat = config['format']
        self.lastrun    = config['lastrun']
        self.state      = config[lib.config.ENG][key]['state']
        self.tags_filename = config[lib.config.ENG][key]['tags']
        self.blacklist_filename = config[lib.config.ENG][key]['blacklist']
 
        ## cache initialization
        self.cachename = os.path.join('lib', 'engines', '{}.cache'.format(key))
        self.cache = self.__init_cache__(self.cachename)

        ## tagfile initialization
        self.tags = self.__init_file__(self.tags_filename, self.get_default_tagfile_contents)

        ## blacklist initialization
        self.blacklist = self.__init_file__(self.blacklist_filename, self.get_default_blacklist_contents)



    @abc.abstractmethod
    def get_query(self, query_str, use_blacklist):
        '''returns a list of tuples, each containing (uuid, pathname, url), where:
            - pathname is the full path and formatted name
            - url is the complete, raw url where the file can be downloaded from
        returns None when query_str yeilds no valid* results
            *: depending on program config, previously-seen files can be omitted'''
        return False
        
    def update(self):
        '''calls get_query for every tag in the tagfile.  returns one list
        of tuples, each containing (uuid, pathname, url)'''
        new_files = []

        for tag in self.tags:
            new_files += get_query(tag)

        return new_files


