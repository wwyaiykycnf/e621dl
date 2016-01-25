#!/usr/bin/env python3

# standard imports
import logging
import platform

# upscrape imports
import utils 

LOG = None

def execute():
    utils.enable_logging()
    LOG = logging.getLogger('main')
    
    LOG.info('UpScrape: %s', utils.VERSION)
    LOG.debug('plaform:  %s', platform.platform())
    LOG.debug('python:   %s', platform.python_version())

    util = utils.IniUtil()
    util.create_ini_from_defaults()


if __name__ == '__main__':
    execute()
