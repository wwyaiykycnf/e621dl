#!/usr/bin/env python
# pylint: disable=missing-docstring,line-too-long,too-many-public-methods,
import os.path
import logging
import sys
import lib.regex as regex
import lib.support as support
import lib.default as default
import datetime
import cPickle as pickle
import json

# this is only here temporarily
SPOOF = support.SpoofOpen()
def download_image(link, tag, path):
    filename = regex.get_filename(link)
    completepath = path + tag + "_" + filename

    if os.path.isfile(completepath) == True:
        return ' skipped (already exists)'

    elif filename in CACHE:
        return ' skipped (previously downloaded)'

    else:
        with open(completepath, 'wb') as dest:
            source = SPOOF.open(link)
            dest.write(source.read())

        CACHE.push(filename)
        pickle.dump(CACHE, open('.cache', 'wb'), pickle.HIGHEST_PROTOCOL)

        return ' downloaded'

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

for tag in TAGS:
    LOG.info("Checking for new uploads tagged: " + tag)

    accumulating = True
    page_number = 1
    dl_links = []

    # get all post pages in same list
    while accumulating:
        results_page = regex.get_results_page(tag, CONFIG['last_run'], page_number)

        if regex.results_exist(results_page):
            LOG.debug('page ' + str(page_number) + ' contained results')
            dl_links += regex.get_links(results_page)
            page_number += 1

        else:
            LOG.debug('page ' + str(page_number) + ' contained nothing')
            accumulating = False

    LOG.info('number of uploads found: ' + str(len(dl_links)))

    # download image in each post page
    remaining = len(dl_links)
    for link in dl_links:
        status = download_image(link, tag, CONFIG['downloads'])
        img_string = '(%d) %s' % (remaining, regex.get_filename(link))

        LOG.info(img_string + status)
        if status == ' downloaded':
            TOTAL_DOWNLOADS += 1
        remaining -= 1
    LOG.info('update for ' + tag + ' completed\n')


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
