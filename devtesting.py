#!/usr/bin/env python3

import logging
import platform

# project imports
import lib.config as config
from lib.engines.supported_engines import ENGINES

# globals
CONFIG = {}
LOG = None

if __name__ == '__main__':
    configuration = config.Configuration()

    ### 1:  Parse INI file ###

    # first, get logger instance so errors can be reported
    LOG = configuration.get_logger()

    # get system info for debug log
    LOG.info('e621dl version: %s', config.VERSION)
    LOG.debug('plaform: %s', platform.platform())
    LOG.debug('python version:  %s', platform.python_version())

    # parse config file.  raises exceptions on failure
    CONFIG = configuration.get_config()

    ### 2: Use engines to build download list ###
    for key in CONFIG[config.ENG]:
        if CONFIG[config.ENG][key]['state'] == False:
            LOG.info('%s engine is disabled in config file', key)
            break
        current_eng = ENGINES[key](CONFIG, key)

