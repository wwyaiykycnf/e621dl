#!/usr/bin/env python3

import sys

import os.path
path = os.path.realpath(os.path.abspath(__file__))
print(path)
sys.path.insert(0, os.path.join(os.path.dirname(path), 'src'))

from main import execute

if __name__ == '__main__':
    execute()