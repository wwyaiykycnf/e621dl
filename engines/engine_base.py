#!/usr/bin/env python3
''' todo '''
import abc
import lib.config 

class Engine(object, metaclass=abc.ABCMeta):
    
    def __init__(self, config, key):
        self.name = key
        self.nameformat = config['format']
        self.lastrun    = config['lastrun']
        self.state      = config[config.ENG][key]['state']
        self.username   = config[config.ENG][key]['user']
        self.password   = config[config.ENG][key]['pass']

    @abc.abstractmethod
    def get_login():
        ''' returns true if login was successful, false if it failed for any reason '''

    @abc.abstractmethod
    def get_query(query_str):
        '''returns a list of tuples, each containing (pathname, url), where:
            - pathname is the full path and formatted name
            - url is the complete, raw url where the file can be downloaded from
        returns None when query_str yeilds no valid* results
            *: depending on program config, previously-seen files can be omitted'''