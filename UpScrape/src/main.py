#!/usr/bin/env python3

# standard imports
import logging

# upscrape imports
import utils 

LOG = None

def execute():
    utils.enable_logging()
    LOG = logging.getLogger('main')
    LOG.info('hello')


if __name__ == '__main__':
    execute()
