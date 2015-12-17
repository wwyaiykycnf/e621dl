#!/usr/bin/env python3

import logging
import platform

# project imports
import lib.config as config

# engine imports
from engines.e621 import e621

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
    e621_engine = e621(CONFIG, "e621_engine")
    #e621_engine.get_login()