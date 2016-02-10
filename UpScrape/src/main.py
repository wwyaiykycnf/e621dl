#!/usr/bin/env python3

# standard imports
import logging
import platform
from pprint import pprint

# upscrape imports
#from .engines import common

import utils
from engines import get_engines
from engines.common import EngineUtils
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
    ini = utils.IniUtil.read_ini()

    for engine in get_engines():
        name = engine.get_name()
        
        # validate/parse common settings
        eng_config = EngineUtils.validate_common_defaults(engine, **ini[name])

        # validate/parse any custom engine settings and 
        custom_config = engine.validate_custom_defaults(**ini[name])

        # merge custom and common config.  eng_config should now be fully 
        # populated with validated settings
        eng_config.update(custom_config)

        # begin the update
        engine.scrape(**eng_config)

if __name__ == '__main__':
    execute()
