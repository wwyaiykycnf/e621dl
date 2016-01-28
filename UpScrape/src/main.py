#!/usr/bin/env python3

# standard imports
import logging
import platform
from pprint import pprint

# upscrape imports
#from .engines import common

import utils
from engines import get_engines

LOG = None

def execute():
    # log everything to file, log warning/error to console
    utils.setup_logging()
    LOG = logging.getLogger('main')
    
    # record platform/version info for debug
    LOG.info('UpScrape: %s', utils.VERSION)
    LOG.debug('plaform:  %s', platform.platform())
    LOG.debug('python:   %s', platform.python_version())

    # get program setting.  returning from this call means read was successful
    config = utils.IniUtil.read_ini()

    for engine in get_engines():
        name = engine.get_name()
        engine.prepare(**config[name])


if __name__ == '__main__':
    execute()
