#!/usr/bin/env python3

# from .common import EngineUtils
from .e621 import e621_Engine

_ALL_ENGINES = [
    eng
    for name, eng in globals().items()
    if name.endswith('_Engine')
]

def get_engines():
    """ Return a list of an instance of every supported extractor.
    The order does matter; the first extractor matched is the one handling the URL.
    """
    return [eng() for eng in _ALL_ENGINES]

def get_engine_defaults():
    return [eng.get_defaults() for eng in _ALL_ENGINES]