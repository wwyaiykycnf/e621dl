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
        
        # parse common settings
        eng_config = EngineUtils.validate_common_defaults(engine, **ini[name])

        # parse any custom engine settings and add these to config
        eng_config.update(engine.validate_custom_defaults(**ini[name]))

        pprint(eng_config)



if __name__ == '__main__':
    execute()
