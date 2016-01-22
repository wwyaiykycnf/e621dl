#!/usr/bin/env python3

from .common import EngineBase, EngineUtils

class e621_Engine(EngineBase):

    def prepare(self, **kwargs):
        ''' called during creation of engine.
            - checks engine config (kwargs) for errors
            - gets blacklist from disk or remote and checks it for errors
            - performs other engine-specific checks to ensure readiness

            Should raise NotImplmentedError if any error occurs which prevents
            the engine from functioning. 
        '''
        log.debug('kwargs = %s', kwargs))
        self.lastrun    = kwargs.get('lastrun')
        self.format     = kwargs.get('format')
        self.duplicates = kwargs.get('duplicates')
        self.state      = kwargs.get('state')
        self.tag_path   = kwargs.get('tags')
        self.bl_path    = kwargs.get('blacklist')
    
    def is_blacklisted(self, query_result):
        ''' checks a query_result against the engine blacklist (if present).
            
            a default implementation of this method is provided in EngineBase,
            but it can be overridden if needed. 
        
        returns 
            - True      query_result is blacklisted (do not download)
            - False     query_result is not blacklisted (proceed with download)
        '''
        # TODO: default blacklist code here
        return False

    def get_query(self, query):
        ''' queries the site for uploads matching <query>
            
            if ignore_date is true, the last_run section in the config file 
                is ignored and all files EVER UPLOADED that match the query 
                will be downloaded. 

            returns 
                - list [query_result] if any were found
                - None if nothing was found or there were errors
        '''

    def update(self):
        ''' processes the tagfile for the engine and downloads all files that
            have not been previously seen  

            tagfile lines starting with $ are fast-forwarded, meaning last_run 
                date in the config file is ignored for these lines and all files
                EVER UPLOADED are downloaded. 

            blacklist (if one exists) is applied to all files before downloading

            a default implementation of this method is provided in EngineBase,
            but it can be overridden if needed.
        '''
        # TODO: default update code here

    @abstractmethod
    def make_filename(self, query_result):
        ''' given a single query_result, creates a proper filename, taking user
            specified format and other program settings into account'''


    @abstractmethod
    def download_file(self, **kwargs):
        ''' downloads a single file.  is called once for each file found during
            the update. 

            returns true/false indicating whether success of file download'''
