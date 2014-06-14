#!/usr/bin/env python
# pylint: disable=missing-docstring,line-too-long,too-many-public-methods,
import os.path
import datetime
import logging
import init_e621dl
import sys
import regex
import cPickle as pickle

# IMPORTANT: Update this line to point to your tagfile
TAGFILE = 'tags.txt'

def get_last_run():
    try:
        with open(".lastrun.txt", 'r') as lastrun:
            return lastrun.read()

    except IOError:
        return datetime.date.today().strftime("%Y-%m-%d")

def set_last_run():
    with open(".lastrun.txt", 'w') as lastrun:
        yesterday = datetime.date.fromordinal(datetime.date.today().toordinal()-1)
        lastrun.write(yesterday.strftime("%Y-%m-%d"))

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

# parse arguments and set up logger
ARGS = init_e621dl.get_args()
logging.basicConfig(level=init_e621dl.get_log_level(ARGS),
    format='%(name)-8s %(levelname)-8s %(message)s', stream=sys.stderr)
LOG = logging.getLogger('e621dl')

# prepare to run
CACHE = init_e621dl.get_downloads_list('.cache')
TAGS = init_e621dl.read_tags_file(TAGFILE)
LASTRUN = get_last_run()
DOWNLOAD_DIR = '''./downloads/'''
TOTAL_DOWNLOADS = 0
SPOOF = init_e621dl.SpoofOpen()

if not os.path.exists(DOWNLOAD_DIR):
    os.makedirs(DOWNLOAD_DIR)

LOG.info("e621dl was last run on " + LASTRUN)

for tag in TAGS:
    LOG.info("Checking for new uploads tagged: " + tag)

    accumulating = True
    page_number   = 1
    dl_links = []

    # get all post pages in same list
    while accumulating:
        results_page = regex.get_results_page(tag, LASTRUN, page_number)

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
        status = download_image(link, tag, DOWNLOAD_DIR)
        img_string = '(%d) %s' % (remaining, regex.get_filename(link))

        LOG.info(img_string + status)
        if status == ' downloaded':
            TOTAL_DOWNLOADS += 1
        remaining -= 1

    LOG.info('update for ' + tag + ' completed')
    LOG.info('')

#set_last_run()

LOG.info('total files downloaded: ' + str(TOTAL_DOWNLOADS))
set_last_run()
LOG.info('last run set to ' + get_last_run())

exit()

