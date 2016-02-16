#!/usr/bin/env python3

from collections import OrderedDict
from .common import EngineBase, EngineUtils
from pprint import pprint
import os
from pathlib import Path
import urllib.request
import urllib.parse
import json
import pickle

import logging

class e621_Engine(EngineBase):
    name = "e621"
    taglist_text = [
        'list the tags to keep updated below.',
        'each line represents one search performed on the site',        
        'multiple tags are allowed on a line.',
        'any file uploaded since last_run will be downloaded'
        ]

    blacklist_text = [
        'list blacklisted tags below.',
        'multiple tags are allowed on a line.',
        'any post which matches any line in this file will not be not downloaded'
        ]
    ff_text = [
        'list the tags to fast-forward below.',
        'each line represents one search performed on the site',        
        'multiple tags are allowed on a line.',
        'last_run will be ignored for these searches (all matching files will download)',
        'for best performance, remove lines from this file after successful fast-forward'
        ]
    comment_char = '#'
    
    log = logging.getLogger("e621")

    DEFAULTS = OrderedDict()
    DEFAULTS['format'] = '${tag}_${id}'
    DEFAULTS['duplicates'] = 'off'
    max_results = 100

    cache = []
    cache_size = 10000
    cache_path = os.path.join('src', 'engines', 'e621.cache')

    illegal_chars = """[]{}<>*\/=!@#$"',:;"""

    def get_name(self):
        return self.name

    def get_taglist_text(self):
        return self.taglist_text

    def get_blacklist_text(self):
        return self.blacklist_text

    def get_fastforward_text(self):
        return self.ff_text    

    def get_comment_char(self):
        return self.comment_char

    def validate_custom_defaults(self, **kwargs):
        config = {}

        # pull out boolean values
        abort = False
        try:
            config['duplicates'] = EngineUtils.to_bool(kwargs.get('duplicates'))
            config['enabled'] = EngineUtils.to_bool(kwargs.get('enabled'))

        except ValueError:
            abort = False

        if abort:
            config['enabled'] = False

        if config['enabled'] == True and config['duplicates'] == False:
            self.cache = self.get_cache()

        # todo: validate format... maybe this will not happen here
        config['format'] = kwargs.get('format').translate({ord(i):'%' for i in '$'})
        print(config['format'])

        return config

    def get_custom_defaults_OrderedDict(self):
        return self.DEFAULTS

    def open_cache(self):
        if self.duplicates == True:
            return

        try:
            with open (self.cache_path, 'rb') as infile:
                self.cache = pickle.load(infile)
                self.log.debug('opened %s containing %d items', self.cache_path, len(self.cache))
        except FileNotFoundError:
            self.log.info('cache was not found and was created from defaults')
            self.log.debug('cache path: %s', self.cache_path)
            pass

    def close_cache(self):
        if self.duplicates == True:
            return

        with open(self.cache_path, 'wb') as outfile:
            data = self.cache[-self.cache_size:]
            pickle.dump(data, outfile, pickle.HIGHEST_PROTOCOL)
            self.log.debug('cache was written to disk (%d items)', len(data))

    def get_page_posts(self, tag, page, since=None):
        # if 'since' was supplied, append it to the tag
        tag = tag + ' date:>' + since if since else tag 

        search = 'http://e621.net/post/index.json?tags={}&page={}&limit={}'.format(tag, page, self.max_results)

        with urllib.request.urlopen(search) as request:
            response = json.loads(request.read().decode())
            self.log.debug('  url: %s', search)
            self.log.debug('  posts: [%d], page: [%d]', len(response), page)
            return response

    def get_all_posts(self, tag, since=None):
        accumulating = True
        potential_downloads = []
        current_page = 1
        
        if (since):
            self.log.info("finding uploads matching '%s' since %s", tag, since)
        else:
            self.log.info("finding all uploads matching '%s' ever uploaded", tag)

        while (accumulating):
            links_found = self.get_page_posts(tag, current_page, since)
            if not links_found:
                accumulating = False
            else:
                # add links found to list to be downloaded
                potential_downloads += links_found
                # continue accumulating if found == max, else stop accumulation
                accumulating = len(links_found) == self.max_results
                current_page += 1
        return potential_downloads

    def get_filename(self, tag, post, format_str):
        #format_str = '%(artist)s_%(md5)s.%(file_ext)s'
        post['tag'] = tag
        name = format_str % post
        safe_name = name.translate({ord(i):None for i in self.illegal_chars})
        return safe_name.replace(' ', '_')


    def scrape(self, last_run, **kwargs):
        self.duplicates = kwargs['duplicates']
        
        self.open_cache()
        tag = 'cat dog fox'
        downloads = self.get_all_posts(tag, '2016-2-8')
        
        pprint(downloads[0])
        print (self.get_filename(tag, downloads[0], kwargs['format']) )
        #for post in downloads:
        #    print(post)
            #filename = get_filename(post)


        self.close_cache()
        #for line in kwargs['fastforwardlist']:
        #    self.get_all_posts(line)
        #
        #for line in kwargs['taglist']:
        #    self.get_all_posts(line, since)
        # 
        # if kwargs['duplicates'] == False:
        #    self.close_cache()






