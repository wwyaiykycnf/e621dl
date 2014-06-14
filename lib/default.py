#!/usr/bin/env python
# pylint: disable=bad-whitespace, missing-docstring

from datetime import datetime

DATETIME_FMT = "%Y-%m-%d"

CONFIG_FILE = {
    'cache_name':   ".cache",
    'cache_size':   65536,
    'downloads':    "downloads/",
    'last_run':     datetime.now().strftime(DATETIME_FMT),
    'tag_file':     "tags.txt"
}

LOGGER_FMT = "%(name)-11s %(levelname)-8s %(message)s"

TAG_FILE = '''# Instructions:
#
# Add tags/artists to download to this file, one group per line.  Any tag
# combination that works on the web site will work here, including all the
# meta-tags (see https://e621.net/help/cheatsheet for more information on
# tags and meta-tags).
#
# NOTE: All lines in this file that begin with # are treated as comments and
# are ignored by e621dl
#
# Each line in this file will be treated as a separate group, and a new folder
# inside the downloads directory will be created for each line in this file.
#
# List any tags, artists, meta-tags, or groups of tags you would like to
# track below:
'''

