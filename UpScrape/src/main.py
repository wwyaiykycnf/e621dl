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
    config = utils.IniUtil.read_ini()

    for engine in get_engines():
        name = engine.get_name()
        eng_config = config[name]
        
        eng_config.update(EngineUtils.read_common_tagfiles(engine, utils.TagUtil))

        pprint(eng_config)

        # engine.prepare(**config[name])


        # if config[name]['enabled'] == False:
        #     LOG.info('engine {} is disabled in {}'.format(name, utils.DEFAULT_INI_NAME))
        #     break
        # pprint(config[name])


if __name__ == '__main__':
    execute()
