#!/usr/bin/env python3

import logging

# project imports
import lib.config as config

# engine imports
import engines.e621 as e621

# globals
CONFIG = {}
LOG = None

if __name__ == '__main__':

    # log messages with levels of DEBUG and higher to file, and those messages
    # at level INFO and higher to the console.  
    # see docs.python.org/2/howto/logging-cookbook.html#logging-to-multiple-destinations

    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                        datefmt='%m-%d %H:%M',
                        filename='debug.log',
                        filemode='w')
    # define a Handler which writes INFO messages or higher to the sys.stderr
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    # set a format which is simpler for console use
    formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
    # tell the handler to use this format
    console.setFormatter(formatter)
    # add the handler to the root logger
    logging.getLogger('').addHandler(console)
    # get the logger used for main
    LOG = logging.getLogger('e621dl')

    CONFIG = config.get_config()
    