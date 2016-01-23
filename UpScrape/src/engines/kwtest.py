#!/usr/bin/env python3

def kw(**kwargs):
    print(kwargs)

# kw(big='foot')
# > {'big': 'foot'}

# a = {'foo':'bar'}
# kw(**a)
# > {'foo': 'bar'}