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

    ### 1:  Parse INI file ###

    # first, get logger instance so errors can be reported
    LOG = config.init_logs()

    # get system info for debug log
    LOG.info('e621dl version: %s', config.VERSION)
    LOG.debug('plaform: %s', platform.platform())
    LOG.debug('python:  %s', platform.python_version())

    # parse config file.  raises exceptions on failure
    CONFIG = config.get_config()

    ### 2: Use engines to build download list ###
    for i in ENGINES:
        print(i, ENGINES[i])
    #e621_engine.get_login()