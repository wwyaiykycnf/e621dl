#!/usr/bin/env python3

# standard imports
import logging
import platform
from pprint import pprint

# upscrape imports
#from .engines import common

import utils

LOG = None

def execute():
    utils.setup_logging()
    LOG = logging.getLogger('main')
    
    LOG.info('UpScrape: %s', utils.VERSION)
    LOG.debug('plaform:  %s', platform.platform())
    LOG.debug('python:   %s', platform.python_version())

    util = utils.IniUtil()
    config = {}

    try:
        with open(utils.DEFAULT_INI_NAME, 'r') as fp:
            config = util.ini_to_dict(fp)
    except FileNotFoundError:
        util.make_ini_from_defaults()
        LOG.error('%s was not found and was created from defaults',
            utils.DEFAULT_INI_NAME)
        LOG.error('inspect the generated file and re-run the program')
    pprint(config)


if __name__ == '__main__':
    execute()
