#!/usr/bin/env python
# pylint: disable=missing-docstring,line-too-long,too-many-public-methods,
import os.path
import logging
import sys
import lib.support as support
import lib.default as default
import datetime
import cPickle as pickle
import json
import lib.e621_api as e621_api
import re

##############################################################################
# INITIALIZATION
# - parse command line arguments
# - create a logger to show runtime messages
# - open config file
# - open file containing tracked tags
# - populate the recent downloads cache
##############################################################################
CONFIG_FILE = 'config.txt' # modify to use different config file

# get args dictionary
ARGS = support.get_args_dict()

# set up logging
logging.basicConfig(level=ARGS['log_lvl'], format=default.LOGGER_FMT,
    stream=sys.stderr)
LOG = logging.getLogger('e621dl')

# this flag will be set to true if a fatal error occurs in pre-update
EARLY_TERMINATE = False

# read the config file.  if not found, create a new one
if not os.path.isfile(CONFIG_FILE):
    CONFIG = support.make_default_configfile(CONFIG_FILE)
    EARLY_TERMINATE = True
else:
    CONFIG = support.read_configfile(CONFIG_FILE)

# read the tags file.  if not found, create a new one
if not os.path.isfile(CONFIG['tag_file']):
    support.make_default_tagfile(CONFIG['tag_file'])
    EARLY_TERMINATE = True
else:
    TAGS = support.read_tagfile(CONFIG['tag_file'])

# tags was read but contained nothing
if len(TAGS) == 0:
    LOG.error('no tags found in ' + CONFIG['tag_file'])
    LOG.error('add tags (or groups of tags) to this file and re-run the program')
    EARLY_TERMINATE = True

# open the cache (this can't really fail; just creates a new blank one)
CACHE = support.get_cache(CONFIG['cache_name'], CONFIG['cache_size'])

# create the downloads directory if needed
if not os.path.exists(CONFIG['downloads']):
    os.makedirs(CONFIG['downloads'])

# keeps running total of files downloaded in this run
TOTAL_DOWNLOADS = 0

# exit before updating if any errors occurred in pre-update
if EARLY_TERMINATE:
    LOG.error('error(s) encountered during initialization, see above')
    exit()
else:
    LOG.debug('successfully initialized\n')

##############################################################################
# UPDATE
# - for each tag (or tag group) in the tagfile:
#   - for each upload since the last time e621dl was run:
#       - if the file has not previously been downloaded, download it
# - count number of downloads for reporting in post-update
##############################################################################

LOG.info("e621dl was last run on " + CONFIG['last_run'])

for line in TAGS:
    LOG.info("Checking for new uploads tagged: " + line)

    # prepare to start accumulating list of download links for line
    accumulating = True
    current_page = 1
    links_to_download = []

    while accumulating:
        LOG.debug('getting page ' + str(current_page) + ' of ' + line)
        links_found = e621_api.get_posts(line, CONFIG['last_run'],
                current_page, default.MAX_RESULTS)

        if not links_found:
            accumulating = False

        else:
            # add links found to list to be downloaded
            links_to_download += links_found
            # continue accumulating if found == max, else stop accumulation
            accumulating = len(links_found) == default.MAX_RESULTS
            current_page += 1

    remaining = len(links_to_download)

    if remaining == 0:
        LOG.info('no new uploads for: ' + line)

    else:
        LOG.info(str(remaining) + ' new uploads for: ' + line)

        for item in links_to_download:

            LOG.debug('item md5 = ' + item.md5)
            # construct full filename
            filename = re.sub('[\<\>:"/\\\|\?\*\ ]', '_', line) + '--' + \
                item.md5 + '.' + item.ext

            # skip if already in cache
            if item.md5 in CACHE:
                LOG.info('(' + str(remaining) + ') skipped (previously downloaded)')

            # skip if already in download directory
            elif os.path.isfile(filename):
                LOG.info('(' + str(remaining) + ') skipped (already in downloads directory')

            # otherwise, download it
            else:
                LOG.info('(' + str(remaining) + ') downloading... ')
                e621_api.download(item.url, CONFIG['downloads'] + filename)

                # push to cache, write cache to disk
                CACHE.push(item.md5)
                pickle.dump(CACHE, open('.cache', 'wb'), pickle.HIGHEST_PROTOCOL)
                TOTAL_DOWNLOADS += 1

            # decrement remaining downloads
            remaining -= 1

        LOG.debug('update for ' + line + ' completed\n')
    print ''

##############################################################################
# WRAP-UP
# - report number of downloads in this session
# - set last run to yesterday (see FAQ for why it isn't today)
##############################################################################
LOG.info('total files downloaded: ' + str(TOTAL_DOWNLOADS))
YESTERDAY = datetime.date.fromordinal(datetime.date.today().toordinal()-1)
CONFIG['last_run'] = YESTERDAY.strftime(default.DATETIME_FMT)

with open(CONFIG_FILE, 'wb') as outfile:
    json.dump(CONFIG, outfile, indent=4, sort_keys=True,
        ensure_ascii=False, separators=(',', ':\t\t'))

LOG.info('last run updated to ' + CONFIG['last_run'])

exit()
