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
from lib.downloader import multi_download
from lib.version import VERSION
from multiprocessing import freeze_support

if __name__ == '__main__':
    freeze_support()    

##############################################################################
# INITIALIZATION
# - parse command line arguments
# - create a logger to show runtime messages
# - open config file
# - open file containing tracked tags
# - populate the recent downloads cache
##############################################################################
    CONFIG_FILE = 'config.txt' # modify to use different config file

    # set up logging
    logging.basicConfig(
            level=support.get_verbosity_level(),
            format=default.LOGGER_FMT,
            stream=sys.stderr)
    LOG = logging.getLogger('e621dl')

    # report current version
    LOG.info('running e621dl version %s', VERSION)

    # this flag will be set to true if a fatal error occurs in pre-update
    EARLY_TERMINATE = False

    # read the config file.  if not found, create a new one
    EARLY_TERMINATE |= not os.path.isfile(CONFIG_FILE)
    CONFIG = support.get_configfile(CONFIG_FILE)
    EARLY_TERMINATE |= not support.validate_config(CONFIG)

    # read the tags file.  if not found, create a new one
    EARLY_TERMINATE |= not os.path.isfile(CONFIG['tag_file'])
    TAGS = support.get_tagfile(CONFIG['tag_file'])

    # are there any tags in the tags file?
    EARLY_TERMINATE |= not support.validate_tagfile(TAGS, CONFIG['tag_file'])

    # open the cache (this can't really fail; just creates a new blank one)
    CACHE = support.get_cache(CONFIG['cache_name'], CONFIG['cache_size'])

    # create the downloads directory if needed
    if not os.path.exists(CONFIG['download_directory']):
        os.makedirs(CONFIG['download_directory'])

    # exit before updating if any errors occurred in pre-update
    if EARLY_TERMINATE:
        LOG.error('error(s) encountered during initialization, see above')
        sys.exit(-1)

##############################################################################
# UPDATE
# - for each tag (or tag group) in the tagfile:
#   - for each upload since the last time e621dl was run:
#       - if the file has not previously been downloaded, download it
# - count number of downloads for reporting in post-update
##############################################################################
    LOG.info("e621dl was last run on %s", CONFIG['last_run'])

    # keeps running total of files downloaded in this run
    TOTAL_DOWNLOADS = 0

    URL_AND_NAME_LIST = []

    for line in TAGS:
        LOG.debug("Checking for new uploads tagged: %s", line)

        # prepare to start accumulating list of download links for line
        accumulating = True
        current_page = 1
        links_in_cache = 0
        links_on_disk = 0
        will_download = 0
        potential_downloads = []

        while accumulating:
            links_found = e621_api.get_posts(line, CONFIG['last_run'],
                    current_page, default.MAX_RESULTS)

            if not links_found:
                accumulating = False

            else:
                # add links found to list to be downloaded
                potential_downloads += links_found
                # continue accumulating if found == max, else stop accumulation
                accumulating = len(links_found) == default.MAX_RESULTS
                current_page += 1

        LOG.info('%d new uploads tagged: %s', len(potential_downloads), line)

        if len(potential_downloads) > 0:

            # there were uploads. determine should any be downloaded
            current = 0
            for idx, item in enumerate(potential_downloads):

                LOG.debug('item md5 = %d', item.md5)
                current = '\t(' + str(idx) + ') '

                # construct full filename
                filename = support.safe_filename(line, item, CONFIG)

                # skip if already in download directory
                if os.path.isfile(CONFIG['download_directory'] + filename):
                    links_on_disk += 1
                    LOG.debug('%s skipped (already in download dir', current)

                # skip if already in cache
                elif item.md5 in CACHE:
                    links_in_cache += 1
                    LOG.debug('%s skipped (previously downloaded)', current)

                # otherwise, download it
                else:
                    LOG.debug('%s will be downloaded', current)
                    URL_AND_NAME_LIST.append(
                        (item.url, CONFIG['download_directory'] + filename))

                    will_download += 1
                    # push to cache, write cache to disk
                    CACHE.push(item.md5)
                    TOTAL_DOWNLOADS += 1

            LOG.debug('update for %s completed\n', line)
            LOG.info('%5d total (+%d new, %d existing, %d cached)\n',
                TOTAL_DOWNLOADS, will_download, links_on_disk, links_in_cache)

    if URL_AND_NAME_LIST:
        print ''
        LOG.info('starting download of %d files', len(URL_AND_NAME_LIST))
        multi_download(URL_AND_NAME_LIST, CONFIG['parallel_downloads'])
    else:
        LOG.info('nothing to download')


##############################################################################
# WRAP-UP
# - write cache out to disk
# - report number of downloads in this session
# - set last run to yesterday (see FAQ for why it isn't today)
##############################################################################
    pickle.dump(CACHE, open('.cache', 'wb'), pickle.HIGHEST_PROTOCOL)
    if URL_AND_NAME_LIST:
        LOG.info('successfully downloaded %d files', TOTAL_DOWNLOADS)
    YESTERDAY = datetime.date.fromordinal(datetime.date.today().toordinal()-1)
    CONFIG['last_run'] = YESTERDAY.strftime(default.DATETIME_FMT)

    with open(CONFIG_FILE, 'wb') as outfile:
        json.dump(CONFIG, outfile, indent=4,
            sort_keys=True, ensure_ascii=False)

    LOG.info('last run updated to %s', CONFIG['last_run'])

    sys.exit(0)
